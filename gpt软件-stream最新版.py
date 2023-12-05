import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import openai
import threading
import json
import pyperclip  # 用于复制文本到剪贴板
import datetime
import pyttsx3

# 设置代理网址
openai.api_base = "https://api.openai-proxy.com/v1"
messages=[]
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

# 默认参数值
default_settings = {
    "selected_model": "gpt-3.5-turbo-1106",
    "system_message": "You are a helpful assistant.",
    "selected_api_key": "",
    "temperature": 0.4,
    "max_tokens": 3600,
    "continuous_chat": 0,
}

# 读取配置文件
def read_settings():
    global selected_model, system_message, selected_api_key, temperature, max_tokens, continuous_chat
    try:
        with open("settings.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            selected_model = data.get("selected_model", default_settings["selected_model"])
            system_message = data.get("system_message", default_settings["system_message"])
            selected_api_key = data.get("selected_api_key", default_settings["selected_api_key"])
            temperature = data.get("temperature", default_settings["temperature"])
            max_tokens = data.get("max_tokens", default_settings["max_tokens"])
            continuous_chat = data.get("continuous_chat", 0)  # 读取连续对话状态，默认为关闭

    except FileNotFoundError:
        with open("settings.txt", "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=4)
            selected_model = default_settings["selected_model"]
            system_message = default_settings["system_message"]
            selected_api_key = default_settings["selected_api_key"]
            temperature = default_settings["temperature"]
            max_tokens = default_settings["max_tokens"]
            continuous_chat = default_settings.get("continuous_chat", 0)

    except Exception as e:
        messagebox.showerror("Error reading settings:", str(e))

# 保存配置文件
def save_settings():
    global selected_model, system_message, selected_api_key, temperature, max_tokens, continuous_chat
    data = {
        "selected_model": selected_model,
        "system_message": system_message,
        "selected_api_key": selected_api_key,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "continuous_chat": continuous_chat  # 保存连续对话状态
    }
    try:
        with open("settings.txt", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error saving settings:", str(e))

# 初始化配置
read_settings()
# 定义一个变量用于保存当前界面状态
simplified_state = False

def toggle_simplified():
    global simplified_state
    if simplified_state:
        # 显示所有界面元素
        model_label.grid(row=1, column=0, sticky="w")
        model_select.grid(row=1, column=1, padx=(0, 10), sticky="ew")
        system_message_label.grid(row=2, column=0, sticky="w")
        system_message_text.grid(row=2, column=1, padx=(0, 10), sticky="ew")
        api_key_label.grid(row=3, column=0, sticky="w")
        api_key_entry.grid(row=3, column=1, padx=(0, 10), sticky="ew")
        show_api_key_check.grid(row=4, columnspan=2, pady=(5, 0), sticky="w")
        temperature_label.grid(row=5, column=0, sticky="w")
        temperature_entry.grid(row=5, column=1, padx=(0, 10), sticky="ew")
        max_tokens_label.grid(row=6, column=0, sticky="w")
        max_tokens_entry.grid(row=6, column=1, padx=(0, 10), sticky="ew")
        continuous_chat_check.grid(row=7, columnspan=2, pady=(5, 0), sticky="w")
        user_input_label.grid(row=8, column=0, sticky="w")
        user_input_text.grid(row=8, column=1, padx=(0, 5), sticky="ew")
        send_button.grid(row=9, column=0, padx=(20, 10), pady=(10, 0), sticky="w")
        clear_button.grid(row=9, column=1, padx=(10, 20), pady=(10, 0), sticky="n")
        simplified_button.grid(row=2, column=0, padx=(10, 15), pady=(10, 0), sticky="n")
        simplified_state = False
    else:
        # 隐藏部分界面元素
        model_label.grid_forget()
        model_select.grid_forget()
        system_message_label.grid_forget()
        system_message_text.grid_forget()
        api_key_label.grid_forget()
        api_key_entry.grid_forget()
        show_api_key_check.grid_forget()
        temperature_label.grid_forget()
        temperature_entry.grid_forget()
        max_tokens_label.grid_forget()
        max_tokens_entry.grid_forget()
        continuous_chat_check.grid_forget()
        simplified_state = True

def get_response_thread():
    global selected_model, system_message, selected_api_key, temperature, max_tokens, continuous_chat
    user_input = user_input_text.get("1.0", "end-1c")
    user_input_text.delete("1.0", tk.END)
    selected_model = model_select.get()
    system_message = system_message_text.get("1.0", "end-1c")
    temperature = float(temperature_entry.get())
    max_tokens = int(max_tokens_entry.get())
    continuous_chat = continuous_chat_var.get()
    response_text_box.config(state=tk.NORMAL)
    response_text_box.insert(tk.END, "\n\n" + "用户: " + user_input + "\n","user")
    response_text_box.tag_configure("user", foreground="blue")
    response_text_box.insert(tk.END,f"{available_models[selected_model]}: ")
    response_text_box.config(state=tk.DISABLED)
    response_text_box.see(tk.END)

    if continuous_chat == 0:
        messages.clear()
        messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": user_input})
    else:
        messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": user_input})

    selected_api_key = api_key_entry.get().strip()
    openai.api_key = selected_api_key

    if len(messages) > 2:
        messages.pop(0)

    response = openai.ChatCompletion.create(
        model=selected_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )

    def update_response_text(response_text):
        response_text_box.config(state=tk.NORMAL)
        response_text_box.insert(tk.END, response_text)
        response_text_box.config(state=tk.DISABLED)
        response_text_box.see(tk.END)
        response_text_box.yview_moveto(1.0)
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']
        if chunk_message != "":
            try:
                content = chunk_message["content"]
                for line in content.split("\n"):
                    messages.append({"role": "assistant", "content": line})
                    update_response_text(line)
            except Exception as e:
                pass

def get_response():
    # 使用 threading 创建一个新线程来执行 get_response_thread 函数
    response_thread = threading.Thread(target=get_response_thread)
    response_thread.start()

def clear_history():
    global messages
    messages.clear()
    response_text_box.config(state=tk.NORMAL)
    response_text_box.delete("1.0", tk.END)
    response_text_box.config(state=tk.DISABLED)
    user_input_text.delete("1.0", tk.END)

def set_api_key_show_state():
    global selected_api_key
    show = show_api_key_var.get()
    if show:
        api_key_entry.config(show="")
    else:
        api_key_entry.config(show="*")
    selected_api_key = api_key_entry.get().strip()

def copy_text_to_clipboard(text):
    pyperclip.copy(text)


# 创建tkinter窗口
root = tk.Tk()
root.title("FREE ChatGPT-----Stream-----MADE-----BY-----中北锋哥-----2023.12.05")

# 主题和风格
style = ttk.Style()
style.theme_use("alt")
style.configure("TFrame", background="lightblue")
style.configure("TButton", padding=2, relief="flat", foreground="black", background="lightblue")
style.configure("TLabel", padding=1, foreground="black", background="lightblue", font=("Arial", 11))
style.configure("TEntry", padding=1, foreground="black", insertcolor="lightblue")
style.configure("TCheckbutton", padding=5, font=("Helvetica", 11), background="lightblue", foreground="blue")

# 创建界面元素
frame_left = ttk.Frame(root)
frame_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
frame_right = ttk.Frame(root)
frame_right.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# 设置权重，使得窗口大小变化时元素可以调整
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# 设置frame_left的权重，使得元素可以水平拉伸
frame_left.grid_columnconfigure(1, weight=1)

# 设置frame_right的权重，使得元素可以水平和垂直拉伸
frame_right.grid_columnconfigure(0, weight=1)
frame_right.grid_rowconfigure(1, weight=1)

model_label = ttk.Label(frame_left, text="选择GPT模型：")
model_label.grid(row=1, column=0, sticky="w")

model_select = ttk.Combobox(frame_left, values=list(available_models.keys()), state="readonly", font=("黑体", 11))
model_select.set(selected_model)
model_select.grid(row=1, column=1, padx=(0, 5), sticky="ew")

system_message_label = ttk.Label(frame_left, text="系统角色：")
system_message_label.grid(row=2, column=0, sticky="w")

system_message_text = scrolledtext.ScrolledText(frame_left, width=45, height=3, font=("黑体", 12))
system_message_text.insert(tk.END, system_message)
system_message_text.grid(row=2, column=1, padx=(0, 5), sticky="ew")

api_key_label = ttk.Label(frame_left, text="API 密钥：")
api_key_label.grid(row=3, column=0, sticky="w")

api_key_entry = ttk.Entry(frame_left, width=50, show="*", font=("Arial", 11))
api_key_entry.insert(0, selected_api_key)
api_key_entry.grid(row=3, column=1, padx=(0, 5), sticky="ew")

show_api_key_var = tk.IntVar()
show_api_key_check = ttk.Checkbutton(frame_left, text="显示 API Key", variable=show_api_key_var, command=set_api_key_show_state)
show_api_key_check.grid(row=4, columnspan=2, pady=(5, 0), sticky="w")

temperature_label = ttk.Label(frame_left, text="Temperature：")
temperature_label.grid(row=5, column=0, sticky="w")

temperature_entry = ttk.Entry(frame_left, width=45, font=("Arial", 11))
temperature_entry.insert(0, temperature)
temperature_entry.grid(row=5, column=1, padx=(0, 5), sticky="ew")

max_tokens_label = ttk.Label(frame_left, text="Max-Tokens：")
max_tokens_label.grid(row=6, column=0, sticky="w")

max_tokens_entry = ttk.Entry(frame_left, width=45, font=("Arial", 11))
max_tokens_entry.insert(0, max_tokens)
max_tokens_entry.grid(row=6, column=1, padx=(0, 5), sticky="ew")

continuous_chat_var = tk.IntVar()
continuous_chat_var.set(continuous_chat)
continuous_chat_check = ttk.Checkbutton(frame_left, text="开启连续对话", variable=continuous_chat_var)
continuous_chat_check.grid(row=7, columnspan=2, pady=(5, 0), sticky="w")

user_input_label = ttk.Label(frame_left, text="用户输入框：")
user_input_label.grid(row=8, column=0, sticky="w")

# 用户输入框设置为自适应宽度
user_input_text = scrolledtext.ScrolledText(frame_left, height=11,width=40,font=("宋体", 11))
user_input_text.grid(row=8, column=1, padx=(0, 5), sticky="ew")
user_input_text.grid_columnconfigure(1, weight=1)  # 设置输入框列的权重

response_label = ttk.Label(frame_right, text="对话消息记录框：")
response_label.grid(row=0, column=0, columnspan=2, sticky="w")

response_text_box = scrolledtext.ScrolledText(frame_right, height=25, width=50, state=tk.DISABLED,font=("宋体", 11))
response_text_box.grid(row=1, column=0, columnspan=2, sticky="nsew")
response_text_box.grid_columnconfigure(1, weight=1)  # 设置输入框列的权重

# 发送按钮设置为自适应宽度
send_button = ttk.Button(frame_left, text="发送用户消息", command=get_response,width=15)
send_button.grid(row=9, column=0, padx=(20, 10), pady=(10, 0), sticky="ew")

clear_button = ttk.Button(frame_left, text="清空对话历史", command=clear_history, width=15)
clear_button.grid(row=9, column=1, padx=(10, 20), pady=(10, 0), sticky="n")

simplified_button = ttk.Button(frame_right, text="显示/隐藏参数", command=toggle_simplified, width=15)
simplified_button.grid(row=2, column=0, padx=(10, 15), pady=(10, 0), sticky="n")
def on_enter_key(event):
    get_response()

# 在user_input_text上绑定Enter键事件
user_input_text.bind("<Return>", on_enter_key)

def copy_user_message():
    response_text = response_text_box.get("end-2l linestart", "end-1c")
    if response_text.strip() != "":
        user_input = response_text.strip().split("\n")[0].replace("用户: ", "")
        copy_text_to_clipboard(user_input)

def copy_assistant_message():
    response_text = response_text_box.get("end-2l linestart", "end-1c")
    if response_text.strip() != "":
        assistant_message = response_text.strip().split("\n")[1].replace(f"{available_models[selected_model]}: ", "")
        copy_text_to_clipboard(assistant_message)
def save_chat_history():
    chat_history = response_text_box.get("1.0", "end-1c")
    if chat_history.strip() != "":
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_history_{current_time}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(chat_history)


user_copy_button = ttk.Button(frame_left, text="复制用户消息", command=copy_user_message, width=15)
user_copy_button.grid(row=10, column=0, padx=(20, 10), pady=(5, 0), sticky="w")

assistant_copy_button = ttk.Button(frame_left, text="复制GPT消息", command=copy_assistant_message, width=15)

assistant_copy_button.grid(row=10, column=1, padx=(10, 20), pady=(5, 0), sticky="n")

save_history_button = ttk.Button(frame_right, text="保存对话记录", command=save_chat_history, width=15)
save_history_button.grid(row=2, column=1, padx=(10, 15), pady=(10, 0), sticky="n")

def play_user_message():
    def play_audio():
        engine = pyttsx3.init()
        user_message = response_text_box.get("end-2l linestart", "end-1c").strip().split("\n")[0].replace("用户: ", "")
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 1)
        engine.setProperty('pitch', 2)
        engine.say(user_message)
        engine.runAndWait()
        engine.stop()

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
play_button1 = ttk.Button(frame_left, text="播放用户回复", command=play_user_message, width=15)
play_button1.grid(row=11, column=0, padx=(20, 10), pady=(5, 0), sticky="w")

def play_assistant_message():
    def play_audio():
        engine = pyttsx3.init()
        assistant_message = response_text_box.get("end-2l linestart", "end-1c").strip().split("\n")[1].replace(f"{available_models[selected_model]}: ", "")
        engine.setProperty('rate', 222)
        engine.setProperty('volume', 1)
        engine.setProperty('pitch', 5)
        engine.say(assistant_message)
        engine.runAndWait()
        engine.stop()

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
play_button2 = ttk.Button(frame_left, text="播放GPT回复", command=play_assistant_message, width=15)
play_button2.grid(row=11, column=1, padx=(10, 20), pady=(5, 0), sticky="n")

def on_closing():
    save_settings()
    save_chat_history()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# 运行窗口循环
root.mainloop()
