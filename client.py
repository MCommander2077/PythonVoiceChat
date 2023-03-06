# -*- coding: utf-8 -*-
# create time    : 2023-02-10 20:27
# author  : MCommander2077
# file    : client.py
# modify time: -

import socket
import sys
import threading
# GUI
import tkinter as tk
import tkinter.messagebox as tkm

import customtkinter as ctk
import pyaudio

# import requests

# official_server = requests.get('http://ds.yetixcn.com:5000/getserverip')
# official_server_ip = official_server.text

app_ip = ''
app_port = ''

app_status_str = ''

mk_status = True


class Window():
    def __init__(self):
        self.window_login()

    def button_login(self, *args):
        global app_ip, app_port
        if self.ip_Port.get() == '':
            app_ip = str(socket.gethostbyname("ds.yetixcn.com"))
            app_port = 9809
        else:
            ip_port = self.ip_Port.get()
            try:
                app_ip, app_port = ip_port.split(':')
            except:
                try:
                    app_ip, app_port = ip_port.split('：')
                except BaseException as error:
                    tkm.showerror("参数传递错误！",message=f"错误码：\n{error}")
        app_port = int(app_port)
        Client().connect_server()
        self.app_login.destroy()
        self.window_mainapp()

    def window_login(self):
        self.app_login = ctk.CTk()
        self.app_login.title('语音聊天')
        self.app_login.geometry('400x200')
        # 按钮
        btn_frame = ctk.CTkFrame(self.app_login, width=480, height=20)
        btn_frame.grid(row=2, column=0, sticky='E')
        # self.app_login.bind('<\>', self.MikeChange)
        self.ip_Port = tk.StringVar()
        self.ip_Port.set('127.0.0.1:9808')  # f'{official_server_ip}:9808'

        label1 = ctk.CTkLabel(self.app_login, text='不填写默认链接官方服务器')
        label1.place(x=0, y=0, width=400, height=40)

        # 服务器标签
        labelIP = ctk.CTkLabel(self.app_login, text='地址:端口')
        labelIP.place(x=0, y=70, width=120, height=40)

        entryIP = ctk.CTkEntry(self.app_login, width=80,
                               textvariable=self.ip_Port)
        entryIP.place(x=120, y=70, width=260, height=40)
        self.app_login.bind(
            '<Return>', self.button_login)            # 回车绑定登录功能
        but = ctk.CTkButton(self.app_login, text='登录',
                            command=self.button_login)
        but.place(x=10, y=150, width=70, height=30)
        # 创建多行文本框, 显示在线用户
        # listbox1 = tk.Listbox(self.app_login)
        # listbox1.place(x=0, y=0, width=130, height=320)
        self.app_login.mainloop()

    def window_mainapp(self):
        self.app_main = ctk.CTk()
        self.app_main.title('语音聊天')
        self.app_main.geometry('400x400')

        # 创建Frame以供Button1
        btn_frame = ctk.CTkFrame(self.app_main, width=480, height=80)
        btn_frame.grid(row=2, column=0, sticky='E')
        # 按钮
        button_disconnect = ctk.CTkButton(
            btn_frame, text='断开链接', command=self.Disconnect)
        button_disconnect.place(x=100, y=10, width=200, height=60)
        # self.app_main.bind('<\>', self.Disconnect)

        # 创建Frame以供Button2
        btn_frame = ctk.CTkFrame(self.app_main, width=480, height=80)
        btn_frame.grid(row=2, column=0, sticky='E')
        # 按钮
        button_disconnect = ctk.CTkButton(
            btn_frame, text='按"\"键开关麦', command=self.Disconnect)
        button_disconnect.place(x=100, y=70, width=200, height=60)

        '''# 创建Frame以供Button3
        btn_frame = ctk.CTkFrame(self.app_main, width=480, height=80)
        btn_frame.grid(row=2, column=0, sticky='E')
        # 按钮
        button_disconnect = ctk.CTkButton(
            btn_frame, text='断开链接', command=self.Disconnect)
        button_disconnect.place(x=100, y=10, width=200, height=60)'''

        labelStatus = ctk.CTkLabel(self.app_main, text='')
        labelStatus.place(x=0, y=110, width=120, height=40)
        self.app_status = (f'114514')
        labelStatus.configure(text=self.app_status)

        # 创建多行文本框, 显示在线用户
        # listbox1 = tk.Listbox(self.app_login)
        # listbox1.place(x=0, y=0, width=130, height=320)
        self.app_main.mainloop()
        self.Disconnect()

    def Disconnect(self, *args):
        Client().disconnect()
        self.app_main.destroy()

    def set_app_status(self, status):
        exec(f"self.app_status = (f'{status}')")


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_close = False

    def connect_server(self):
        global app_ip, app_port
        while 1:
            try:
                self.target_ip = app_ip
                self.target_port = app_port
                self.s.connect((self.target_ip, self.target_port))

                break
            except BaseException as error:
                tkm.showerror(
                    "错误", message=f"程序发生错误\n错误码:{error}")
                self.disconnect()
                sys.exit(error)

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                            frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        # start threads
        self.receive_thread = threading.Thread(
            target=self.receive_server_data).start()
        self.send_thread = threading.Thread(
            target=self.send_data_to_server).start()

        tkm.showinfo("提示", message=f"已连接到服务器")

    def disconnect(self):
        self.connect_close = True
        self.s.close()
        sys.exit(0)

    def change_mk_status(self):
        if mk_status == True:
            mk_status = False
        else:
            mk_status = True

    def receive_server_data(self):
        while True:
            if self.connect_close == True:
                break
            try:
                receive_data = self.s.recv(1024)
                self.playing_stream.write(receive_data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            if self.connect_close == True:
                break
            try:
                if mk_status == True:
                    data = self.recording_stream.read(1024)
                    self.s.sendall(data)
                else:
                    pass
            except:
                pass


if __name__ == '__main__':
    client = Client()
    window = Window()
