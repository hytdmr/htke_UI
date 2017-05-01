#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-18 16:16:49
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import tkinter as tk
from tkinter import ttk
import threading
import random
import sys
import time
from PIL import Image, ImageTk
from dataAnalysis import s
from serialhelp import *
from globalvariable import *


class Treatfinish(SerialHelp):

    def __init__(self, master, canvas):
        self.root = master
        # self.root.iconbitmap('logo.ico')
        # self.root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
        # self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white', cursor='none')  #
        self.canvas = canvas

        self.image = Image.open("./image/treatfinish.bmp")
        self.im = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(400, 300, image=self.im)
        self.canvas.pack()
        self.parameter_init()

    def start(self):
        # 发送发送主机状态：结束治疗 aa bb cc dd 0f ff 08 60 23 00 00 00 00 00 00
        hostStatus = 'aa bb cc dd 0f ff 08 60 23 00 00 00 00 00 00'
        self.TQueue.put(hostStatus)

        # 更新时间
        self.threadDatetime = threading.Thread(target=self.datetime_update)
        self.threadDatetime.setDaemon(True)
        self.threadDatetime.start()

        self.exitButton = ttk.Button(self.canvas, takefocus=False, text='QUIT',  command=self.quit, cursor='none')  #
        self.exitButton.place(x=25, y=530)

    def parameter_init(self):

        # 日期
        self.Date = self.canvas.create_text(X_AXIS_0_1, Y_AXIS_0_1, fill='blue', font=DEFAULT_FONT_NUM)
        # 时间
        self.Time = self.canvas.create_text(X_AXIS_0_1 + X_AXIS_0_1_ADD, Y_AXIS_0_1, fill='blue', font=DEFAULT_FONT_NUM)

    def datetime_update(self):
        # 获取当前日期
        self.currentDate = time.strftime("%y-%m-%d")
        self.currentTime = time.strftime("%H:%M:%S")
        self.canvas.itemconfigure(self.Date, text=self.currentDate)
        self.canvas.itemconfigure(self.Time, text=self.currentTime)

        # threading.Timer线程每隔60s更新时间
        self.timeupdate = threading.Timer(1, self.datetime_update)
        # 守护线程(后台线程)，主程序结束，守护线程无论完成与否都结束
        self.timeupdate.setDaemon(True)
        self.timeupdate.start()

    def quit(self):
        sys.exit()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
    canvas = tk.Canvas(root, width=800, height=600, bg='white', cursor='none')
    ui = Treatfinish(root, canvas)
    ui.start()
    root.mainloop()
