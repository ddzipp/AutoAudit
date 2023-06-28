import os
import openai

# 填入你的OPENAI_API_KEY
openai.api_key = "xxxxx"

# 代理设置：如果你在墙内需要使用代理才能调用，支持http代理和socks代理
openai.proxy = "http://127.0.0.1:7890"

prompt = '''I want you to become a network security expert specializing in SQL injection. I will provide you with SQL statements, and your job is to analyze the given statement and assess its risk level. Your output must include (i) Analyzing the SQL statement,  (ii) assessing the security risk in labels high and low, and (iii) locating the specific element, code, or line in the statement that may produce the vulnerability. I want you to output your answer in .JSON with the following format:
{
  "instruction": "Please analyze whether this statement poses security risks",
  "input": "[here should be the SQL statement I provided to you.]",
  "output": "1.  analysis:[Analyze the SQL statement] \n2. label:[label high or low]\n3. risk:[Locate the specific element, code or line in the statement that produce the vulnerability]\n4. solution: [ short solution for the risk with no longer than one sentence. Do not output when there is no risk]" 
},'''

conversation = [{"role": "system", "content": "You are a network security expert"}]

count = 1
while True:
    if count != 1:
        user_input = input()
        conversation.append({"role": "user", "content": user_input})
    else:
        conversation.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 模型.
        messages=conversation
    )

    # conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    print("\n" + response['choices'][0]['message']['content'] + "\n")
    count += 1
