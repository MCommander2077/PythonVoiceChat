# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import tkinter as tk
import customtkinter as ctk
import socket
import threading
import pyaudio


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                self.target_ip = input('IP:')
                self.target_port = int(input('PORT:'))

                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        receive_thread = threading.Thread(
            target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(10240)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass


def send_bottom():


class Window():
    def __init__(self):
        app = ctk.CTk()
        app.title('ChatRoom')
        # 显示消息框
        msg_frame = ctk.CTkFrame(app, width=480, height=300)
        msg_frame.grid(row=0, column=0, padx=6, pady=6)
        msg_frame.grid_propagate(0)  # 固定Frame的大小
        msg_text = tk.Text(msg_frame, bg='white')
        msg_text.grid()
        # msg_text.insert('0.0','hhh')
        # 输入
        input_frame = ctk.CTkFrame(app, width=480, height=100)
        input_frame.grid(row=1, column=0)
        input_frame.grid_propagate(0)
        input_text = tk.Text(input_frame, bg='white')
        input_text.grid()


        # 发送按钮
        btn_frame = ctk.CTkFrame(app, width=480, height=20)
        btn_frame.grid(row=2, column=0, sticky='E')
        button = ctk.CTkButton(btn_frame, text='发送', command=send)
        app.bind('<Return>', send)
        button.grid()

window = Window()
client = Client()

