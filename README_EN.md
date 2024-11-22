# AutoAudit-Cyber Security LLM model

[**🇨🇳中文**](./README_EN.md) | [**🌐English**](./README.md) | [**📖文档/Wiki**](https://github.com/ddzipp/AutoAudit/wiki) | [**❓提问/Issues**](https://github.com/ddzipp/AutoAudit/issues) | [**💬讨论/Discussions**](https://github.com/ddzipp/AutoAudit/discussions) 

<div align="center">
  <a href="https://github.com/ddzipp/AutoAudit">
  <img src="https://github.com/ddzipp/AutoAudit/blob/main/images/logo.png" width="50%">
  </a>
  <p align="center">
      <br/>
      <em>Security / Audit / Convenience </em>
      <br/>
      <a href="https://huggingface.co/lilBuffaloEric/autoaudit_20230703_attempt1"><strong>HuggingFace</strong></a>
    </p>
  </p>
</div>

# AutoAudit 系列模型

- [AutoAudit-7B](https://huggingface.co/lilBuffaloEric/autoaudit_20230714_attempt2)：此版本为基于 [Alpaca-Lora](https://github.com/tloen/alpaca-lora) 训练的演示版本。在网络安全领域表现良好，能够提供令人满意的英文回复。但目前缺乏上下文理解能力，需要更大参数量的模型来弥补这一缺陷。

- [AutoAudit-8B-Instruct](https://huggingface.co/dzip/Llama3_8B_4Cybersecurity)：此版本基于 [Llama3-8B-instruct](https://github.com/meta-llama/llama3) 微调，在回答网络安全相关问题方面的性能显著提升。相比 AutoAudit-7B，其基础能力也得到了大幅增强。

- AutoAudit-Qwen：由于中文网络安全语料库的有限性，该模型仍处于探索和规划阶段。

- 更多模型版本即将推出！

  

## 简介

本项目探索了大语言模型（LLMs）在网络安全领域的应用，旨在应对这一领域的复杂性以及对强大防御机制的迫切需求。**网络安全涵盖操作系统、网络协议、恶意软件分析和威胁检测等多个领域**。随着网络威胁的复杂性和规模不断增长，LLMs 通过其先进的语言处理能力，为威胁检测、分析和响应提供了广阔的前景。LLMs 能够解释、生成和综合海量数据，为解决复杂的网络安全挑战提供了变革性工具。

与传统方法相比，LLMs 可通过微调适应不断变化的威胁环境，提供跨领域的知识连接以及可操作的应急响应能力。同时，它们可以自动化重复的分析任务，整合来自多种来源的数据，生成能够捕捉潜在威胁的风险评估，从而提高安全系统的适应性和弹性。因此，LLMs 在强化网络安全防御框架方面发挥着关键作用，为安全专家提供更强大的支持，并实现更全面、更灵活的保护。

为了提升交互便捷性并适配实际的安全审计场景，我们将 AutoAudit 模型与 ClamAV 结合，创建了一个安全扫描平台（前端设计借鉴了 Bootstrap 模板）。如果您希望直接下载 AutoAudit 模型，可以访问 HuggingFace 获取模型权重。



## 检测分析平台部署以及使用

### 环境设置

1. 将此代码库的内容下载到本地或远程服务器：

   ```
   git clone git@github.com:ddzipp/AutoAudit.git
   cd AutoAudit
   ```

2. 创建 Conda 环境：

   ```
   conda create --name AutoAudit python=3.8
   conda activate AutoAudit
   ```

3. 安装依赖：

   ```
   pip install -r requirements.txt
   ```

4. 安装 ClamAV 并将其添加到环境路径中。

5. 在 sandbox 中设置 llama 模型和 Lora 权重的路径：

   ```
   sandbox/yahma/llama-7b-hf 
   sandbox/lilBuffaloEirc/autoaudit_20230703_attempt2
   ```

6. 运行以下命令启动项目：

   ```
   python manage.py runserver
   ```



## Dataset

我们采用了 Self-Instruct 数据集组织方法，结合了人工标注和自生成数据。数据集主要来源于 Github、Kaggle、安全网站以及公开的安全漏洞数据集。随后对数据进行清洗和数据增强，以构建对话数据。数据集严格按照 Alpaca 模型数据集格式进行组织，分为三部分：Instruction、Input 和 Output。在 Output 部分，我们规定分析应包括以下详细信息：**分析（analysis）**、**安全评级（label）**、**安全风险（risk）** 以及 **对应的解决方案（solution）**。有关数据集的详细信息（包括格式和组织方式），请参考 [AutoAudit Training Data](https://github.com/ddzipp/AutoAudit/wiki/About-Dataset)。以下是一些示例：

| question                                                     | answer                                                       | Subject                |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- |
| Please evaluate whether this statement carries any security vulnerabilities：" or pg_sleep ( TIME ) --" | **1. analysis**: The SQL statement appears to be attempting SQL injection by injecting a sleep command using the 'pg_sleep' function.\n**2. label**: high\n**3. risk**: The given SQL statement poses a high risk of SQL injection. It utilizes the 'pg_sleep' function to attempt a time-based blind SQL injection attack.\n**4. solution**: Implement proper input validation and parameterization to prevent SQL injection attacks. | SQL Analysis           |
| Please analyze whether this Python code snippet poses security risks："import socket\nimport json\nimport os\nimport subprocess\nimport base64\n\nclass Backdoor:\n def **init**(self, ip, port):\n self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n self.connection.connect((ip, port))" | **1. analysis**: The Python code snippet defines a class named 'Backdoor' with an initializer method '**init**'. The class sets up a socket connection to a specified IP address and port.\n**2. label**: Low\n**3. risk**: The given Python code snippet has a low security risk. It mainly establishes a socket connection, which is a common networking operation. However, the actual security risk depends on the implementation details of the class and its usage.\n**4. solution**: Ensure that the 'Backdoor' class and its usage have appropriate security measures in place, such as proper input validation, secure communication protocols, access controls, and error handling, to mitigate potential security risks. | Python Code Analysis   |
| What is the purpose of the Certificate Revocation List (CRL)? | The purpose of the Certificate Revocation List (CRL) is to list the digital certificates revoked by the issuing certificate authority (CA) before their scheduled expiration date, indicating that they should no longer be trusted. | Security Knowledge Q&A |

数据集组成以及对应比例如图所示：

![dataset composition](https://github.com/ddzipp/AutoAudit/blob/main/images/dataset%20composition.png)

为了简化自动化数据集生成的流程，我们还在 GPT Store 中更新了专用于生成网络安全问答数据集的 [GPTs](https://chatgpt.com/g/g-c9tvJtq1z-cybersecurity-dataset-for-llama)，其示例如下：

![GPT Store](https://github.com/ddzipp/AutoAudit/blob/main/images/GPT%20store.png)



## 未来计划

1. **受 [CyberPal](https://arxiv.org/abs/2408.09304) 的启发，我们计划合成一个高质量的网络安全语料库**：该数据集将包括开放/封闭式问答、是非题、多选问答以及链式推理（CoT）。我们计划开源数据集及其相关代码，为网络安全研究社区提供宝贵的资源。
2. **响应当前 Agent 的发展趋势**，我们将进一步集成 Nmap、Metasploit 等安全工具，并参考 [MetaGPT](https://github.com/geekan/MetaGPT) 等 Agent 框架，尽可能实现网络安全操作的自动化。这将有助于简化安全任务并提高操作效率。
3. **评估面向网络安全的大模型的安全性**：我们计划分析这些模型可能存在的安全风险，例如潜在的越狱或后门攻击。这将确保模型在真实应用场景中具有安全性和抵抗性。



## 致谢

我要感谢我的朋友 [Eric Ma](https://github.com/lilBuffaloEric)；与他一起不断改进这个项目是我经历过的最有意义的体验之一。同时，我也要感谢 CUHKSZ He Lab，在这里我学到了很多，并确定了进一步改进的方向。最后，我要感谢每一位开源社区的成员。感谢你们的支持和帮助！



