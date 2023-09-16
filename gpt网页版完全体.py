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

@app.route('/')
def index():
    return render_template('index1.html', models=available_models)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('user_input')
    selected_model = request.form.get('selected_model')
    system_message = request.form.get('system_message')
    temperature = float(request.form.get('temperature'))
    max_tokens = int(request.form.get('max_tokens'))

    # 检查用户输入是否为空
    if not user_input:
        return jsonify({'error': '请输入问题或内容，然后再点击发送。'})

    try:
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        generated_text = response.choices[0].message["content"]

        print("用户输入内容：", user_input)
        print("GPT回复内容：", generated_text)
        print("-------------------------------------------")
        return jsonify({'response': generated_text})
    except Exception as e:
        return jsonify({'error': f"发生错误: {str(e)}"})

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)