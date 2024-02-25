from flask import Flask, render_template, request, Response, jsonify
import openai
import random
import threading

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
    "gpt-3.5-turbo-0125": "GPT-3.5-Turbo-0125(4096tokens)",
    "gpt-3.5-turbo-1106": "GPT-3.5-Turbo-1106(4096tokens)",
    "gpt-3.5-turbo": "GPT-3.5-Turbo(4096tokens)",
    "gpt-3.5-turbo-16k": "GPT-3.5-Turbo-16k(16385tokens)",
    "gpt-3.5-turbo-0613": "GPT-3.5-Turbo-0613(4096tokens)",
    "gpt-3.5-turbo-16k-0613": "GPT-3.5-Turbo-16k-0613(16385tokens)",
    "gpt-3.5-turbo-0301": "GPT-3.5-Turbo-0301(4096tokens)",
    "gpt-4-turbo-preview": "GPT-4-Turbo-preview(4096tokens,max:128000tokens)",
    "gpt-4-0125-preview": "GPT-4-0125-preview(4096tokens,max:128000tokens)",
    "gpt-4-1106-preview": "GPT-4-1106-preview(4096tokens,max:128000tokens)",
    "gpt-4-vision-preview": "GPT-4-Vision-preview(4096tokens,max:128000tokens)",
    "gpt-4": "GPT-4(8192tokens)",
    "gpt-4-32k": "GPT-4-32k(32768tokens)",
    "gpt-4-0613": "GPT-4-0613(8192tokens)",
    "gpt-4-32k-0613": "GPT-4-32k-0613(32768tokens)",
    "gpt-4-0314": "GPT-4-0314(8192tokens)",
    "gpt-4-32k-0314": "GPT-4-32k-0314(32768tokens)",
}


messages = []
messages_lock = threading.Lock()


@app.route('/')
def index():

    return render_template('g1.html', models=available_models)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    with messages_lock:
        messages.clear()  # 清除所有对话历史
    return jsonify({"message": "对话历史已清除"})
    
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    selected_model = request.json.get('selected_model')
    system_message = request.json.get('system_message')
    temperature = float(request.json.get('temperature'))
    max_tokens = int(request.json.get('max_tokens'))
    continuous_chat = request.json.get('continuous_chat')

    with messages_lock:
        if continuous_chat == "false":
            messages.clear()  # 只有在禁用连续对话时清空消息列表
            messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": user_input})
        else:
            messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": user_input})
        selected_api_key = random.choice(api_keys)
        openai.api_key = selected_api_key.strip()
        if len(messages) > 1:
            messages.pop(0)

    response = openai.ChatCompletion.create(
        model=selected_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )
    collected_messages = []
    # 在你的 get_stream 函数中
    def get_stream(tar_get_response):
        try:
            for chunk in tar_get_response:
                chunk_message = chunk['choices'][0]['delta']
                collected_messages.append(chunk_message)  
                if chunk_message != "":
                    try:
                        content = chunk_message["content"]
                        for line in content.split("\n"):
                            messages.append({"role": "assistant", "content": line})
                            yield line
                        
                    except Exception as e:
                        yield "\n"

        except GeneratorExit:
            return

    return Response(get_stream(response), content_type='text/html')
if __name__ == '__main__':
    app.run('0.0.0.0', 80)

