import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



def send_prompt(chrome,prompt):
    # 获取输入框、发送按钮的xpath表达式
    textarea = '//textarea[@class="home_chat-input__qM_hd"]'
    submit_button = '//button[@class="button_icon-button__BC_Ca undefined undefined home_chat-input-send__rsJfH clickable button_primary__7a7UW"]'
    # selenium自动发送prompt
    chrome.find_element(By.XPATH, textarea).clear()
    chrome.find_element(By.XPATH, textarea).send_keys(prompt)
    time.sleep(2)
    chrome.find_element(By.XPATH, submit_button).click()
    time.sleep(5)

def send_msg(chrome,msg):
    # 获取输入框、发送按钮的xpath表达式
    textarea='//*[@id="prompt-textarea"]'
    submit_button='//*[@id="__next"]/div[1]/div/div/main/div[3]/form/div/div[1]/button'
    # selenium自动获取输入框的内容，并发送
    chrome.find_element(By.XPATH,textarea).clear()
    chrome.find_element(By.XPATH,textarea).send_keys(msg)
    time.sleep(2)
    chrome.find_element(By.XPATH,submit_button).click()
    time.sleep(15)

def get_msg(file_path):
    data=[]
    with open(file_path,'r',encoding="utf-8") as file:
        for line in file:
            line=line.strip(" ")
            data.append(line)
        return data

def split_text(filename):
    with open(filename, 'r') as file:
        content = file.read()
        parts = content.split('@@@')
        return parts

if __name__=="__main__":
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    browser = webdriver.Chrome(options=options)

    #发送Prompt
#     prompt='''
#     I want you to become a network security expert specializing in XSS injection. I will provide an XSS statement. Your job is to analyze the given XSS statement and provide corresponding strategies for addressing this security vulnerability. Your analysis may include whether there is a risk of XSS injection in the statement, and if there is an attempt to locate a specific statement, provide a corresponding single solution strategy for the risk. Please note that you only need to provide a brief analysis and answer. I hope you can output your answer in JSON format. I hope your output is in this format:
# {
#   "instruction": "Please analyze whether this statement poses XSS security risks"
#   "input": here should be the XSS statement I provided to you.
#   "output": "1.  analysis:(Please analyze what happened to the statement I provided you here)2. risk:(Write the specific security risks associated with this statement here)3. solution: (Please write the corresponding defense strategy here)"
# }
# 下面是我提供给你的XSS语句：
# <style onmouseleave="alert(1)">test</style>
#     '''
#     send_prompt(chrome=browser,prompt=prompt)


    data = get_msg('专业.txt')
    for msg in data:
        send_msg(chrome=browser,msg=msg)
    while True:
        a=1
    chrome.quit()