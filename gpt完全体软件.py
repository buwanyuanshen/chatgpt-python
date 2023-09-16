import tkinter as tk
from tkinter import messagebox, ttk
import openai
import threading
import time
import os

# 设置代理网址
openai.api_base = "https://api.openai-proxy.com/v1"

# 存储API密钥和系统角色到文件
def save_settings(api_key, system_message):
    with open("settings.txt", "w") as file:
        file.write(f"API Key: {api_key}\n")
        file.write(f"System Role: {system_message}\n")

# 从文件加载API密钥和系统角色
def load_settings():
    api_key = ""
    system_message = "You are a helpful assistant."
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("API Key:"):
                    api_key = line.split(":")[1].strip()
                elif line.startswith("System Role:"):
                    system_message = line.split(":")[1].strip()
    return api_key, system_message

# 初始化API密钥和系统角色
api_key, system_message = load_settings()

def get_response():
    # 获取用户输入
    user_input = user_input_entry.get()
    selected_model = model_var.get()
    system_message = system_message_var.get()
    temperature = float(temperature_var.get())
    max_tokens = int(max_tokens_var.get())

    # 检查用户输入是否为空
    if not user_input:
        messagebox.showerror("Error", "请输入问题或内容，然后再点击发送。")
        return

    # 获取API密钥
    api_key = api_key_entry.get().strip()

    # 存储API密钥和系统角色
    save_settings(api_key, system_message_var.get())

    # 初始化OpenAI
    openai.api_key = api_key

    # 在单独的线程中执行GPT调用
    def call_openai():
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

            # 在对话框中逐个字添加用户输入和AI回复
            conversation_text.config(state="normal")
            for char in f"用户: {user_input}\n":
                conversation_text.insert(tk.END, char, "user")
                conversation_text.update()
                time.sleep(0.02)

            for char in f"{available_models[selected_model]}: {generated_text}\n":
                conversation_text.insert(tk.END, char, "gpt")
                conversation_text.update()
                time.sleep(0.02)

            conversation_text.insert(tk.END, "-" * 50 + "\n")
            conversation_text.see(tk.END)  # 滚动到最底部
            conversation_text.config(state="disabled")

            # 添加复制按钮
            add_copy_button(f"用户: {user_input}\n{available_models[selected_model]}: {generated_text}\n")

            # 清除用户输入框内容
            user_input_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"发生错误: {str(e)}")

    # 创建并启动新线程
    thread = threading.Thread(target=call_openai)
    thread.start()

def copy_text(text):
    root.clipboard_clear()
    root.clipboard_append(text)


def add_copy_button(text):
    copy_button = tk.Button(conversation_frame, text="复制", font=("Arial Bold", 12), bg="#0077c8", fg="white", bd=1,
                            relief=tk.SOLID, command=lambda: copy_text(text))
    copy_button.place(x=460, y=0)

def toggle_api_key_visibility():
    global api_key_entry, api_key_visibility_button

    if api_key_entry['show'] == "":
        api_key_entry.config(show="*")
        api_key_visibility_button.config(text="显示")
    else:
        api_key_entry.config(show="")
        api_key_visibility_button.config(text="隐藏")

def clear_conversation():
    conversation_text.config(state="normal")  # 更改state属性值为"normal"
    conversation_text.delete("1.0", tk.END)
    conversation_text.config(state="disabled")  # 再次更改state属性值为"disabled"


def save_conversation():
    conversation = conversation_text.get("1.0", tk.END).strip()
    if conversation:
        with open("conversation.txt", "w", encoding="utf-8") as file:
            file.write(conversation)
        messagebox.showinfo("提示", "对话已保存到 conversation.txt 文件中。")
    else:
        messagebox.showinfo("提示", "对话为空，无需保存。")

# 创建主窗口
root = tk.Tk()
root.title("OpenAI-ChatGPT智能聊天机器人---Made By---锋哥")
root.geometry("600x720")  # 调整窗口大小

# 更改背景颜色
root.configure(bg="lightblue")

# 添加标题
title_label = tk.Label(root, text="GPT-3.5-turbo/GPT-4", font=("Arial Bold", 20), bg="lightblue", fg="#0077c8")
title_label.pack(pady=20)

# 添加界面元素
api_key_frame = tk.Frame(root, bg="#ffffff")
api_key_frame.pack(pady=20)

api_key_label = tk.Label(api_key_frame, text="API密钥:", font=("Arial Bold", 14), bg="lightblue", fg="#0077c8")
api_key_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

api_key_var = tk.StringVar(value="")
api_key_entry = tk.Entry(api_key_frame, width=51, font=("宋体", 11), bd=2, relief=tk.SOLID, show="*",
                         textvariable=api_key_var)
api_key_entry.grid(row=0, column=1, padx=5, pady=5)

api_key_visibility_button = tk.Button(api_key_frame, text="显示", command=toggle_api_key_visibility,
                                      font=("黑体", 12),
                                      bg="#0077c8", fg="white", bd=2, relief=tk.SOLID)
api_key_visibility_button.grid(row=0, column=2, padx=5, pady=5)

input_frame = tk.Frame(root, bg="#ffffff")
input_frame.pack(pady=20)

user_input_label = tk.Label(input_frame, text="您的问题或内容:", font=("Arial Bold", 14), bg="lightblue", fg="#0077c8")
user_input_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

user_input_entry = tk.Entry(input_frame, width=30, font=("Arial", 14), bd=2, relief=tk.SOLID)
user_input_entry.grid(row=0, column=1, padx=5, pady=5)

system_message_label = tk.Label(input_frame, text="系统角色:", font=("Arial Bold", 14), bg="lightblue", fg="#0077c8")
system_message_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

default_system_message = "You are a helpful assistant."
system_message_var = tk.StringVar(value=default_system_message)
system_message_entry = tk.Entry(input_frame, textvariable=system_message_var, width=30, font=("Arial", 14),
                                bd=2, relief=tk.SOLID)
system_message_entry.grid(row=1, column=1, padx=5, pady=5)

model_label = tk.Label(input_frame, text="选择GPT模型:", font=("Arial Bold", 14), bg="lightblue", fg="#0077c8")
model_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

model_var = tk.StringVar(value="gpt-3.5-turbo-16k")
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
model_dropdown = ttk.Combobox(input_frame, textvariable=model_var, values=list(available_models.keys()),
                              font=("Arial", 12), state="readonly")
model_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

temperature_label = tk.Label(input_frame, text="Temperature (>=0):", font=("Arial Bold", 14), bg="lightblue",
                             fg="#0077c8")
temperature_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

temperature_var = tk.StringVar(value="0.3")
temperature_entry = tk.Entry(input_frame, textvariable=temperature_var, font=("Arial", 14), bd=2, relief=tk.SOLID)
temperature_entry.grid(row=3, column=1, padx=5, pady=5)

max_tokens_label = tk.Label(input_frame, text="最大 Tokens 数量:", font=("Arial Bold", 14), bg="lightblue",
                            fg="#0077c8")
max_tokens_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

max_tokens_var = tk.StringVar(value="3500")
max_tokens_entry = tk.Entry(input_frame, textvariable=max_tokens_var, font=("Arial", 14), bd=2, relief=tk.SOLID)
max_tokens_entry.grid(row=4, column=1, padx=5, pady=5)

button_container = tk.Frame(root)
button_container.pack(pady=5)

send_button = tk.Button(button_container, text="发送消息", command=get_response, font=("Arial Bold", 14), bg="#0077c8",
                        fg="white", padx=5, bd=2, relief=tk.SOLID)
send_button.pack(side=tk.LEFT)

clear_button = tk.Button(button_container, text="清除消息", command=clear_conversation, font=("Arial Bold", 14),
                         bg="#0077c8", fg="white", padx=5, bd=2, relief=tk.SOLID)
clear_button.pack(side=tk.LEFT)

save_button = tk.Button(button_container, text="保存对话", command=save_conversation, font=("Arial Bold", 14),
                        bg="#0077c8", fg="white", padx=5, bd=2, relief=tk.SOLID)
save_button.pack(side=tk.LEFT)

response_frame = tk.LabelFrame(root, text="聊天对话框", font=("Arial Bold", 14), bg="#ffffff", bd=2, relief=tk.SOLID)
response_frame.pack(pady=10)

conversation_frame = tk.Frame(response_frame, bg="#ffffff")
conversation_frame.pack()

# 创建滚动条
scrollbar = tk.Scrollbar(conversation_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 创建对话框
conversation_text = tk.Text(conversation_frame, height=12, width=55, font=("宋体", 13), bd=2, relief=tk.SOLID,
                            state="disabled", yscrollcommand=scrollbar.set)
conversation_text.pack(padx=5, pady=30)

conversation_text.tag_config("user", foreground="red")
conversation_text.tag_config("gpt", foreground="blue")

# 绑定滚动条到对话框
scrollbar.config(command=conversation_text.yview)
# 设置API密钥输入框的初始值
api_key_var.set(api_key)

# 设置系统角色输入框的初始值
system_message_var.set(system_message)

root.mainloop()
