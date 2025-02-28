from openai import OpenAI
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time

client = OpenAI(
    api_key="",
    base_url="",
)

system_prompt= """你将作为网络安全领域知识工程师。请依据给定技术材料，提炼材料内容，并按以下规范生成新的提问。请注意：仅需要生成一个规范提问即可。

#### 生成规范

1. **技术聚焦原则**
   - 问题应涵盖特定的攻击方法、技术原理、协议漏洞、加密机制、合规标准或安全防护措施等，尽量具体且深入。

2. **问题类型要求**
   - 确保每个问题都能探讨攻击方式的实施步骤、漏洞的工作原理、协议的安全性分析、加密算法的弱点或防护措施的效果等详细技术要点。

3. **生成控制策略**
   - 仅需要生成一个问题即可，输出内容仅包含问题本身。
   - 禁止列表: 为避免幻觉，禁止生成未经验证的CVE编号、ATT&CK技术ID。
"""

def query(prompt):
    completion = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': "[给定材料]\n " + prompt}],
        )
    message = completion.choices[0].message.content
    print(message)
    return message

def process_content(content, num_threads=10):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        return list(tqdm(executor.map(query, content), total=len(content), desc="Processing"))

df = pd.read_csv("./sampled_primus_seed_new.csv")
content = df['content']
print(len(content))

processed_content = process_content(content, num_threads=20)
df['processed_content'] = processed_content

df.to_csv('processed_data_new.csv', index=False)