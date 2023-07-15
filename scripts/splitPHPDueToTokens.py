import tiktoken
import re

def num_tokens_from_messages(messages):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(messages))
    return num_tokens


def count_token(messages):
    return num_tokens_from_messages(messages)


def split_text(text):
    # 切分行
    token_limit = 200
    current_segment = ''
    segments = []

    remove_extra_spaces(text)

    def process_line(each_line):
        nonlocal current_segment
        if count_token(each_line) > token_limit:
            # 当前段加上该行超过 token 数限制，将该行切分为多个部分
            for i in range(0, len(each_line), token_limit):
                segments.append(current_segment + each_line[i:round(i+token_limit*4/3)])
                current_segment = ''
            return
        else:
            current_segment += each_line

            if count_token(current_segment) >= token_limit:
                # 当前段超过 token 数限制，将当前段作为一个部分
                segments.append(current_segment[:-len(each_line)])
                current_segment = each_line


    for line in text.split('\n'):
        process_line(line)

    # 添加最后一个部分
    if current_segment:
        segments.append(current_segment)

    return segments





def remove_extra_spaces(text):
    # 将连续三个以上的空格替换为1个空格
    return re.sub(r'\s{3,}', ' ', text)
