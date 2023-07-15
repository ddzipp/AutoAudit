import os
import re
import json


def remove_newlines(text):
    text1 = text.replace("\n","")	
    return text1.replace("\t", "")


def find_xcodes(script):
    # 移除变量和函数声明
    script = remove_newlines(script)
    # cleaned_script = re.sub(r'\bvar\b|\bfunction\b', '', script)
    pattern = r'(var|let|const)\s+(\w+)\s*=[^;]+;|function\s+(\w+)\s*\([^)]*\)\s*{[^}]*}'
    cleaned_script = re.sub(pattern, '', script)
    # 查找除变量和函数之外的可执行语句段
    statements = re.findall(r'[^{};]+;', cleaned_script)
    return ''.join(statements)


def find_vars(script):
    script = remove_newlines(script)
    variable_declarations = re.findall(r'var\s+([^;]+);', script)
    return ';'.join(variable_declarations)


def find_funcs(script):
    script = remove_newlines(script)
    function_declarations = re.findall(r'function\s+([\w$]+)\s*\([^)]*\)\s*{([^}]+)}', script,
                                       re.MULTILINE | re.DOTALL)
    return '\n'.join([f'function {name}() {{{body}}}' for name, body in function_declarations])
    #return '\n'.join(function_declarations)


def find_scripts(text):
    has_js = False
    if re.search(r'<script\b[^>]*>(.*?)</script>', text, re.DOTALL):
        has_js = True
    return has_js


def count_vars(script):
    var_pattern = r'\bvar\b'
    # 统计变量数量
    var_count = len(re.findall(var_pattern, script))
    return var_count


def count_funcs(script):
    function_pattern = r'\bfunction\b'
    function_count = len(re.findall(function_pattern, script))
    return function_count


def analyze_javascript(script, checkhead=False):
    JSinfo = {
        "hasJS": False,
        "var_count": 0,
        "func_count": 0,
        "vcodes": "",
        "fcodes": "",
        "xcodes": "",
    }

    # 检查文本中是否含有JavaScript脚本
    if find_scripts(script) and checkhead == True:
        # var_count = count_vars(script)
        # function_count = count_funcs(script)
        # executable_statements = find_xcodes(script)
        JSinfo["hasJS"] = True
        JSinfo["var_count"] = count_vars(script)
        JSinfo["func_count"] = count_funcs(script)
        JSinfo["vcodes"] = find_vars(script)
        JSinfo["fcodes"] = find_funcs(script)
        JSinfo["xcodes"] = find_xcodes(script)
    elif checkhead == False:
        JSinfo["hasJS"] = True
        JSinfo["var_count"] = count_vars(script)
        JSinfo["func_count"] = count_funcs(script)
        JSinfo["vcodes"] = find_vars(script)
        JSinfo["fcodes"] = find_funcs(script)
        JSinfo["xcodes"] = find_xcodes(script)

    JS_json = json.dumps(JSinfo, indent=4)

    return JS_json


# 测试示例文本
text = """
var gFz = "husr<lspw~Ul45<gj}n<H}yj!%%%%%";
gFz=aObWPoo(gFz,"z"+"i"+"r",2);
var hwY = "7-'j}n<kPTMQy<!<-,,'nyhinr<Q}ht2nsir";
"TYAmshjOYVDEWZTHdxEPFSKAnxdTanrXepBqZyTwYnNQvfuHGsVszCqiWmTCTJiCjBZYnXEJgbHsdEydTtxrwAgyNtemKBvdHURFXxobibFFEtyXlgTpHzXZvJQVBMAkrjDPuHFLQDwLkMoOMTsAwFTpZXmCLAOjuNIfSWveWoeeuQluEePqmPxNIteuhvSsiMnaoBFRNdKmUDmtFqfLUGmFHflzUgCfvsgqdOnNAtTR";
var RZo = "x4HRDnswi4564H}yj1kPTMQy57kPTMQy5'a";
"hnNsjhykroCqbdUTUNTzoNdKkKgioyaeoZECFkdIRYjMNywGcVwGfkNLFtJCSyLTeFXRtRUDAKNpKMKuaNHpuyhyKyBoRtxsqbazMgkedagCBShkUKqXIZgWjlFHnPALoenyAcslEslTOqdglputjSbpksvrvQZAVOxCPKRvflnuWcUHKivwwFpkBXIXFOTGmUDMeTzsjBZiQMSrnkijLwofOwsUcgcASQkVzKYVUnxIhuHIlbKceutXcPcthENJYChLnGyGapTzsdAgTIzuxgriGgsTVEtxtgjIGJNexEJqLXFHjzUoeIYNjqICLViXVeiGNTqSUDadJIwe";
var MwR = "zirhusr<Jvt[}Qdl4]q_^5<gj}n<HRoTo";
"iyTQXknmmFDrdqssdcXvPKoyxLJmhtPOLVIftHxxIhDnQjYANItDBuhHRupSqWZyPMldUhkKjRuIQMeJEmqXRiCirLOdvqQdTYsYXCQgJzuNKtFVSHJPzYiixNGUMACywdKpteapMsmjLGHlOVbcnTaWtknpZQpfZiMBXGdoQkrEJifCWksGdVtxLcadPykyhLjVfhBcKRztYmAXcbcYyjUAIMtuwDUZbuFOhzOYoHQGXhbVcJeUoqYQnxHqQqkUYeqUuxhKyHXrJfSbtdDEBbyydAGKNwdFquvkUVjnwAuZHnNWuBwTHbyLZqLqASPnLbgHeufrcdnlYdVtqjvVWgCSrok";
var iuK = "JwK!;]^_XYZ[TUVWPQRSLMNOHIJKDEF;7;}~";
"rvRzxbUHTGWgRNSXJgspSjHcyhkNhXwDUYQkAAMZYUvnbLCssVqvXJdPTSKrUbnkGgzGZPXcSiKaWcUWasmqTpRZRdefWwXWCYzovqMapSlxmBFNxDvRkcEnBIuPXDIAJrvsJNlfijttqWfhiaNorIvgLiDnAxjweyVEGvvEpdstuGhaTWARuEEFopglSZsXiVcvEJCWyAwqbwfyzLkzIhwhRQUsdzQmfJUmtVDCUTlZTNdInSWOcYuINKZCtrRSNHvhyxPqIKycJbFMePMlYLzerplyQbIzEkxIwYcLIITiyivrppxIpWTPohAufyOPWhnUCZQhEPpugFBbvbDf";
var MrN = "xyz{tuvwpqrslmnohijkdef;'zsn4j}n<Ji";
"wGNiIuPMETUXSLQntVkXcrBkvjyFtiDoJiRCfikVALlwihMUKrjdjrkhbJZCwUlWiAVNPLKrTLXtFllaQVdhmfmrvregskTLQuVnJTEtsrYqqEgXJjUkkFxchvMeheNjXouPwPyUFQaJmnbYnSzDcuYgivqJQtnzqACMSKhOcyvtyNabgAXLOVShseXUpqsRnKyAvYUFWpnEBtHLoFNBDlVIhMoXxHoekjKAjoRC";
var CbM = "~~s!,'Ji~~s ]q_^'Ji~~s775g]n}Tz7!HR";
"gNkGlIMIuMOQqLxdqHoGqabdVgIIMfMeeJnOpKHmFCljooosNHSCCVCQsIFpNoKKzkruqbJLdBIOqzQgkHgcMLRiZCCOkcIXgRaYqiAipleyvCasKtuXiXGfPpBrqMKshldzKcsDaBbyZwHunreMiDCpuNxvBDxgaTgYBAyBRUYlgyJXrrVGjlfpvTZYieYNIonhhaLlqKQxXCFsKefXWvakfEMqCOUbYjfDYDDEgTNznplaynmOQmOrklMZkcLWrgdRGakFCKsTyGGguBX";
var TKg = "oToJwK2t}n]h4Q}ht2zpssn4Q}ht2n}rxsq";
"qbUjVwpugLsRhlwWhrcRgIBtMtfhMUZsxTolZasnBNLhXZTTNzJHSffdStvvelChgHGpIohbjkhOebtVWJTqdPRVcsYBwHTCLFXAVvDmqCdQYBcJvJozQvdTeHFzZRqBDJFuyTJNOeqhhYKmZcgmTvVNZyWAOmBnrGYKoldLBWjjaNxzpkyGZAfNjMWAglSvzNBOgjADHEHXTeLldEWDdkwhfiaHgBSKfRXTLSUunzapjXynClASQPjnOwdpJclHZdPUMlsGfbJscDGRevIAByWNWVceDJQFQDgstYKKVKnraTQoiLPpmHGafsArRFcfSXBAbzavy";
var APE = "456HRoToJwK2pyr{ht55'anyhinr<]n}Tz'a";
"""

org_directory = "/home/erickali1920/桌面/alpaca/2017"
target_path = "/home/erickali1920/桌面/alpaca/output.json"
files = os.listdir(org_directory)
list_json = []
count = 0

print("processing javascripts...")


for root, dirs, files in os.walk(org_directory):
    for file in files:
        if file.endswith(".js"):  # 只处理 .js 文件
            file_path = os.path.join(root, file)
            with open(file_path, "r") as js_file:
                content = js_file.read()
                # 在这里进行对读取到的 .js 文件的操作
                # 可以打印文件内容或者对其进行解析等
                JS_json = analyze_javascript(content)
                # print(JS_json)                
                list_json.append(JS_json)
                count = count + 1



data_json = json.dumps(list_json,indent=4)
with open(target_path,"w") as file:
    file.write(data_json)
    
print("done with ", count)

'''
{
  "tokens": 1000,
  "funcs": 5,
  "vars": 3,
  "fcodes": ""
  "vcodes": ""
  "xcodes": "console.log('Hello, World!');\nif (x > 0) {\n  doSomething();\n}\n// Rest of the executable code" 
}
'''
