



# AutoAudit-LLM for Cybersecurity

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




# AutoAudit Series Model

- [AutoAudit-7B](https://huggingface.co/lilBuffaloEric/autoaudit_20230714_attempt2), this version is a demo version trained based on [Alpaca-Lora](https://github.com/tloen/alpaca-lora). It performs admirably in the field of network security, yielding satisfactory responses in English. However, it currently lacks contextual understanding and requires a larger parameter model to address this limitation.

- [AutoAudit-8B-Instruct](https://huggingface.co/dzip/Llama3_8B_4Cybersecurity), this version is fine-tuned based on [Llama3-8B-instruct](https://github.com/meta-llama/llama3), and its performance in answering cybersecurity-related queries has significantly improved. The model's foundational capabilities have also seen a substantial enhancement compared to AutoAudit-7B.

- AutoAudit-Qwen, due to the limited availability of Chinese cybersecurity corpus, this model is still in the exploration and planning stage.

- More LLMs are coming soon

  


## Brief Introduction

This Projects explores the application of Large Language Models (LLMs) within cybersecurity, driven by the domain’s complexity and critical need for robust defense mechanisms. **Cybersecurity encompasses diverse areas such as operating systems, network protocols, malware analysis, and threat detection**. As cyber threats grow in sophistication and scale, LLMs present a promising avenue to enhance threat detection, analysis, and response through advanced language processing capabilities. Their ability to interpret, generate, and synthesize vast amounts of data positions LLMs as a transformative tool for addressing complex cybersecurity challenges.

Compared to traditional methods, LLMs can be fine-tuned to adapt to the ever-changing threat landscape, providing cross-domain knowledge connections and actionable emergency responses. They can also automate repetitive analytical tasks, integrate data from multiple sources, and generate risk assessments that capture subtle threats, thereby improving the adaptability and resilience of security systems. Therefore, LLMs play a crucial role in strengthening cybersecurity defense frameworks, offering experts enhanced support and enabling more comprehensive and flexible protection.

For interactive convenience and to address practical security auditing scenarios, we have coupled the AutoAudit model with ClamAV to create a security scanning platform (with the frontend inspired by Bootstrap templates). If you wish to directly download the AutoAudit model, you can visit HuggingFace to obtain the weights.



## Agent Deployment and Usage

### Environment Setup

1. Download the contents of this repository to your local or remote server:

   ```
   git clone git@github.com:ddzipp/AutoAudit.git
   cd AutoAudit
   ```

2. Create a Conda environment:

   ```
   conda create --name AutoAudit python=3.8
   conda activate AutoAudit
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Install ClamAV and add ClamAV to the environment path.

5. Set the paths for the llama model and Lora weights in the sandbox:

   ```
   sandbox/yahma/llama-7b-hf 
   sandbox/lilBuffaloEirc/autoaudit_20230703_attempt2
   ```

6. Run the following command to start the project:

   ```
   python manage.py runserver
   ```



## Dataset

We have adopted the Self-Instruct dataset organization method, which combines human annotation and self-generated data. The dataset is mainly sourced from Github, Kaggle, security websites, and publicly available security vulnerability datasets. Subsequently, it undergoes cleansing and data augmentation to construct dialogue data. The dataset is strictly organized in the Alpaca model dataset format, divided into three parts: Instruction, Input, and Output. In the output, we specify that the analysis should include detailed information (analysis), security rating (label), security risks (risk), and corresponding solutions (solution). For detailed dataset information (including format and organization), refer to [AutoAudit Training Data](https://github.com/ddzipp/AutoAudit/wiki/About-Dataset). Here are some examples:

| question                                                     | answer                                                       | Subject                |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- |
| Please evaluate whether this statement carries any security vulnerabilities：" or pg_sleep ( TIME ) --" | **1. analysis**: The SQL statement appears to be attempting SQL injection by injecting a sleep command using the 'pg_sleep' function.\n**2. label**: high\n**3. risk**: The given SQL statement poses a high risk of SQL injection. It utilizes the 'pg_sleep' function to attempt a time-based blind SQL injection attack.\n**4. solution**: Implement proper input validation and parameterization to prevent SQL injection attacks. | SQL Analysis           |
| Please analyze whether this Python code snippet poses security risks："import socket\nimport json\nimport os\nimport subprocess\nimport base64\n\nclass Backdoor:\n def **init**(self, ip, port):\n self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n self.connection.connect((ip, port))" | **1. analysis**: The Python code snippet defines a class named 'Backdoor' with an initializer method '**init**'. The class sets up a socket connection to a specified IP address and port.\n**2. label**: Low\n**3. risk**: The given Python code snippet has a low security risk. It mainly establishes a socket connection, which is a common networking operation. However, the actual security risk depends on the implementation details of the class and its usage.\n**4. solution**: Ensure that the 'Backdoor' class and its usage have appropriate security measures in place, such as proper input validation, secure communication protocols, access controls, and error handling, to mitigate potential security risks. | Python Code Analysis   |
| What is the purpose of the Certificate Revocation List (CRL)? | The purpose of the Certificate Revocation List (CRL) is to list the digital certificates revoked by the issuing certificate authority (CA) before their scheduled expiration date, indicating that they should no longer be trusted. | Security Knowledge Q&A |

The composition of the dataset used for training the current model and their corresponding proportions are as follows:

![dataset composition](https://github.com/ddzipp/AutoAudit/blob/main/images/dataset.png)

To simplify the process of automated dataset generation, we have also updated the [GPT](https://chatgpt.com/g/g-c9tvJtq1z-cybersecurity-dataset-for-llama) in the GPT Store dedicated to generating cybersecurity QA datasets, and the generation results are as follows:

![GPT Store](https://github.com/ddzipp/AutoAudit/blob/main/images/GPT%20store.png)



## Future Plans

1. **Inspired by [CyberPal](https://arxiv.org/abs/2408.09304), we plan to synthesize a high-quality cybersecurity corpus**: This dataset will include open/closed book question answering, yes/no questions, multiple-choice Q&A, and Chain of Thoughts (CoT). We aim to open-source both the dataset and the corresponding code, providing a valuable resource for the cybersecurity research community.
2. **Responding to the current trend of Agents**, we will further integrate security tools such as Nmap, Metasploit, etc., and reference agent frameworks like [MetaGPT](https://github.com/geekan/MetaGPT) to automate cybersecurity operations as much as possible. This will help streamline security tasks and improve operational efficiency.
3. **Evaluating the security of cybersecurity-specific large models**: We plan to assess the potential security risks associated with these models, such as possible jailbreaks or backdoors. This will ensure that the models remain secure and resilient against adversarial threats in real-world applications.



## Acknowledge

I would like to thank my friend [Eric Ma](https://github.com/lilBuffaloEric); working together with him to continuously improve this project has been one of the most meaningful experiences. I also want to express my gratitude to CUHKSZ He Lab, where I have learned so much and solidified my direction for further improvements. Finally, I extend my thanks to every member of the open-source community. Thank you for your support and help. I will try my best to develop my project, I hope you can like it.
