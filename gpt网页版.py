import openai
from flask import Flask, render_template, request, session
from gevent import pywsgi

app = Flask(__name__)

class ChatApp:
    def __init__(self):
        self.api_key = None
        self.assistant_message = None
        self.copy_buttons = []
        self.conversation = []
        self.username = "用户"

    def set_api_key_and_assistant_message(self):
        api_key = request.form.get('api_key')
        assistant_message = request.form.get('assistant_message')

        openai.api_key = api_key
        openai.api_base = "https://api.openai-proxy.com/v1"

        self.api_key = api_key
        self.assistant_message = assistant_message

        return "恭喜！设置成功，开始聊天吧！"

    def send_message(self):
        user_input = request.form.get('user_input')
        max_tokens = int(request.form.get('max_tokens'))
        temperature = float(request.form.get('temperature'))

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": f"{self.username}: {user_input}"},
                {"role": "system", "content": f"GPT3.5: {self.assistant_message}"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        ai_response = response.choices[0].message["content"]

        self.conversation.append(f'{self.username}: {user_input}')
        self.conversation.append(f'GPT: {ai_response}')

        return render_template('chat.html', conversation=self.conversation)

    def clear_conversation(self):
        self.conversation = []
        return render_template('chat.html', conversation=self.conversation)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'set_api_key':
            result = app.chat_app.set_api_key_and_assistant_message()
            return render_template('chat.html', result=result)
        elif action == 'send_message':
            return app.chat_app.send_message()
        elif action == 'clear_conversation':
            return app.chat_app.clear_conversation()
            return render_template('chat.html')

if __name__ == "__main__":
    app.chat_app = ChatApp()
    app.run('0.0.0.0', 8080)
   # server = pywsgi.WSGIServer(('0.0.0.0', 8080), app)//二选一
   # server.serve_forever()
