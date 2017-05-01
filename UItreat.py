#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-18 15:57:04
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
from UIconfirmfinishtreat import Confirmfinishtreat
from globalvariable import *
from UIkeyboard import *

X_AXIS_KEYBOARD = 612
Y_AXIS_KEYBOARD = 425

X_AXIS_3_1 = 270
Y_AXIS_3_1 = 257
X_AXIS_3_2 = 408
Y_AXIS_3_2 = 257
X_AXIS_3_3 = 472
Y_AXIS_3_3 = 257
X_AXIS_3_4 = 645
Y_AXIS_3_4 = 257

X_AXIS_4_1 = 270
Y_AXIS_4_1 = 306
X_AXIS_4_2 = 408
Y_AXIS_4_2 = 306
X_AXIS_4_3 = 472
Y_AXIS_4_3 = 306
X_AXIS_4_4 = 645
Y_AXIS_4_4 = 306

X_AXIS_5_1 = 270
Y_AXIS_5_1 = 352
X_AXIS_5_2 = 408
Y_AXIS_5_2 = 352

X_AXIS_6_1 = 270
Y_AXIS_6_1 = 402
X_AXIS_6_2 = 408
Y_AXIS_6_2 = 402


class Treat(SerialHelp):

    def __init__(self, master, canvas):
        self.root = master
        # self.root.iconbitmap('logo.ico')
        # self.root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
        # self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white', cursor='none')  #
        self.canvas = canvas

        self.image = Image.open("./image/treat.bmp")
        self.im = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(400, 300, image=self.im)
        self.canvas.pack()
        self.parameter_init()
        self.canvas.bind("<Button>", self.button_press)

    def start(self):
        # 发送发送主机状态：进行治疗 aa bb cc dd 0f ff 08 60 21 00 00 00 00 00 00
        hostStatus = 'aa bb cc dd 0f ff 08 60 21 00 00 00 00 00 00'
        self.TQueue.put(hostStatus)

        # 更新时间
        self.threadDatetime = threading.Thread(target=self.datetime_update)
        self.threadDatetime.setDaemon(True)
        self.threadDatetime.start()

        # 动脉压及其上下限
        self.arterialPressure = self.canvas.create_text(X_AXIS_3_1, Y_AXIS_3_1, text='1000', fill='blue', font=DEFAULT_FONT_NUM)
        self.arterialPressureMin = self.canvas.create_text(X_AXIS_3_2, Y_AXIS_3_2, text='0', fill='blue', font=DEFAULT_FONT_NUM)
        self.arterialPressureMax = self.canvas.create_text(X_AXIS_3_3, Y_AXIS_3_3, text='2000', fill='blue', font=DEFAULT_FONT_NUM)
        # 虑器前压
        self.filterFrontPressure = self.canvas.create_text(X_AXIS_3_4, Y_AXIS_3_4, text='1000', fill='blue', font=DEFAULT_FONT_NUM)

        # 静脉压及其上下限
        self.venousPressure = self.canvas.create_text(X_AXIS_4_1, Y_AXIS_4_1, text='-1000', fill='blue', font=DEFAULT_FONT_NUM)
        self.venousPressureMin = self.canvas.create_text(X_AXIS_4_2, Y_AXIS_4_2, text='-2000', fill='blue', font=DEFAULT_FONT_NUM)
        self.venousPressureMax = self.canvas.create_text(X_AXIS_4_3, Y_AXIS_4_3, text='0', fill='blue', font=DEFAULT_FONT_NUM)
        # 虑器压降
        self.filterPressureDrop = self.canvas.create_text(X_AXIS_4_4, Y_AXIS_4_4, text='100', fill='blue', font=DEFAULT_FONT_NUM)

        # 超滤压及其上限
        self.ultraFilterPressure = self.canvas.create_text(X_AXIS_5_1, Y_AXIS_5_1, text='1200', fill='blue', font=DEFAULT_FONT_NUM)
        self.ultraFilterPressureMax = self.canvas.create_text(X_AXIS_5_2, Y_AXIS_5_2, text='2000', fill='blue', font=DEFAULT_FONT_NUM)

        # 跨膜压及其下限
        self.transmembranePressure = self.canvas.create_text(X_AXIS_6_1, Y_AXIS_6_1, text='1300', fill='blue', font=DEFAULT_FONT_NUM)
        self.transmembranePressureMin = self.canvas.create_text(X_AXIS_6_2, Y_AXIS_6_2, text='2000', fill='blue', font=DEFAULT_FONT_NUM)

        # 结束治疗
        self.butfinishtreatimage = ImageTk.PhotoImage(Image.open("./image/but_finishtreat.bmp"))
        self.finishtreatButton = ttk.Button(self.canvas, takefocus=False, image=self.butfinishtreatimage,  command=self.finishtreat, cursor='none')  #
        self.finishtreatButton.place(x=620, y=530)

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

    def finishtreat(self):
        if not Keyboard.keyBoardCall:
            print('Fhinsh treat...')
            self.finishtreatButton.destroy()
                
            confirmfinisttreat = Confirmfinishtreat(self.root, self.canvas)
            confirmfinisttreat.start()

    def button_press(self, event):
        x = event.x
        y = event.y
        # print(x)
        # print(y)
        if not Keyboard.keyBoardCall:
            
            # 动脉压上下限
            if(385 <= x <= 435 and 240 <= y <= 275):
                # 发送发送主机状态：治疗参数设置 aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00
                hostStatus = 'aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00'
                self.TQueue.put(hostStatus)

                Keyboard.keyBoardCall = True
                self.finishtreatButton.place_forget()
                self.keyboard = Keyboard(self.root, self.canvas, X_AXIS_KEYBOARD, Y_AXIS_KEYBOARD)
                self.original = self.canvas.itemcget(self.arterialPressureMin, 'text')
                self.change_min_max(self.arterialPressureMin)

                # instruct_BpSpeedUp = 'aabbccdd0f4008A10600faff10fb01'
                # self.TQueue.put(instruct_BpSpeedUp)
            if(450 <= x <= 500 and 240 <= y <= 275):
                # 发送发送主机状态：治疗参数设置 aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00
                hostStatus = 'aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00'
                self.TQueue.put(hostStatus)
                
                Keyboard.keyBoardCall = True
                self.finishtreatButton.place_forget()
                self.keyboard = Keyboard(self.root, self.canvas, X_AXIS_KEYBOARD, Y_AXIS_KEYBOARD)
                self.original = self.canvas.itemcget(self.arterialPressureMax, 'text')
                self.change_min_max(self.arterialPressureMax)
                
                # instruct_BpSpeedUp = 'aabbccdd0f4008A10600faff10fb01'
                # self.TQueue.put(instruct_BpSpeedUp)

            # 静脉压上下限
            if(385 <= x <= 435 and 285 <= y <= 320):
                # 发送发送主机状态：治疗参数设置 aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00
                hostStatus = 'aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00'
                self.TQueue.put(hostStatus)

                Keyboard.keyBoardCall = True
                self.finishtreatButton.place_forget()
                self.keyboard = Keyboard(self.root, self.canvas, X_AXIS_KEYBOARD, Y_AXIS_KEYBOARD)
                self.original = self.canvas.itemcget(self.venousPressureMin, 'text')
                self.change_min_max(self.venousPressureMin)
                

                # instruct_BpSpeedUp = 'aabbccdd0f4008A10600faff10fb01'
                # self.TQueue.put(instruct_BpSpeedUp)
            if(450 <= x <= 500 and 285 <= y <= 320):
                # 发送发送主机状态：治疗参数设置 aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00
                hostStatus = 'aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00'
                self.TQueue.put(hostStatus)

                Keyboard.keyBoardCall = True
                self.finishtreatButton.place_forget()
                self.keyboard = Keyboard(self.root, self.canvas, X_AXIS_KEYBOARD, Y_AXIS_KEYBOARD)
                self.original = self.canvas.itemcget(self.venousPressureMax, 'text')
                self.change_min_max(self.venousPressureMax)
            

            # instruct_BpSpeedUp = 'aabbccdd0f4008A10600faff10fb01'
            # self.TQueue.put(instruct_BpSpeedUp)

            # 超滤压上限
            if(385 <= x <= 435 and 335 <= y <= 370):
                # 发送发送主机状态：治疗参数设置 aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00
                hostStatus = 'aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00'
                self.TQueue.put(hostStatus)

                Keyboard.keyBoardCall = True
                self.finishtreatButton.place_forget()
                self.keyboard = Keyboard(self.root, self.canvas, X_AXIS_KEYBOARD, Y_AXIS_KEYBOARD)
                self.original = self.canvas.itemcget(self.ultraFilterPressureMax, 'text')
                self.change_min_max(self.ultraFilterPressureMax)
                

                # instruct_BpSpeedUp = 'aabbccdd0f4008A10600faff10fb01'
                # self.TQueue.put(instruct_BpSpeedUp)

            # 跨膜压下限
            if(385 <= x <= 435 and 385 <= y <= 420):
                # 发送发送主机状态：治疗参数设置 aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00
                hostStatus = 'aa bb cc dd 0f ff 08 60 33 00 00 00 00 00 00'
                self.TQueue.put(hostStatus)

                Keyboard.keyBoardCall = True
                self.finishtreatButton.place_forget()
                self.keyboard = Keyboard(self.root, self.canvas, X_AXIS_KEYBOARD, Y_AXIS_KEYBOARD)
                self.original = self.canvas.itemcget(self.transmembranePressureMin, 'text')
                self.change_min_max(self.transmembranePressureMin)
                

                # instruct_BpSpeedUp = 'aabbccdd0f4008A10600faff10fb01'
                # self.TQueue.put(instruct_BpSpeedUp)

    def change_min_max(self, item=None):

        # print(original)
        if self.keyboard.input_cancel:
            self.canvas.itemconfigure(item, text=self.original)
            Keyboard.keyBoardCall = False
            self.finishtreatButton.place(x=620, y=530)
        if not self.keyboard.input_ok:
            min_max = self.keyboard.keynum
            if min_max:
                self.canvas.itemconfigure(item, text=min_max)
            else:
                self.canvas.itemconfigure(item, text=self.original)
            # print(self.keyboard.number)
            self.threadChange = threading.Timer(0.1, self.change_min_max, args=(item,))
            self.threadChange.setDaemon(True)
            self.threadChange.start()
        else:
            self.threadChange.cancel()
            Keyboard.keyBoardCall = False
            self.finishtreatButton.place(x=620, y=530)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
    canvas = tk.Canvas(root, width=800, height=600, bg='white')  # , cursor='none'
    ui = Treat(root, canvas)
    ui.start()
    root.mainloop()
