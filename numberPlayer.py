import tkinter as tk
from fake_useragent import UserAgent
from tkinter import Button, Label, Entry, StringVar, messagebox
import random
import requests
import pygame
import time
import threading
import os

class DigitalPlayer(tk.Tk):
    def __init__(self):
        super().__init__()

        # 主窗口属性
        self.title("数字播放器")
        self.geometry("550x450")
        self.configure(bg='#F7F7F7')

        # 标题标签
        self.label_title = Label(self, text="YoYo 个人专属数字播放器", font=("Helvetica Neue", 24, "bold"), bg='#F7F7F7', fg="#333")
        self.label_title.pack(pady=30)

        # 数字范围标签
        self.label_range = Label(self, text="输入数字范围（如：1 - 100）", bg='#6A8D92', font=("Helvetica Neue", 15))
        self.label_range.pack(pady=10)

        # 数字范围输入框
        self.range_str = StringVar()
        self.entry_range = Entry(self, textvariable=self.range_str, font=("Helvetica Neue", 15), width=15, bd=3, relief=tk.FLAT)
        self.entry_range.pack(pady=10, padx=50)

        # 播放按钮
        self.start_button = Button(self, text="开始播放", font=("Helvetica Neue", 16), command=self.start_play, 
                                  relief=tk.FLAT, bg="#D1D1D6", activebackground="#BDBDC2", fg="#333", pady=10, padx=20, bd=3)
        self.start_button.pack(pady=15)
        self.start_button.bind("<Enter>", self.on_enter_start)
        self.start_button.bind("<Leave>", self.on_leave_start)

        # 退出按钮
        self.exit_button = Button(self, text="退出软件", font=("Helvetica Neue", 16), command=self.exit_app,
                                  relief=tk.FLAT, bg="#D1D1D6", activebackground="#BDBDC2", fg="#333", pady=10, padx=20, bd=3)
        self.exit_button.pack(pady=15)
        self.exit_button.bind("<Enter>", self.on_enter_exit)
        self.exit_button.bind("<Leave>", self.on_leave_exit)

        self.playing = False
        
        # 请求头
        self.ua = UserAgent()
        
        self.remaining_time = 600  # 设置为10分钟，单位为秒
        self.timer_str = tk.StringVar()
        self.timer_str.set('10:00')  # 初始显示10:00
        self.timer_label = tk.Label(self, textvariable=self.timer_str, font=("Helvetica Neue", 24, "bold"), bg='#F7F7F7', fg="#333")
        self.timer_label.pack(pady=20)

    def on_enter_start(self, event):
        self.start_button['background'] = "#BDBDC2"

    def on_leave_start(self, event):
        self.start_button['background'] = "#D1D1D6"

    def on_enter_exit(self, event):
        self.exit_button['background'] = "#BDBDC2"

    def on_leave_exit(self, event):
        self.exit_button['background'] = "#D1D1D6"

    def generate_number(self, min_num, max_num):
        return random.randint(min_num, max_num)
    
    def get_random_user_agent(self):
        return self.ua.random
    
    def update_timer(self):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_str.set(f"{mins:02}:{secs:02}")
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.exit_app()

    def play_sound(self, num):
        headers = {
            "User-Agent": self.get_random_user_agent()
        }
        link = f"http://dict.youdao.com/dictvoice?type=1&audio={num}"
        response = requests.get(link, headers=headers)

        with open("temp_audio.mp3", "wb") as audio_file:
            audio_file.write(response.content)

        pygame.mixer.init()
        pygame.mixer.music.load("temp_audio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        os.remove("temp_audio.mp3")

    def start_play(self):
        if not self.playing:
            range_str = self.range_str.get().strip()
            if '-' not in range_str:
                messagebox.showerror("错误", "请输入有效的数字范围，例如：1-1000")
                return
            min_num, max_num = map(int, range_str.split('-'))
            if min_num >= max_num:
                messagebox.showerror("错误", "最小数字必须小于最大数字")
                return
            self.playing = True
            self.start_button.config(text="播放中…")
            self.thread = threading.Thread(target=self.loop_play, args=(min_num, max_num))
            self.thread.start()
            self.update_timer()

    def loop_play(self, min_num, max_num):
        while self.playing:
            num = self.generate_number(min_num, max_num)
            self.play_sound(num)
            time.sleep(random.uniform(1, 3))

    def exit_app(self):
        self.playing = False
        self.destroy()

app = DigitalPlayer()
app.mainloop()
