import json
import random

# 同义句列表
synonyms = [
    "Please evaluate if this statement presents any security risks",
    "Please assess whether this statement poses security threats",
    "Please examine whether this statement has any potential security vulnerabilities",
    "Could you assess the potential security hazards associated with this statement?",
    "I would appreciate it if you could evaluate whether this statement presents any security risks.",
    "Can you analyze the security implications of this statement and determine if there are any risks?",
    "Please conduct a security analysis to determine if this statement poses any potential risks.",
    "Kindly provide an analysis of the security risks that may arise from this statement."
]


def replace_instruction(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    for obj in data:
        if "instruction" in obj:
            obj["instruction"] = random.choice(synonyms)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# 示例用法
json_file = 'XSSoutput.json'  # 输入的 JSON 文件路径

print("processing")
replace_instruction(json_file)
print("done.")