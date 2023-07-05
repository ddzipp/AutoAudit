import json
import tiktoken

encmode = "cl100k_base" # gpt-3.5-turbo
# encmode = "p50k_base"
# encmode = "r50k_base"
encoding = tiktoken.get_encoding(encoding_name=encmode)
# gpt-3.5-turbo
counts_list = []
counts128_list = []
counts256_list = []
counts512_list = []
rest_list = []
file_path = "datasets/data20230703.json"
data_json = None
with open(file_path,"r") as file:
    data_json = json.load(file)

for json_obj in data_json:
    json_str = ""
    for key in json_obj:
        json_str = json_str + key + json_obj[key]
    tokens = encoding.encode(json_str)
    tokens_count = len(tokens)
    counts_list.append(tokens_count)
    if tokens_count <= 128:
        counts128_list.append(tokens_count)
    elif tokens_count <= 256:
        counts256_list.append(tokens_count)
    elif tokens_count <= 512:
        counts512_list.append(tokens_count)
    else:
        rest_list.append(json_obj)
average_count = sum(counts_list)/len(counts_list)
max_count = max(counts_list)

print("encoding mode: ",encmode )
print("average tokens:")
print(average_count)
print("maximum tokens:")
print(max_count)
print("tokens count less than 128:")
print(len(counts128_list))
print("tokens count less than 256:")
print(len(counts256_list))
print("tokens count less than 512:")
print(len(counts512_list))
print("rest:")
print(len(counts_list)-len(counts128_list)-len(counts256_list)-len(counts512_list))

