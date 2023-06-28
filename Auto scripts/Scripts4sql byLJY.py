import openai
import pandas as pd
import json
from openai import api_key, ChatCompletion

# 设置OpenAI API Key
openai.api_key = "xxxxxxxxx"
openai.proxy = "http://127.0.0.1:7890"


# 创建ChatCompletion对象
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": '''You are a network security expert specializing in SQL injection.'''},
        {"role": "user", "content": '''I will provide you with SQL statements, and your job is to analyze the given statement and assess its risk level.'''},
        {"role": "assistant", "content": '''Certainly! Please provide me with the SQL statement you would like me to 
                                         analyze, and I'll assess its risk level for potential SQL injection vulnerabilities.'''},
        {"role": "user", "content": '''Your output must include (i) Analyzing the SQL statement,  (ii) assessing the 
                                    security risk in labels high and low, (iii) locating the specific element, code,
                                    or line in the statement that may produce the vulnerability. I want you to 
                                    output your answer in .JSON format:I want you to output your answer in .JSON with the following format:
{
  "instruction": "Please analyze whether this statement poses security risks",
  "input": "[here should be the SQL statement I provided to you.]",
  "output": "1.  analysis:[Analyze the SQL statement] \n2. label:[label high or low]\n3. risk:[Locate the specific element, code or line in the statement that produce the vulnerability]\n4. solution: [ short solution for the risk with no longer than one sentence. Do not output when there is no risk]" 
},'''
         },
        {"role": "assistant", "content": '''
{
"instruction": "Please analyze whether this statement poses security risks",
"input": "[here should be the SQL statement I provided to you.]",
"output": "1. analysis: [Analyze the SQL statement] \n2. label: [label high or low]\n3. risk: [Locate the specific element, code or line in the statement that produces the vulnerability]\n4. solution: [short solution for the risk with no longer than one sentence. Do not output when there is no risk]"
} '''},
        {"role": "user", "content": '''SELECT * FROM users WHERE username = 'admin' AND password = 'password123';'''},
    ],
    temperature=0
)

print(response['choices'][0]['message']['content'])
