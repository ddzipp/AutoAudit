



# AutoAudit-网络安全大模型

[**🇨🇳中文**](./README.md) | [**🌐English**](./README_EN.md) | [**📖文档/Wiki**](https://github.com/ddzipp/AutoAudit/wiki) | [**❓提问/Issues**](https://github.com/ddzipp/AutoAudit/issues) | [**💬讨论/Discussions**](https://github.com/ddzipp/AutoAudit/discussions) 

<div align="center">
  <a href="https://github.com/ddzipp/AutoAudit">
  <img src="https://github.com/ddzipp/AutoAudit/blob/main/images/logo.png" width="50%">
  </a>
  <p align="center">
      <a href="https://github.com/ddzipp/AutoAudit/graphs/contributors">
        <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/ddzipp/AutoAudit" />
      </a>
      <a href="https://github.com/ddzipp/AutoAudit/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/ddzipp/AutoAudit?color=0088ff" />
      </a>
      <a href="https://github.com/ddzipp/AutoAudit/stargazers">
        <img alt="GitHub stars" src="https://img.shields.io/github/stars/ddzipp/AutoAudit?color=ccf" />
      </a>
      <br/>
      <em>安全 / 审计 / 便捷 </em>
      <br/>
      <a href="https://huggingface.co/lilBuffaloEric/autoaudit_20230703_attempt1"><strong>HuggingFace下载</strong></a>
    </p>
  </p>
</div>




# AutoAudit系列模型

- [AutoAudit-7B]()，此版本为demo版，基于[Alpaca-Lora](https://github.com/tloen/alpaca-lora)训练而来，在网络安全的英文领域回答效果尚佳，但暂时不具备上下文关联的功能，需要用更大参数的模型来解决。

- AutoAudit-33B，该版本仍然在内部测试和训练过程中，我们会稍晚些时候放出。

  


## 简介 Brief Introduction

ChatGPT开启了大语言模型发展的新方向，各大互联网巨头纷纷进入赛道。各大高校也加大对LLM的研发应用。在通用大语言模型领域OpenAI的统治地位暂时无可撼动；因此针对特定领域（Specific-Domain）的大语言模型是发展的必然趋势。目前医疗、教育、金融，法律领域已逐渐有了各自的模型，但网络安全领域迟迟没有模型发布。

无独有偶的是，我们发现微软也有类似定位产品——Microsoft Security Copilot，或许将自然语言处理的大语言模型引入到网络安全乃至安全审计领域，是一条可行的路线；

为促进大语言模型在网络安全领域的应用，本项目开源了网络安全大模型AutoAudit，AutoAudit作为专门针对网络安全领域的大语言模型，其目标是为安全审计和网络防御提供强大的自然语言处理能力。它具备分析恶意代码、检测网络攻击、预测安全漏洞等功能，为安全专业人员提供有力的支持。

通过引入AutoAudit这样的网络安全语言模型，我们可以期待在网络安全领域取得更大的突破。它将成为安全专业人员的得力助手，提供准确、快速的分析和预测，帮助应对不断演进的网络威胁。

为了便于交互，应对实际的安全审核应用场景，我们将AutoAudit模型与ClamAV进行耦合，搭建了一个安全扫描的平台（前端参考了Bootstrap所提供的模板）。如果您想直接下载AutoAudit模型，请访问[HuggingFace](https://huggingface.co/lilBuffaloEric/autoaudit_20230703_attempt1)直接获取权重。



## 模型部署Usage

### 环境安装

1.下载本仓库内容至本地/远程服务器

```
git clone git@github.com:ddzipp/AutoAudit.git
cd AutoAudit
```

2.创建conda环境

```
conda create --name AutoAudit python=3.8
conda activate AutoAudit
```

3.安装依赖

```
pip install -r requirements.txt
```

4.安装ClamAV，并将 clamAV 添加到环境路径中。

5.设置权重路径：我们的项目目前使用 yahma/llama-7b-hf 和 lilBuffaloEirc/autoaudit_20230703_attempt2 作为基本的 llama 模型和 Lora 权重进行增强，这些权重可以从 Hugging Face 上获取。您需要在sandbox中设置 llama 模型和 Lora 权重的路径为：

```
sandbox/yahma/llama-7b-hf 
sandbox/lilBuffaloEirc/autoaudit_20230703_attempt2
```

5.输入下述指令启动项目：

```
python manage.py runserver
```



## 未来计划 Todo

1. **强化安全领域的逻辑推理能力，尝试在更大的模型基座上进行相应的训练**：在网络安全领域，特别是我们所选择的恶意代码分析，SQL注入，以及XSS分析等细分场景下，对于模型的输入Token有着较大的要求，目前的初级模型输入大约为500-700Token，显然无法达到我们的需求。目前正在考虑使用ChatGLM或者LLaMA2作为新的基底模型。

2. **加强准确性和可信度**：在安全领域，准确性和可信度至关重要。由于我们的团队资金限制以及某些特殊原因，我们暂时还只能使用scripts目录下的部分自动化脚本进行Self-instruct，生成的数据样本实在有限且耗费时间，同时也可能缺乏专业性和严谨性。目前团队对于改进，扩大数据集还有很多问题亟需解决，希望能够得到帮助。

3. **接入更多的安全扫描工具**，并且与LLM进行耦合，尽可能覆盖更多的安全场景（正在考虑自动化漏洞挖掘以及二进制逆向分析）。

4. **尝试接入Langchain**，允许LLM模型与外界数据源进行连接。

   


## 数据集 Dataset

我们采用了数据集组织方法Self-Instruct，该方法结合了人工标注和自我生成的数据。数据集主要来自于Github、Kaggle、安全网站、公开的安全漏洞数据集组成，随后经过清洗、数据增强等来构造对话数据。数据集严格按照Alpaca模型数据集格式组织，分为Instruction，input，output三部分，我们规定在output输出中应当包含对具体内容的分析（analysis），安全评级（label），安全风险（risk），以及对应的解决方案（solution）。详细的数据集信息（包括数据集格式以及组织方式）见[AutoAudit训练数据](https://github.com/ddzipp/AutoAudit/wiki/About-Dataset)，以下是场景样例:

| question                                                     | answer                                                       | Subject                |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- |
| Please evaluate whether this statement carries any security vulnerabilities："" or pg_sleep ( TIME ) --" | **1. analysis**: The SQL statement appears to be attempting SQL injection by injecting a sleep command using the 'pg_sleep' function.\n**2. label**: high\n**3. risk**: The specific element that produces the vulnerability is the injection of the 'pg_sleep' function within the statement.\n**4. solution**: Implement proper input validation and parameterization to prevent SQL injection attacks. | SQL分析        |
| Please analyze whether this Python code snippet poses security risks：“import socket\nimport json\nimport os\nimport subprocess\nimport base64\n\nclass Backdoor:\n    def __init__(self, ip, port):\n        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n        self.connection.connect((ip, port))" | **1.  analysis**: The Python code snippet defines a class named 'Backdoor' with an initializer method '__init__'. The class sets up a socket connection to a specified IP address and port.\n**2. label**: Low\n**3. risk**: The given Python code snippet has a low security risk. It mainly establishes a socket connection, which is a common networking operation. However, the actual security risk depends on the implementation details of the class and its usage.\n**4. solution**: Ensure that the 'Backdoor' class and its usage have appropriate security measures in place, such as proper input validation, secure communication protocols, access controls, and error handling, to mitigate potential security risks. | Python代码分析 |
| What is the purpose of the Certificate Revocation List (CRL)? | The purpose of the Certificate Revocation List (CRL) is to list the digital certificates revoked by the issuing certificate authority (CA) before their scheduled expiration date, indicating that they should no longer be trusted. | 安全知识问答   |

当前我们训练的模型数据集构成比例为：

![dataset composition](https://github.com/ddzipp/AutoAudit/blob/main/images/dataset%20composition.png)

为简化自动化数据集生成过程，我们也在GPT Store更新了专用于生成以LLaMA(Alpaca)为Base model的网络安全QA数据集的[GPT](https://chatgpt.com/g/g-c9tvJtq1z-cybersecurity-dataset-for-llama)，生成效果如下：

![GPT Store](https://github.com/ddzipp/AutoAudit/blob/main/images/GPT%20store.png)

## 系统示意 Schema

![result1](https://github.com/ddzipp/AutoAudit/blob/main/images/result1.png)

![result2](https://github.com/ddzipp/AutoAudit/blob/main/images/result2.png)

![result3](https://github.com/ddzipp/AutoAudit/blob/main/images/result3.png)

![result4](https://github.com/ddzipp/AutoAudit/blob/main/images/result4.png)



