# AutoAudit-网络安全大模型

[**🇨🇳中文**](./README.md) | [**🌐English**](./README_EN.md) | [**📖文档/Docs**](https://github.com/ddzipp/AutoAudit/wiki) | [**❓提问/Issues**](https://github.com/ddzipp/AutoAudit/issues) | [**💬讨论/Discussions**](https://github.com/ddzipp/AutoAudit/discussions) |

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



# AutoAudit系列模型

- [AutoAudit-7B]()，此版本为demo版，基于[Alpaca-Lora](https://github.com/tloen/alpaca-lora)训练而来，在网络安全的英文领域回答效果尚佳，但暂时不具备上下文关联的功能，需要用更大参数的模型来解决。

- AutoAudit-33B，该版本仍然在内部测试和训练过程中，我们会稍晚些时候放出。

  


## 简介 Brief Introduction

ChatGPT开启了大语言模型发展的新方向，各大互联网巨头纷纷进入赛道。各大高校也加大对LLM的研发应用。在通用大语言模型领域OpenAI的统治地位暂时无可撼动；因此针对特定领域（Specific-Domain）的大语言模型是发展的必然趋势。目前医疗、教育、金融，法律领域已逐渐有了各自的模型，但网络安全领域迟迟没有模型发布。

无独有偶的是，我们发现微软也有类似定位产品——Microsoft Security Copilot，或许将自然语言处理的大语言模型引入到网络安全乃至安全审计领域，是一条可行的路线；

为促进大语言模型在网络安全领域的应用，本项目开源了网络安全大模型AutoAudit，AutoAudit作为专门针对网络安全领域的大语言模型，其目标是为安全审计和网络防御提供强大的自然语言处理能力。它具备分析恶意代码、检测网络攻击、预测安全漏洞等功能，为安全专业人员提供有力的支持。

通过引入AutoAudit这样的网络安全语言模型，我们可以期待在网络安全领域取得更大的突破。它将成为安全专业人员的得力助手，提供准确、快速的分析和预测，帮助应对不断演进的网络威胁。




## 数据 Dataset

我们采用了数据集组织方法Self-Instruct，该方法结合了人工标注和自我生成的数据。数据集主要来自于Github、Kaggle、安全网站、公开的安全漏洞数据集组成，随后经过清洗、数据增强等来构造对话数据。详细的数据集信息见（包括数据集格式以及组织方式）[AutoAudit训练数据](https://github.com/ddzipp/AutoAudit/wiki/About-Dataset)，以下是样例:

```json
{
	"instruction": "Does this statement have any potential XSS security risks?",
	"input": "<noscript id=x tabindex=1 onfocusin=alert(1)></noscript>",
	"output": "1. analysis: The provided XSS statement attempts to inject a script into the HTML page using the <noscript> tag. It sets the 'id' attribute to 'x', the 'tabindex' attribute to '1', and triggers the 'onfocusin' event to execute the 'alert(1)' JavaScript code. This code will display an alert dialog with the value '1'. \n2. risk: The risk associated with this statement is that it allows an attacker to inject arbitrary JavaScript code into the page and potentially manipulate its behavior or steal sensitive information from users. \n3. solution: To mitigate the XSS vulnerability, input validation and output encoding should be implemented. Any user input or untrusted data should be properly sanitized and validated before being rendered in HTML. Additionally, output encoding should be used when displaying dynamic content to ensure that any special characters are properly encoded and cannot be interpreted as code by the browser."
}
```

当前我们训练的模型数据集构成比例为：

![dataset composition](https://github.com/ddzipp/AutoAudit/blob/main/images/dataset%20composition.png)



## 系统示意 Schema

![result1](https://github.com/ddzipp/AutoAudit/blob/main/images/result1.png)

![result2](https://github.com/ddzipp/AutoAudit/blob/main/images/result2.png)

![result3](https://github.com/ddzipp/AutoAudit/blob/main/images/result3.png)

![result4](https://github.com/ddzipp/AutoAudit/blob/main/images/result4.png)



## 未来计划 Planning

1. **强化安全领域的逻辑推理能力**：我们将致力于提升AutoAudit在安全领域的逻辑推理能力。通过加强模型的训练和优化，我们将努力提高其对复杂安全场景的理解和应对能力。这将使AutoAudit能够更好地处理安全事件、威胁分析和漏洞预测等任务，为安全专业人员提供更准确的解决方案。
2. **加强准确性和可信度**：在安全领域，准确性和可信度至关重要。我们将持续优化AutoAudit的回答内容，确保其对安全审计和防御的建议和指导符合行业标准和最佳实践。通过与专业安全机构和专家的合作，我们将不断更新模型的法规、安全标准和威胁情报，以提供更为准确和可信的结果。
3. 广泛探索私有数据模型：我们将积极探索基于私有数据模型的定制化需求。理解企业和组织对安全领域的特定需求，我们将确保数据隐私和安全，并遵守相关的法律和监管要求。
4. 持续研究和技术创新：我们将与相关领域的专家、学术机构和安全社区合作，进行深入的研究和技术创新。通过不断探索前沿技术和方法，我们将提升AutoAudit的性能和功能，使其始终处于安全领域的前沿位置。

通过这些未来改进计划，我们希望不断提升AutoAudit作为安全领域大语言模型的能力和价值，为安全专业人员提供更精确、可信的安全审计解决方案，同时，我们欢迎与您深入讨论合作，以满足您在安全领域的定制化需求。
