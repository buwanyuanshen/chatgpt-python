# OpenAI-ChatGPT智能聊天机器人

这是一个使用OpenAI的GPT-3.5 Turbo或GPT-4模型创建的智能聊天机器人应用。它允许用户与ChatGPT进行对话并获取回复。

## 功能

- 用户可以输入问题或内容，并选择模型以获取AI的回复。
- 用户可以选择GPT-3.5 Turbo或GPT-4作为聊天模型。
- 用户可以自定义系统角色和温度参数来影响回复的多样性和创意性。

## 如何使用

1. **安装依赖**

    请确保您已经安装了所需的依赖库，可以使用以下命令安装：

    ```bash
    pip install tkinter openai
    ```

2. **设置API密钥**

    在`settings.txt`文件中，设置OpenAI API密钥和系统角色。格式如下：

    ```
    API Key: YOUR_API_KEY
    System Role: You are a helpful assistant.
    ```

3. **运行应用程序**

    运行`main.py`文件，启动应用程序。

    ```bash
    python main.py
    ```

    界面会打开，您可以在输入框中输入问题或内容，然后点击“发送消息”获取AI回复。

## 配置参数

- **API密钥 (`API Key`)**: 在`settings.txt`文件中设置您的OpenAI API密钥。
- **系统角色 (`System Role`)**: 您可以自定义AI的系统角色，影响其回复风格。
- **GPT模型 (`GPT Model`)**: 选择要使用的GPT模型，包括GPT-3.5 Turbo和GPT-4等。
- **温度 (`Temperature`)**: 控制生成文本的创意度，数值越高，生成的文本越多样化。
- **最大 Tokens 数量 (`Max Tokens`)**: 控制AI生成回复的最大token数。

## 贡献

欢迎贡献和改进此项目！如果您想为该项目做贡献，请提交 issue 或者 pull request。


在您的项目中，确保替换`YOUR_API_KEY`为您的实际OpenAI API密钥。同时，您可以根据实际情况对文件结构、配置参数等进行调整和完善。