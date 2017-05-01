#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-07 09:34:45
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import tkinter as tk
from tkinter import ttk
import threading
import random
import time
from PIL import Image, ImageTk
from dataAnalysis import s
from serialhelp import *
from UImaintance import Maintance
from UIweightCalibrate import Weightcalibrate
import inspect
import ctypes
from globalvariable import *


NEXT = False
FIRST = True

X_AXIS_0_1 = 628
X_AXIS_0_1_ADD = 100
Y_AXIS_0_1 = 27


X_AXIS_1_1 = 160
Y_AXIS_1_1 = 122
Y_AXIS_1_1_ADD = 80
X_AXIS_1_2 = 415
Y_AXIS_1_2 = 122
Y_AXIS_1_2_ADD = 80
X_AXIS_1_3 = 670
Y_AXIS_1_3 = 122
Y_AXIS_1_3_ADD = 80

X_AXIS_2_1 = 160
Y_AXIS_2_1 = 472
Y_AXIS_2_1__ADD = 22


class Selfcheck(SerialHelp):

    def __init__(self, master, canvas):
        self.root = master
        # self.root.iconbitmap('logo.ico')
        # self.root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
        # self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white', cursor='none')  #
        self.canvas = canvas
        self.checkNum = 0
        self.imageNum = 0
        self.check_err = False
        self.check_ok = False

        self.image = Image.open("./image/selfcheck.bmp")
        self.im = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(400, 300, image=self.im)
        self.canvas.pack()

        self.image3 = Image.open("./image/ok.bmp")
        self.im3 = ImageTk.PhotoImage(self.image3)
        self.parameter_init()

    def start(self):
        '''发送发送主机状态：系统自检 aa bb cc dd 0f ff 08 60 11 00 00 00 00 00 00'''
        hostStatus = 'aa bb cc dd 0f ff 08 60 11 00 00 00 00 00 00'
        self.TQueue.put(hostStatus)

        # 更新时间
        self.threadDatetime = threading.Thread(target=self.datetime_update)
        self.threadDatetime.setDaemon(True)
        self.threadDatetime.start()

        # 下一步
        self.nextimage = ImageTk.PhotoImage(Image.open("./image/next.bmp"))
        self.nextButton = ttk.Button(self.canvas, takefocus=False, image=self.nextimage,  command=self.next, cursor='none')  #
        self.nextButton.place(x=620, y=530)
        # 系统维护
        self.butmaintanceimage = ImageTk.PhotoImage(Image.open("./image/but_ma.bmp"))
        self.maintanceButton = ttk.Button(self.canvas, takefocus=False, image=self.butmaintanceimage,  command=self.maintance, cursor='none')  #
        self.maintanceButton.place(x=25, y=530)

    def parameter_init(self):
        '''
        第0行
        '''
        # 日期
        self.Date = self.canvas.create_text(X_AXIS_0_1, Y_AXIS_0_1, fill='blue', font=DEFAULT_FONT_NUM)
        # 时间
        self.Time = self.canvas.create_text(X_AXIS_0_1 + X_AXIS_0_1_ADD, Y_AXIS_0_1, fill='blue', font=DEFAULT_FONT_NUM)

        '''
        第4行
        '''

    def parameter_update(self):
        global NEXT
        global ui
        NEXT = True
        while not self.check_ok:

            self.checking(x_axis=X_AXIS_1_1, y_axis=Y_AXIS_1_1)
            self.checking(x_axis=X_AXIS_1_1, y_axis=Y_AXIS_1_1 + Y_AXIS_1_1_ADD)
            self.checking(x_axis=X_AXIS_1_1, y_axis=Y_AXIS_1_1 + 2 * Y_AXIS_1_1_ADD)
            self.checking(x_axis=X_AXIS_1_1, y_axis=Y_AXIS_1_1 + 3 * Y_AXIS_1_1_ADD)

            self.checking(x_axis=X_AXIS_1_2, y_axis=Y_AXIS_1_2)
            self.checking(x_axis=X_AXIS_1_2, y_axis=Y_AXIS_1_2 + Y_AXIS_1_2_ADD)
            self.checking(x_axis=X_AXIS_1_2, y_axis=Y_AXIS_1_2 + 2 * Y_AXIS_1_2_ADD)
            self.checking(x_axis=X_AXIS_1_2, y_axis=Y_AXIS_1_2 + 3 * Y_AXIS_1_2_ADD)

            self.checking(x_axis=X_AXIS_1_3, y_axis=Y_AXIS_1_3)
            self.checking(x_axis=X_AXIS_1_3, y_axis=Y_AXIS_1_3 + Y_AXIS_1_3_ADD)
            self.checking(x_axis=X_AXIS_1_3, y_axis=Y_AXIS_1_3 + 2 * Y_AXIS_1_3_ADD)
            self.checking(x_axis=X_AXIS_1_3, y_axis=Y_AXIS_1_3 + 3 * Y_AXIS_1_3_ADD)
            self.check_ok = True
            NEXT = False

            self.nextButton.place(x=620, y=530)
            self.maintanceButton.place(x=25, y=530)

    def checking(self, x_axis, y_axis):
        self.bar = ttk.Progressbar(self.canvas, mode='indeterminate', maximum=25, length=100)
        self.bar.place(x=x_axis - 10, y=y_axis - 10)
        self.bar.start()
        self.imageNum += 1

        time.sleep(1.25)

        self.bar.stop()
        self.checkMark = self.canvas.create_image(x_axis + 75, y_axis, image=self.im3)
        self.bar.place_forget()
        self.checkNum += 1
        # self.imageNum = 0
        self.check_err = True

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

    def thread_parameter_update(self):
        self.nextButton.place_forget()
        self.maintanceButton.place_forget()

        self.threadParameter = threading.Thread(target=self.parameter_update)
        self.threadParameter.setDaemon(True)
        self.threadParameter.start()

    def next(self):
        global FIRST
        if FIRST:
            self.thread_parameter_update()
            FIRST = False
        else:
            if not self.check_ok:
                self.check_ok = False
                self.canvas.delete(tk.ALL)
                self.canvas.create_image(400, 300, image=self.im)
                self.canvas.pack()
                self.parameter_init()
                self.thread_parameter_update()
            else:
                self.nextButton.destroy()
                self.maintanceButton.destroy()
                uiweightcalibrate = Weightcalibrate(self.root, self.canvas)
                uiweightcalibrate.start()

    def maintance(self):
        print('main')
        if not NEXT:
            self.nextButton.destroy()
            self.maintanceButton.destroy()
            uimaintance = Maintance(self.root, self.canvas)
            uimaintance.start()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
    canvas = tk.Canvas(root, width=800, height=600, bg='white', cursor='none')
    ui = Selfcheck(root, canvas)
    ui.start()
    root.mainloop()
