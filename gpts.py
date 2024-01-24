from flask import Flask, render_template, request, Response, jsonify
import openai
import random
import threading

# 设置代理网址
openai.api_base = "https://api.openai-proxy.com/v1"

# 替换为您自己的OpenAI API密钥列表
api_keys = [
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
    "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",
] 

# 创建Flask应用程序
app = Flask(__name__)
# 定义可供选择的模型
available_models = {
    "gpt-3.5-turbo-1106": "GPT-3.5-Turbo-1106(4096tokens)",
    "gpt-3.5-turbo": "GPT-3.5-Turbo(4096tokens)",
    "gpt-3.5-turbo-16k": "GPT-3.5-Turbo-16k(16385tokens)",
    "gpt-3.5-turbo-0613": "GPT-3.5-Turbo-0613(4096tokens)",
    "gpt-3.5-turbo-16k-0613": "GPT-3.5-Turbo-16k-0613(16385tokens)",
    "gpt-3.5-turbo-0301": "GPT-3.5-Turbo-0301(4096tokens)",
    "gpt-4-1106-preview": "GPT-4-1106-preview(4096tokens,max:128000tokens)",
    "gpt-4-vision-preview": "GPT-4-vision-preview(4096tokens,max:128000tokens)",
    "gpt-4": "GPT-4(8192tokens)",
    "gpt-4-0613": "GPT-4-0613(8192tokens)",
    "gpt-4-32k": "GPT-4-32k(32768tokens)",
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

