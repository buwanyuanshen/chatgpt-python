# 使用 OpenAI GPT-3.5 Turbo 创建聊天机器人

这是一个使用 OpenAI GPT-3.5 Turbo 模型创建的基于 Flask 的聊天机器人应用程序。它可以与用户进行对话，并通过 OpenAI API 提供智能回复。

## 依赖

在运行应用程序之前，请确保已安装以下依赖项：

- Flask
- openai

您可以使用 pip 命令来安装它们：

```
pip install flask openai
```

## 配置 OpenAI API 密钥

在 `app.py` 文件中，将 `api_key` 变量替换为您自己的 OpenAI API 密钥。您可以从 OpenAI 网站上创建一个新的 API 密钥并将其粘贴到此处。

## 启动应用程序

要启动应用程序，请运行以下命令：

```
python app.py
```

然后在浏览器中访问 `http://localhost:8080`。

## 使用应用程序

启动应用程序后，您将看到一个界面，其中包含一个文本输入框和一个发送按钮。您可以在文本输入框中输入问题或内容，然后点击发送按钮。

应用程序将使用您提供的模型和参数来调用 OpenAI API，获取智能回复，并将其显示在界面上。

## 注意事项

请注意，本应用程序使用了一个开源的 OpenAI 代理网址：`https://api.openai-proxy.com/v1`。如果您想自己部署代理或直接使用 OpenAI API，请相应地更改 `openai.api_base` 和 `openai.api_key`。

此外，请确保遵守 OpenAI 的使用条款和指南，并在应用程序中正确处理 API 调用的限制和错误。