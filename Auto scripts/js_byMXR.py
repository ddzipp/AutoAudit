import re
def remove_newlines(text):
    return text.replace("\n", "")
def count_variables(script):
    var_count = 0
    function_count = 0

    # 查找变量和函数
    var_pattern = r'\bvar\b'
    function_pattern = r'\bfunction\b'

    # 统计变量数量
    var_count = len(re.findall(var_pattern, script))

    # 统计函数数量
    function_count = len(re.findall(function_pattern, script))

    return var_count, function_count

def find_executable_statements(script):
    # 移除变量和函数声明
    script = remove_newlines(script)
    # cleaned_script = re.sub(r'\bvar\b|\bfunction\b', '', script)
    pattern = r'(var|let|const)\s+(\w+)\s*=[^;]+;|function\s+(\w+)\s*\([^)]*\)\s*{[^}]*}'
    cleaned_script = re.sub(pattern, '', script)
    # 查找除变量和函数之外的可执行语句段
    statements = re.findall(r'[^{};]+;', cleaned_script)

    return statements

def find_vars(script):
    variable_declarations = re.findall(r'var\s+([^;]+);', script)
    return '\n'.join(variable_declarations)


def find_funcs(js_code):
    function_declarations = re.findall(r'function\s+([\w$]+)\s*\([^)]*\)\s*{([^}]+)}', js_code, re.MULTILINE | re.DOTALL)
    return '\n'.join([f'function {name}() {{\n{body}\n}}' for name, body in function_declarations])

def analyze_javascript(script):
    has_javascript = False
    var_count, function_count = 0, 0
    executable_statements = []

    # 检查文本中是否含有JavaScript脚本
    if re.search(r'<script\b[^>]*>(.*?)</script>', script, re.DOTALL):
        has_javascript = True
        var_count, function_count = count_variables(script)
        executable_statements = find_executable_statements(script)

    return has_javascript, var_count, function_count, executable_statements


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
has_js, var_count, function_count, exec_statements = analyze_javascript(text)

print("JavaScript存在：" if has_js else "JavaScript不存在")
print("变量数量：", var_count)
print("函数数量：", function_count)
find_vars(script=text)
print("可执行语句段：")
for statement in exec_statements:
    print(statement.strip())
