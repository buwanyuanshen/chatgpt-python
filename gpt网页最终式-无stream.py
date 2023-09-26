from flask import Flask, render_template, request, jsonify
import openai
import random

# 设置代理网址
openai.api_base = "https://api.openai-proxy.com/v1"

# 替换为您自己的OpenAI API密钥列表
api_keys = [
    "",
]

# 创建Flask应用程序
app = Flask(__name__)

# 定义可供选择的模型
available_models = {
    "gpt-3.5-turbo": "GPT-3.5-Turbo(4097tokens)",
    "gpt-3.5-turbo-16k": "GPT-3.5-Turbo-16k(16385tokens)",
    "gpt-3.5-turbo-0613": "GPT-3.5-Turbo-0613(4097tokens)",
    "gpt-3.5-turbo-16k-0613": "GPT-3.5-Turbo-16k-0613(16385tokens)",
    "gpt-3.5-turbo-0301": "GPT-3.5-Turbo-0301(4097tokens)",
    "gpt-4": "GPT-4(8192tokens)",
    "gpt-4-0613": "GPT-4-0613(8192tokens)",
    "gpt-4-32k": "GPT-4-32k(32768tokens)",
    "gpt-4-32k-0613": "GPT-4-32k-0613(32768tokens)",
    "gpt-4-0314": "GPT-4-0314(8192tokens)",
    "gpt-4-32k-0314": "GPT-4-32k-0314(32768tokens)"
}
messages = []

@app.route('/')
def index():
    return render_template('index5.html', models=available_models)

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


        selected_api_key = random.choice(api_keys)
        openai.api_key = selected_api_key.strip()
        print(openai.api_key)
        # 调整消息历史记录的长度
        if len(messages) > 2:
            messages.pop(0)
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        generated_text = response.choices[0].message["content"]

        messages.append({"role": "assistant", "content": generated_text})  # 将助手回复添加到消息中
        print("用户输入内容：", user_input)
        print("GPT回复内容：", generated_text)
        return jsonify({'response': generated_text})
    except Exception as e:
        return jsonify({'error': f"发生错误: {str(e)}"})

if __name__ == '__main__':
    app.run('0.0.0.0', 800)
