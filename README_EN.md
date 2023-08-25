# AutoAudit-Cyber Security LLM model

[**🇨🇳中文**](./README.md) | [**🌐English**](./README_EN.md) | [**📖文档/Wiki**](https://github.com/ddzipp/AutoAudit/wiki) | [**❓提问/Issues**](https://github.com/ddzipp/AutoAudit/issues) | [**💬讨论/Discussions**](https://github.com/ddzipp/AutoAudit/discussions) 

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

# AutoAudit Series model

- [AutoAudit-7B](), this version is a demo version trained based on [Alpaca-Lora](https://github.com/tloen/alpaca-lora). It performs admirably in the field of network security, yielding satisfactory responses in English. However, it currently lacks contextual understanding and requires a larger parameter model to address this limitation.

- AutoAudit-33B, this version is still undergoing internal testing and training, and it will be released at a later date.

  

## Brief Introduction

ChatGPT has opened up a new direction in the development of large language models, with major internet giants entering the race. Prominent universities are also increasing their efforts in the research and application of LLMs. In the realm of general large language models, OpenAI's dominance remains unshaken. Thus, the development of large language models tailored for specific domains is an inevitable trend. While models have gradually emerged in fields like healthcare, education, finance, and law, the field of network security has been lacking in model releases.

Coincidentally, we've discovered that Microsoft also has a similar targeted product called "Microsoft Security Copilot." Perhaps introducing large language models for natural language processing into the realm of network security, even security auditing, is a feasible path.

To promote the application of large language models in the field of network security, this project has open-sourced the network security grand model "AutoAudit." Specifically designed for the network security domain, AutoAudit aims to provide robust natural language processing capabilities for security auditing and network defense. It has functionalities such as analyzing malicious code, detecting network attacks, and predicting security vulnerabilities, providing strong support for security professionals.

By introducing network security language models like AutoAudit, we can anticipate significant breakthroughs in the field of network security. It will become an invaluable assistant to security professionals, offering accurate and swift analysis and predictions to counter ever-evolving cyber threats.

For interactive convenience and to address practical security auditing scenarios, we have coupled the AutoAudit model with ClamAV to create a security scanning platform (with the frontend inspired by Bootstrap templates). If you wish to directly download the AutoAudit model, you can visit [HuggingFace](https://huggingface.co/lilBuffaloEric/autoaudit_20230703_attempt1) to obtain the weights.



## Model Deployment and Usage

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



## Future Plans

1. **Enhancing Logical Reasoning in the Security Domain with Larger Model Bases**: In the field of network security, particularly in subdomains like malicious code analysis, SQL injection, and XSS analysis, there is a substantial demand for a higher number of input tokens. The current basic model's input is around 500-700 tokens, which is clearly inadequate for our needs. We are currently considering using ChatGLM or LLaMA2 as new foundational models.
2. **Increased Accuracy and Reliability**: In the security domain, accuracy and reliability are paramount. Due to limitations in our team's resources and certain unique challenges, we currently can only use some automated scripts in the `scripts` directory for self-instruct, resulting in limited and time-consuming data samples that might lack professionalism and rigor. Our team faces many challenges in terms of improving and expanding the dataset, which we hope to receive assistance with.
3. **Integration with More Security Scanning Tools** and coupling them with LLM to cover as many security scenarios as possible (we are considering automated vulnerability detection and binary reverse engineering).
4. **Exploring Integration with Langchain**, allowing the LLM model to connect with external data sources.



## Dataset

We have adopted the Self-Instruct dataset organization method, which combines human annotation and self-generated data. The dataset is mainly sourced from Github, Kaggle, security websites, and publicly available security vulnerability datasets. Subsequently, it undergoes cleansing and data augmentation to construct dialogue data. The dataset is strictly organized in the Alpaca model dataset format, divided into three parts: Instruction, Input, and Output. In the output, we specify that the analysis should include detailed information (analysis), security rating (label), security risks (risk), and corresponding solutions (solution). For detailed dataset information (including format and organization), refer to [AutoAudit Training Data](https://github.com/ddzipp/AutoAudit/wiki/About-Dataset). Here are some examples:

| question                                                     | answer                                                       | Subject                |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- |
| Please evaluate whether this statement carries any security vulnerabilities：" or pg_sleep ( TIME ) --" | **1. analysis**: The SQL statement appears to be attempting SQL injection by injecting a sleep command using the 'pg_sleep' function.\n**2. label**: high\n**3. risk**: The given SQL statement poses a high risk of SQL injection. It utilizes the 'pg_sleep' function to attempt a time-based blind SQL injection attack.\n**4. solution**: Implement proper input validation and parameterization to prevent SQL injection attacks. | SQL Analysis           |
| Please analyze whether this Python code snippet poses security risks："import socket\nimport json\nimport os\nimport subprocess\nimport base64\n\nclass Backdoor:\n def **init**(self, ip, port):\n self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n self.connection.connect((ip, port))" | **1. analysis**: The Python code snippet defines a class named 'Backdoor' with an initializer method '**init**'. The class sets up a socket connection to a specified IP address and port.\n**2. label**: Low\n**3. risk**: The given Python code snippet has a low security risk. It mainly establishes a socket connection, which is a common networking operation. However, the actual security risk depends on the implementation details of the class and its usage.\n**4. solution**: Ensure that the 'Backdoor' class and its usage have appropriate security measures in place, such as proper input validation, secure communication protocols, access controls, and error handling, to mitigate potential security risks. | Python Code Analysis   |
| What is the purpose of the Certificate Revocation List (CRL)? | The purpose of the Certificate Revocation List (CRL) is to list the digital certificates revoked by the issuing certificate authority (CA) before their scheduled expiration date, indicating that they should no longer be trusted. | Security Knowledge Q&A |

The current composition of the training dataset is as follows:

![dataset composition](https://github.com/ddzipp/AutoAudit/blob/main/images/dataset%20composition.png)



## System Schema

![result1](https://github.com/ddzipp/AutoAudit/blob/main/images/result1.png)

![result2](https://github.com/ddzipp/AutoAudit/blob/main/images/result2.png)

![result3](https://github.com/ddzipp/AutoAudit/blob/main/images/result3.png)

![result4](https://github.com/ddzipp/AutoAudit/blob/main/images/result4.png)



