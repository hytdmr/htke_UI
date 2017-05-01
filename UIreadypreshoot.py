#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-18 15:24:51
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
from UIsyssetting import Systemsetting
from globalvariable import *


class Readypreshoot(SerialHelp):

    def __init__(self, master, canvas):
        self.root = master
        # self.root.iconbitmap('logo.ico')
        # self.root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
        # self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white', cursor='none')  #
        self.canvas = canvas

        self.image = Image.open("./image/readypreshoot.bmp")
        self.im = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(400, 300, image=self.im)
        self.canvas.pack()
        self.parameter_init()

    def start(self):
        # 发送发送主机状态：准备预冲 aa bb cc dd 0f ff 08 60 13 00 00 00 00 00 00
        hostStatus = 'aa bb cc dd 0f ff 08 60 13 00 00 00 00 00 00'
        self.TQueue.put(hostStatus)

        # 更新时间
        self.threadDatetime = threading.Thread(target=self.datetime_update)
        self.threadDatetime.setDaemon(True)
        self.threadDatetime.start()

        # 上一步
        self.butpreimage = ImageTk.PhotoImage(Image.open("./image/but_pre.bmp"))
        self.preButton = ttk.Button(self.canvas, takefocus=False, image=self.butpreimage,  command=self.pre, cursor='none')  #
        self.preButton.place(x=25, y=530)

        # 预冲
        self.butpreshootimage = ImageTk.PhotoImage(Image.open("./image/but_preshoot.bmp"))
        self.preshootButton = ttk.Button(self.canvas, takefocus=False, image=self.butpreshootimage,  command=self.preshooting, cursor='none')  #
        self.preshootButton.place(x=620, y=530)

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

    def pre(self):
        print('Pre...')
        from UIweightCalibrate import Weightcalibrate
        self.preButton.destroy()
        self.preshootButton.destroy()
        uiweightcalibrate = Weightcalibrate(self.root, self.canvas)
        uiweightcalibrate.start()

    def preshooting(self):
        print('Preshoot...')
        from UIpreshoot import Preshoot
        self.preButton.destroy()
        self.preshootButton.destroy()
        preshoot = Preshoot(self.root, self.canvas)
        preshoot.start()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
    canvas = tk.Canvas(root, width=800, height=600, bg='white', cursor='none')
    ui = Readypreshoot(root, canvas)
    ui.start()
    root.mainloop()
