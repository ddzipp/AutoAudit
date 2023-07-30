# AutoAudit-Cyber Security LLM model

[**🇨🇳中文**](./README.md) | [**🌐English**](./README_EN.md) | [**📖文档/Docs**](https://github.com/ddzipp/AutoAudit/wiki) | [**❓提问/Issues**](https://github.com/ddzipp/AutoAudit/issues)) | [**💬讨论/Discussions**](https://github.com/ddzipp/AutoAudit/discussions) |

```html
<div align="center">
  <a href="https://github.com/ddzipp/AutoAudit">
  <img src="https://github.com/ddzipp/AutoAudit/blob/main/images/logo.png" width="50%">
  </a>
  <p align="center">
      <br/>
      <em>安全 / 审计 / 便捷 </em>
      <br/>
      <a href="https://huggingface.co/lilBuffaloEric/autoaudit_20230703_attempt1"><strong>HuggingFace</strong></a>
    </p>
  </p>
</div>
```

# AutoAudit Series model

- [AutoAudit-7B](), this version is a demo version trained based on [Alpaca-Lora](https://github.com/tloen/alpaca-lora). It performs admirably in the field of network security, yielding satisfactory responses in English. However, it currently lacks contextual understanding and requires a larger parameter model to address this limitation.
- AutoAudit-33B, this version is still undergoing internal testing and training, and it will be released at a later date.

## Brief Introduction

ChatGPT has ushered in a new era of large language model development, with major internet giants actively participating in this endeavor. Prominent universities are also intensifying their efforts in research and application of LLMs. In the realm of general large language models, OpenAI's dominance remains unshaken. Consequently, the trend towards specific-domain LLMs is inevitable. While models tailored for healthcare, education, finance, and law have gradually emerged, the domain of network security has thus far lacked such a model.

Coincidentally, we discovered that Microsoft has a similar offering, the "Microsoft Security Copilot." This suggests that incorporating natural language processing LLMs into the field of network security, even security auditing, is a viable path.

To facilitate the application of large language models in the domain of network security, we have open-sourced the network security model "AutoAudit." Specifically designed for network security, AutoAudit aims to provide robust natural language processing capabilities for security auditing and network defense. Its functionalities include analyzing malicious code, detecting network attacks, and predicting security vulnerabilities, offering valuable support to security professionals.

By introducing network security language models like AutoAudit, we can anticipate significant breakthroughs in the field of network security. It will serve as an indispensable aide to security professionals, furnishing accurate and rapid analysis and predictions to combat evolving cyber threats.

## Dataset

We have adopted the dataset organization method "Self-Instruct," which combines human annotation and self-generated data. The dataset is primarily sourced from Github, Kaggle, security websites, and publicly available security vulnerability datasets. Subsequently, it undergoes cleansing and data augmentation to construct dialogue data. Detailed information about the dataset, including its format and organization, can be found at [AutoAudit Training Data](https://github.com/ddzipp/AutoAudit/wiki/About-Dataset). Below is an example:

```json
{
	"instruction": "Does this statement have any potential XSS security risks?",
	"input": "<noscript id=x tabindex=1 onfocusin=alert(1)></noscript>",
	"output": "1. analysis: The provided XSS statement attempts to inject a script into the HTML page using the <noscript> tag. It sets the 'id' attribute to 'x', the 'tabindex' attribute to '1', and triggers the 'onfocusin' event to execute the 'alert(1)' JavaScript code. This code will display an alert dialog with the value '1'. \n2. risk: The risk associated with this statement is that it allows an attacker to inject arbitrary JavaScript code into the page and potentially manipulate its behavior or steal sensitive information from users. \n3. solution: To mitigate the XSS vulnerability, input validation and output encoding should be implemented. Any user input or untrusted data should be properly sanitized and validated before being rendered in HTML. Additionally, output encoding should be used when displaying dynamic content to ensure that any special characters are properly encoded and cannot be interpreted as code by the browser."
}
```

Currently, the composition ratio of our training dataset is as follows:

![dataset composition](https://github.com/ddzipp/AutoAudit/blob/main/images/dataset%20composition.png)

## System Schema

![result1](https://github.com/ddzipp/AutoAudit/blob/main/images/result1.png)

![result2](https://github.com/ddzipp/AutoAudit/blob/main/images/result2.png)

![result3](https://github.com/ddzipp/AutoAudit/blob/main/images/result3.png)

![result4](https://github.com/ddzipp/AutoAudit/blob/main/images/result4.png)

## Future Plans

1. **Enhanced Logical Reasoning in the Security Domain**: We are committed to boosting AutoAudit's logical reasoning capabilities in the realm of security. By intensifying model training and optimization, we aim to enhance its understanding and response to complex security scenarios. This will empower AutoAudit to handle tasks such as security incidents, threat analysis, and vulnerability prediction more effectively, providing security professionals with more precise solutions.
2. **Improved Accuracy and Credibility**: In the field of security, accuracy and credibility are of paramount importance. We will continuously optimize AutoAudit's responses to ensure that its recommendations and guidance for security auditing and defense adhere to industry standards and best practices. Through collaboration with professional security institutions and experts, we will continuously update the model with regulations, security standards, and threat intelligence to deliver more accurate and credible results.
3. **Extensive Exploration of Private Data Models**: We will actively explore customized demands based on private data models. Understanding the specific requirements of enterprises and organizations in the security domain, we will ensure data privacy and security, complying with relevant laws and regulatory requirements.
4. **Continuous Research and Technological Innovation**: Collaborating with experts, academic institutions, and the security community, we will engage in in-depth research and technological innovation. By continually exploring cutting-edge technologies and methodologies, we will enhance AutoAudit's performance and functionality, ensuring it remains at the forefront of the security domain.

Through these future improvement plans, we aspire to elevate AutoAudit's capabilities and value as a large language model in the domain of security. It will provide security professionals with more precise and reliable security auditing solutions. Moreover, we welcome in-depth discussions and collaborations with you to meet your customized requirements in the field of security.