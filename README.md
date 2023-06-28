# 🦙🌲🤏AutoAudit_LLM 数据集

欢迎来到 AutoAudit_LLM 数据集仓库！本仓库旨在存储一个全面的数据集，用于训练和评估网络安全领域的语言模型。同时该数据集还会收录精心编写的Prompt以及自动化脚本——用于帮助从业人员来引入ChatGPT类LLM并进行清洗，分析，生成对应的数据集。

我们并行构建了一个以Alpaca—Lora作为Base model的大语言模型，期望该大语言模型能够解决实际的网络安全审计问题——因此精心组织一个完备而精准的网络安全语料数据集就显得至关重要。

## 简介

AutoAudit_LLM 数据集旨在为网络安全领域的研究人员、开发者和从业者提供一个标准化且多样化的语言样本和提示集合。该数据集涵盖了与网络安全相关的各种主题，包括漏洞评估、渗透测试、安全编码实践、入侵检测、网络协议、威胁分析等等。

通过利用 AutoAudit_LLM 数据集，用户可以训练出能够在网络安全领域生成上下文准确的响应的先进语言模型。

## 更新

- 📣 2023/06/28：上传了批量处理SQL注入的脚本，使用了Openai API完成自动化任务。
- 🛠️ 2023/06/27：开放 [Discussions 讨论区](https://github.com/ddzipp/AutoAudit_LLM_Dataset/discussions)，欢迎朋友们交流探讨、提出意见、分享观点！

## 数据集格式

由于我们使用的是[Alpaca-Lora](https://github.com/tloen/alpaca-lora)作为Base Model，并收集网络安全相关的知识形成对应语料进行训练，因此本数据集符合Alpaca-Lora规定的数据集格式；

下面将展示一个最为简单的实例：

```json
{
	"instruction": "Does this statement have any potential XSS security risks?",
	"input": "<noscript id=x tabindex=1 onfocusin=alert(1)></noscript>",
	"output": "1. analysis: The provided XSS statement attempts to inject a script into the HTML page using the <noscript> tag. It sets the 'id' attribute to 'x', the 'tabindex' attribute to '1', and triggers the 'onfocusin' event to execute the 'alert(1)' JavaScript code. This code will display an alert dialog with the value '1'. \n2. risk: The risk associated with this statement is that it allows an attacker to inject arbitrary JavaScript code into the page and potentially manipulate its behavior or steal sensitive information from users. \n3. solution: To mitigate the XSS vulnerability, input validation and output encoding should be implemented. Any user input or untrusted data should be properly sanitized and validated before being rendered in HTML. Additionally, output encoding should be used when displaying dynamic content to ensure that any special characters are properly encoded and cannot be interpreted as code by the browser."
}
```

## 上传文件规范

为了保持一致性和使用的便利性，我们请求贡献者在向 AutoAudit_LLM 数据集仓库上传文件时遵循以下规范：

1. **文件格式：** 请以常用格式（如纯文本TXT、CSV或JSON）上传数据集以及Prompt文件，具体格式取决于数据集的结构和要求。（由于使用Alpaca模型，我们的数据集将以指定的JSON格式呈现）
2. **命名规范：** 在命名文件时，请使用描述性和有意义的名称，以反映数据集的内容和目的。避免使用泛泛的或模糊的名称，以确保清晰易辨认。具体的文件结构将会在后续说明中给出。
3. **时间规范：**对于数据集中的每个样本，请确保包含一个时间字段，记录数据创建或获取的时间。时间可以使用标准的日期和时间格式，例如 ISO 8601 格式（YYYY-MM-DDTHH:MM:SS）。
4. **文件编码：** 确保所有文件使用统一的字符编码，例如 UTF-8，以确保跨平台的兼容性和文本数据的正确解析。
5. **缺失值处理：** 如果数据集中存在缺失值，请明确指定缺失值的表示方式，并在数据结构描述中说明处理缺失值的方法或约定。

## 数据集工作进度

~~1.SQL注入特化分析~~

~~2.XSS攻击特化分析~~

3.Bash脚本特化分析

4.PHP特化分析

5.高级语言漏洞特化分析

......

## :rainbow:贡献 AutoAudit_LLM数据集

我们欢迎社区的贡献，丰富和扩展 AutoAudit_LLM 数据集。如果您希望做出贡献，请按照以下步骤进行：

1. 将本仓库 Fork 到您自己的 GitHub 帐户中。
2. 为您的更改创建一个新分支：`git checkout -b feature/new-dataset`。
3. 按照上述上传文件规范，将您的数据集文件添加到仓库中。
4. 包括一个 README.md 文件，提供有关数据集的相关信息。
5. 提交您的更改并将分支推送到您 Fork 的仓库。
6. 在本仓库中打开一个 pull 请求，提供有关您贡献的数据集的详细信息。

请注意，所有贡献都需要经过仓库维护者的审查和批准。非常感谢您的合作，让我们共同建立一个为网络安全社区提供全面和有价值资源的项目。

## :rotating_light:注意事项和免责声明

1. **数据集内容：** 本仓库中的数据集（AutoAudit_LLM）可能包含网络安全漏洞和攻击的相关信息。请注意，这些数据仅用于研究和教育目的，并且在实际应用中可能会引起安全风险。
2. **使用风险：** 使用本数据集所带来的任何风险和责任由使用者自行承担。我们强烈建议用户在合适的环境中使用数据集，并遵循适当的安全实践和法律法规。
3. **数据验证：** 虽然我们尽力确保数据集的准确性和质量，但我们无法保证数据集中的所有信息都是完全准确和最新的。用户在使用数据集之前应该自行验证和审查数据的有效性和适用性。
4. **合法合规：** 使用本数据集时，用户应确保其行为符合适用的法律法规，并遵守适用的隐私、数据保护和知识产权规定。我们不对用户使用数据集的违法或滥用行为承担任何责任。
5. **安全注意：** 请用户在使用数据集时采取适当的安全措施，包括但不限于隔离网络环境、匿名化处理数据、避免不必要的系统连接和操作等，以防止意外的安全事件和数据泄露。
6. **贡献免责：** 作为贡献者，请确保你上传的数据符合法律规定，且不包含任何恶意软件、敏感信息或侵犯他人隐私和知识产权的内容。我们对贡献者上传的数据内容不承担任何责任。
7. **免责声明：** 本仓库及其维护者不对因使用数据集导致的任何损失、安全事件或法律纠纷承担责任。

使用本数据集即表示您已阅读、理解并同意上述注意事项和免责声明。

## 许可证

AutoAudit_LLM 数据集采用 [LICENSE] 许可证发布。请查看许可证文件以获取有关数据集使用和分发的更多详细信息。

## 参考链接

本项目参考了多个Github项目或网络安全相关的网站以及数据集，链接如下：

Alpaca-Lora：https://github.com/tloen/alpaca-lora

Standford Alpaca: https://github.com/tatsu-lab/stanford_alpaca

Self-instruct: https://github.com/yizhongw/self-instruct

......(待更新)

## 联系方式

如有任何问题、建议或相关 AutoAudit 数据集的疑问，请联系 [1282459418@qq.com]或 [205913647@qq.com],也欢迎您在讨论区或者Issue中提出疑问。
