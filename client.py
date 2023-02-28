# -*- coding: utf-8 -*-
# create time    : 2023-02-10 20:27
# author  : MCommander2077
# file    : client.py
# modify time: -

#GUI
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkm

import socket
import threading
import sys
import pyaudio
import requests

official_server = requests.get('http://ds.yetixcn.com:5000/getserverip')
official_server_ip = official_server.text

app_ip = ''
app_port = ''

app_status_str = ''

class Window():
    def __init__(self):
        self.window_login()

    def button_login(self, *args):
        global app_ip, app_port
        if self.ip_Port.get() == '':
            app_ip = official_server_ip
            app_port = 9809
        else:
            ip_port = self.ip_Port.get()
            app_ip, app_port = ip_port.split(':')
        app_port = int(app_port)
        Client().connect_server()
        self.app_login.destroy()
        self.window_mainapp()

    def window_login(self):
        self.app_login = ctk.CTk()
        self.app_login.title('语音聊天')
        self.app_login.geometry('400x400')
        # 按钮
        btn_frame = ctk.CTkFrame(self.app_login, width=480, height=20)
        btn_frame.grid(row=2, column=0, sticky='E')
        #self.app_login.bind('<\>', self.MikeChange)
        self.ip_Port = tk.StringVar()
        self.ip_Port.set('')  # f'{official_server_ip}:9808'

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
        # 按钮
        btn_frame = ctk.CTkFrame(self.app_main, width=480, height=20)
        btn_frame.grid(row=2, column=0, sticky='E')
        buttom = ctk.CTkButton(
            btn_frame, text='断开链接', command=self.Disconnect)
        buttom.place()
        buttom.grid()
        #self.app_main.bind('<\>', self.Disconnect)

        '''self.app_status = tk.StringVar()
        self.app_status.set(f'')
        labelStatus = ctk.CTkLabel(self.app_main, textvariable = app_status)
        labelStatus.place(x=0, y=70, width=120, height=40)'''
        # 创建多行文本框, 显示在线用户
        # listbox1 = tk.Listbox(self.app_login)
        # listbox1.place(x=0, y=0, width=130, height=320)
        self.app_main.mainloop()

    def Disconnect(self, *args):
        Client().disconnect()
        self.app_main.destroy()


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_close = True

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
        self.s.close()
        self.connect_close = True
        sys.exit(0)

    def receive_server_data(self):
        while True:
            if self.connect_close == True:
                break
            try:
                receive_data = self.s.recv(10240)
                self.playing_stream.write(receive_data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            if self.connect_close == True:
                break
            try:
                send_data = self.recording_stream.read(1024)
                self.s.sendall(send_data)
            except:
                pass


if __name__ == '__main__':
    client = Client()
    window = Window()
