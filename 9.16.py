
from flask import Flask, render_template, request, jsonify
import openai

# 设置代理网址
openai.api_base = "https://api.openai-proxy.com/v1"

# 替换为您自己的OpenAI API密钥
api_key = "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"

# 初始化OpenAI
openai.api_key = api_key

# 创建Flask应用程序
app = Flask(__name__)

# 定义可供选择的模型
available_models = {
    "gpt-3.5-turbo-0301": "GPT-3.5-Turbo-0301",
    "gpt-3.5-turbo-16k": "GPT-3.5-Turbo-16k",
    "gpt-3.5-turbo": "GPT-3.5-Turbo",
    "gpt-3.5-turbo-0613": "GPT-3.5-Turbo-0613",
    "gpt-3.5-turbo-16k-0613": "GPT-3.5-Turbo-16k-0613"
}

messages = []

@app.route('/')
def index():
    return render_template('index4.html', models=available_models)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('user_input')
    selected_model = request.form.get('selected_model')
    system_message = request.form.get('system_message')
    temperature = float(request.form.get('temperature'))
    max_tokens = int(request.form.get('max_tokens'))
    continuous_chat = request.form.get('continuous_chat')  # 获取连续对话参数

    try:
        if continuous_chat == "true" and messages:
            messages.append({"role": "user", "content": user_input})
        else:
            messages.clear()  # 清空消息列表
            messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": user_input})

        # 调整消息历史记录的长度
        if len(messages) > 3:
            messages.pop(0)

        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        collected_chunks = []
        collected_messages = []
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            generated_text = chunk['choices'][0]['delta']  # extract the message
            collected_messages.append(generated_text)
        full_reply_content = ''.join([m.get('content', '') for m in collected_messages])

        messages.append({"role": "assistant", "content": full_reply_content})  # 将助手回复添加到消息中
        print("用户输入内容：", user_input)
        print("GPT回复内容：", full_reply_content)
        return jsonify({'response': full_reply_content})
    except Exception as e:
        return jsonify({'error': f"发生错误: {str(e)}"})

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)