#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-05 13:31:25
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk
from UIselfcheck import Selfcheck
from netgate import NetGate
from serialhelp import *
from globalvariable import *


class Start(SerialHelp):

    def __init__(self, master, canvas):
        self.root = master
        self.canvas = canvas
        self.imageNum = 0
        self.root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
        # self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white', cursor='none')  #

        self.image1 = Image.open("./image/start1.bmp")
        self.im1 = ImageTk.PhotoImage(self.image1)
        self.image2 = Image.open("./image/start2.bmp")
        self.im2 = ImageTk.PhotoImage(self.image2)
        self.image3 = Image.open("./image/start3.bmp")
        self.im3 = ImageTk.PhotoImage(self.image3)
        self.image4 = Image.open("./image/start4.bmp")
        self.im4 = ImageTk.PhotoImage(self.image4)
        self.image5 = Image.open("./image/start5.bmp")
        self.im5 = ImageTk.PhotoImage(self.image5)
        self.canvas.create_image(400, 300, image=self.im1)
        self.canvas.pack()

    def start(self):
        netgate = NetGate()
        if not netgate.netGateFind:
            self.canvas.create_text(X_AXIS_1_1, Y_AXIS_1_1, text='CAN 网关不可用...！', fill='blue', font=DEFAULT_FONT_NUM)
        else:
            '''发送发送主机状态：开机动画 aa bb cc dd 0f ff 08 60 10 00 00 00 00 00 00'''
            hostStatus = 'aa bb cc dd 0f ff 08 60 10 00 00 00 00 00 00'
            self.TQueue.put(hostStatus)
            '''更新开机动画'''
            self.update_image()

    def update_image(self):
        if self.imageNum == 0:
            self.canvas.create_image(400, 300, image=self.im1)
            self.canvas.after(1000)
        if self.imageNum == 1:
            self.canvas.create_image(400, 300, image=self.im2)
            self.canvas.after(1000)
        if self.imageNum == 2:
            self.canvas.create_image(400, 300, image=self.im3)
            self.canvas.after(1000)
        if self.imageNum == 3:
            self.canvas.create_image(400, 300, image=self.im4)
            self.canvas.after(1000)
        if self.imageNum == 4:
            self.canvas.create_image(400, 300, image=self.im5)
            self.canvas.after(1000)
            selfcheck = Selfcheck(self.root, self.canvas)
            selfcheck.start()

        self.imageNum += 1

        self.threadImageUpdate = threading.Timer(0.2, self.update_image)
        self.threadImageUpdate.setDaemon(True)
        self.threadImageUpdate.start()
        if self.imageNum >= 5:
            self.threadImageUpdate.cancel()
            # print(self.threadImageUpdate.is_alive())
            self.imageNum = 0


def main():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=800, height=600, bg='white', cursor='none')
    start = Start(root, canvas)
    start.start()

    root.mainloop()


if __name__ == '__main__':
    main()
