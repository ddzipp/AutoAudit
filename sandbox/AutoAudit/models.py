import datetime
import os
import re
import time

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.core.files.base import File as FileBase
import hashlib
import magic

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Create your models here.


"""
File 用于存放用户上传的文件/代码的一些通用信息，所有用户上传的代码都需要用 .txt 文件装载，这样可以将两种上传形式都使用文件来存储。
id: 文件的唯一主键
name: 文件名
type: 文件类型
size: 文件大小（单位为字节）
submission_date: 提交日期
detection_count: "x/y" x 为检测出威胁的引擎数，y 为总引擎数
risk_level: 风险评级
content_file: 文件本身（在数据库里实际存的是路径）
md5,sha1,sha256: hash
"""

'''
   @classmethod
    def insert(cls, name, type, submission_date, detection_count, risk_level, content_file):
        # Save the file to the file system
        fs = FileSystemStorage()
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{name}"
        filename = fs.save(filename, content_file)

        # Get the full path of the saved file
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Calculate the file size
        size = os.path.getsize(file_path)

        # Calculate the file digests
        with open(file_path, 'rb') as f:
            content = f.read()
        digests = cls.get_digest(content)

        # Create a new File instance with the specified field values
        new_file = cls(name=name, type=type, submission_date=submission_date,
                       detection_count=detection_count, risk_level=risk_level,
                       md5=digests['md5'], sha256=digests['sha256'], sha1=digests['sha1'],
                       size=size, content_file=file_path)
        new_file.save()
        return new_file
'''


class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    size = models.IntegerField()
    submission_date = models.DateTimeField(auto_now_add=True)
    detection_count = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=50)
    md5 = models.CharField(max_length=32)
    sha256 = models.CharField(max_length=64)
    sha1 = models.CharField(max_length=40)
    content_file = models.FileField()

    @classmethod
    def insert(cls, detection_count, risk_level, content_file):
        # Save the file to the file system
        name = content_file.name

        fs = FileSystemStorage()
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{name}"
        filename = fs.save(filename, content_file)

        # Get the full path of the saved file
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Check the type:
        magic_obj = magic.Magic()
        magic_obj = magic.Magic(mime=True)
        type = None
        with open(file_path, "rb") as file:
            content = file.read()
        type = magic_obj.from_buffer(content)
        # Calculate the file size
        size = os.path.getsize(file_path)

        # Calculate the file digests
        with open(file_path, 'rb') as f:
            content = f.read()
        digests = cls.get_digest(content)

        # Create a new File instance with the specified field values
        new_file = cls(name=name, type=type,
                       detection_count=detection_count, risk_level=risk_level,
                       md5=digests['md5'], sha256=digests['sha256'], sha1=digests['sha1'],
                       size=size, content_file=file_path)
        new_file.save()

        return new_file

    @classmethod
    def get_by_id(cls, Id):

        try:
            file = cls.objects.get(id=Id)
            return file
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_name(cls, Name):
        try:
            files = cls.objects.filter(name=Name)
            return files
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_type(cls, Type):
        try:
            files = cls.objects.filter(type=Type)
            return files
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_sha256(cls, digest):
        try:
            files = cls.objects.filter(sha256=digest)
            return files
        except cls.DoesNotExist:
            return None

    @staticmethod
    def get_digest(content):
        md5 = hashlib.md5(content).hexdigest()
        sha256 = hashlib.sha256(content).hexdigest()
        sha1 = hashlib.sha1(content).hexdigest()
        return {'md5': md5, 'sha256': sha256, 'sha1': sha1}

    @classmethod
    def update_by_id(cls, Id, **kwargs):
        file = None
        try:
            file = cls.objects.get(id=Id)
        except cls.DoesNotExist:
            return None
        for field, value in kwargs.items():
            setattr(file, field, value)
        file.save()
        return file

    @classmethod
    def delete_by_id(cls, Id):
        file = cls.objects.get(id=Id)
        file.delete()
        file.save()

    # @classmethod
    # def get_digest(cls, file):
    #     if isinstance(file, FileBase):
    #         print("变量是文件对象类型")
    #         md5 = hashlib.md5()
    #         sha1 = hashlib.sha1()
    #         sha256 = hashlib.sha256()
    #         for chunk in file.chunks():
    #             md5.update(chunk)
    #             sha1.update(chunk)
    #             sha256.update(chunk)
    #         return {
    #             'md5': md5.hexdigest(),
    #             'sha1': sha1.hexdigest(),
    #             'sha256': sha256.hexdigest()
    #         }
    #     else:
    #         print("变量不是文件对象类型")
    #         # content_bytes = file.encode('utf-8')
    #         md5 = hashlib.md5(file)
    #         sha1 = hashlib.sha1(file)
    #         sha256 = hashlib.sha256(file)
    #
    #     return {
    #         'md5': md5.hexdigest(),
    #         'sha1': sha1.hexdigest(),
    #         'sha256': sha256.hexdigest()
    #     }


"""
LLMAnalysis 用于存放用户上传的文件对应的语言模型推理结果，注意：上传的文件可能存在多个推理结果（对应不同分段），也可能不存在推理结果（二进制文件）。
id: 唯一主键
file_id: File 表外键，注意：该表的增删查改都应该使用其外键 file_id 为主。
section_id: 文件分段以后的序号。section_id 应该从 0 开始，若文件可以被分为两端，则数据库中应该有 section_id = 0, 1 两条记录。
version: 语言模型版本，默认为 0.0.1
result: 存储语言模型的 raw 输出，也即未经处理的输出。
time: 语言模型生成该段输出的时间
start_date: 开始推理的日期
tokenizer: 语言模型使用的 tokenizer 标识，默认。。。
"""


class LLMAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    section_id = models.IntegerField()
    version = models.CharField(max_length=50)
    result = models.TextField()
    time = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    tokenizer = models.CharField(max_length=50)

    @classmethod
    def insert(cls, file_id, section_id, version, result, time, start_date, tokenizer):
        new_line = cls(file_id=file_id, section_id=section_id, version=version, result=result, time=time,
                       tokenizer=tokenizer, start_date=start_date)
        new_line.save()
        return new_line

    @classmethod
    def get_by_fileid(cls, file_id):
        try:
            lines = cls.objects.filter(file_id=file_id)
            return lines
        except cls.DoesNotExist:
            return None

    # TO DO: add time into this function !!!!!!!!!!!!!!!!!!!
    '''
    @classmethod
    def update_by_fileid(cls, file_id, version, results):  # WARNING: careful using this function.
        cls.delete_by_fileid(file_id)
        section_id = 0
        for rslt in results:
            cls.insert(file_id, section_id, version, rslt)
            section_id += 1
        return
    '''

    @classmethod
    def delete_by_fileid(cls, file_id):
        lines = cls.get_by_fileid(file_id)
        for line in lines:
            line.delete()
            line.save()

    @classmethod
    def parse_security_info(cls, info_str):
        info_dict = {}
        lines = info_str.strip().split('\n')
        for line in lines:
            line = re.sub(r'^\d+\.\s*', '', line.strip())  # 可以去除开头的序号
            if line:
                parts = line.split(':')
                if len(parts) == 2:
                    key, value = parts
                    info_dict[key.strip()] = value.strip()
        return info_dict





"""
ClamAnalysis 用于存放用户上传的文件对应的ClamAV推理结果，注意：上传的文件理论上都对应唯一一个ClamAVAnalysis 记录。
id: 唯一主键
file_id: File 表外键，注意：该表的增删查改都应该使用其外键 file_id 为主。
virus_type: 病毒名称
known_viruses: clamAV的病毒库中的病毒
engine_version: ClamAV版本
data_scanned: 扫描的数据大小（以字符串形式存储）
time: 扫描时间
start_date: 开始扫描的日期
 
"""


class ClamAVAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    virus_type = models.TextField()
    is_infected = models.CharField(max_length=50)
    known_viruses = models.CharField(max_length=50)
    engine_version = models.CharField(max_length=50)
    data_scanned = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    start_date = models.DateTimeField()

    @classmethod
    def insert(cls, file_id, virus_type, is_infected, known_viruses, engine_version, data_scanned, time, start_date):
        new_line = cls(
            file_id=file_id,
            virus_type=virus_type,
            known_viruses=known_viruses,
            engine_version=engine_version,
            data_scanned=data_scanned,
            time=time,
            start_date=start_date,
            is_infected=is_infected
        )
        new_line.save()
        return new_line

    @classmethod
    def get_by_fileid(cls, file_id):
        try:
            line = cls.objects.get(file_id=file_id)
            return line
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_by_fileid(cls, file_id, **kwargs):  # WARNING: careful using this function.
        line = None
        try:
            line = cls.objects.get(file_id=file_id)
        except cls.DoesNotExist:
            return None
        for field, value in kwargs.items():
            setattr(line, field, value)
        line.save()
        return line

    @classmethod
    def delete_by_fileid(cls, file_id):
        lines = cls.get_by_fileid(file_id)
        for line in lines:
            line.delete()
            line.save()
