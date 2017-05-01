#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-28 11:29:48
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


class Maintance(SerialHelp):
    """
    维护界面
    """

    def __init__(self, master, canvas):
        self.root = master
        # self.root.iconbitmap('logo.ico')
        # self.root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
        # self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white', cursor='none')  #
        self.canvas = canvas

        self.image = Image.open("./image/maintance.bmp")
        self.im = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(400, 300, image=self.im)
        self.canvas.pack()
        self.bloodSpeed = 0
        self.fliterSpeed = 0
        self.parameter_init()
        # self.canvas.bind("<Button>", self.button_press)

    def start(self):
        # 发送发送主机状态：系统维护 aa bb cc dd 0f ff 08 60 31 00 00 00 00 00 00
        hostStatus = 'aa bb cc dd 0f ff 08 60 31 00 00 00 00 00 00'
        self.TQueue.put(hostStatus)

        # 更新时间
        self.threadDatetime = threading.Thread(target=self.datetime_update)
        self.threadDatetime.setDaemon(True)
        self.threadDatetime.start()

        # 更新参数
        self.threadParameter = threading.Thread(target=self.parameter_update)
        self.threadParameter.setDaemon(True)
        self.threadParameter.start()

        # 解析数据
        self.data_decode()


    def parameter_init(self):
        """
        参数初始化，共5行参数，从0开始
        """
        
        # ---------------------第0行----------------------
        # 日期
        self.Date = self.canvas.create_text(X_AXIS_0_1, Y_AXIS_0_1, text='17-03-28', fill='blue', font=DEFAULT_FONT_NUM)
        # 时间
        self.Time = self.canvas.create_text(X_AXIS_0_1 + X_AXIS_0_1_ADD, Y_AXIS_0_1, text='14:44', fill='blue', font=DEFAULT_FONT_NUM)


        # ---------------------第1行----------------------
        # 血泵速度
        self.bloodPumpSpeed = self.canvas.create_text(X_AXIS_1_1, Y_AXIS_1_1, text=self.bloodSpeed, fill='blue', font=DEFAULT_FONT_NUM)
        self.upimage = ImageTk.PhotoImage(Image.open("./image/up.bmp"))
        self.bloodPumpSpeedUpButton = ttk.Button(self.canvas, takefocus=True, image=self.upimage,  command=self.bloodPump_speed_up, cursor='none')  #
        self.bloodPumpSpeedUpButton.place(x=260, y=64)
        self.downimage = ImageTk.PhotoImage(Image.open("./image/down.bmp"))
        self.bloodPumpSpeedDownButton = ttk.Button(self.canvas, takefocus=False, image=self.downimage, cursor='none', command=self.bloodPump_speed_down)
        self.bloodPumpSpeedDownButton.place(x=260, y=113)

        # 超滤速度
        self.ultraFilterPumpSpeed = self.canvas.create_text(X_AXIS_1_1 + X_AXIS_1_1_ADD, Y_AXIS_1_1, text=self.fliterSpeed, fill='blue', font=DEFAULT_FONT_NUM)
        self.ultraFliterPumpSpeedUpButton = ttk.Button(self.canvas, takefocus=False, image=self.upimage, cursor='none', command=self.ultraFliterPump_speed_up)
        self.ultraFliterPumpSpeedUpButton.place(x=655, y=64)
        self.ultraFliterPumpSpeedDownButton = ttk.Button(self.canvas, takefocus=False, image=self.downimage,
                                                         cursor='none', command=self.ultraFliterPump_speed_down)
        self.ultraFliterPumpSpeedDownButton.place(x=655, y=113)

        
        # ---------------------第2行----------------------
        # ---------------------第2行，第1列---------------
        # 动脉压
        self.arterialPressure = self.canvas.create_text(X_AXIS_2_1, Y_AXIS_2_1, text='1000', fill='blue', font=DEFAULT_FONT_NUM)
        # 静脉压
        self.venousPressure = self.canvas.create_text(X_AXIS_2_1, Y_AXIS_2_1 + Y_AXIS_2_1_ADD, text='1100', fill='blue', font=DEFAULT_FONT_NUM)
        # 超滤压
        self.ultraFilterPressure = self.canvas.create_text(X_AXIS_2_1, Y_AXIS_2_1 + 2 * Y_AXIS_2_1_ADD, text='1200', fill='blue', font=DEFAULT_FONT_NUM)
        # 虑前压
        self.filterFrontPressure = self.canvas.create_text(X_AXIS_2_1, Y_AXIS_2_1 + 3 * Y_AXIS_2_1_ADD, text='1300', fill='blue', font=DEFAULT_FONT_NUM)
        # # 跨膜压
        # self.transmembranePressure = self.canvas.create_text(X_AXIS_2_1, Y_AXIS_2_1 + 4 * Y_AXIS_2_1_ADD, text='1400', fill='blue', font=DEFAULT_FONT_NUM)
        # 滤袋重量
        self.bagWeight = self.canvas.create_text(X_AXIS_2_1, Y_AXIS_2_1 + 4 * Y_AXIS_2_1_ADD, text='1500', fill='blue', font=DEFAULT_FONT_NUM)

        # ---------------------第2行，第2列---------------
        # 静脉夹
        self.clipStatus = self.canvas.create_text(X_AXIS_2_2, Y_AXIS_2_2, text='开', fill='blue', font=DEFAULT_FONT)
        # 漏血
        self.bloodLeakStatus = self.canvas.create_text(X_AXIS_2_2, Y_AXIS_2_2 + Y_AXIS_2_2_ADD, text='否', fill='blue', font=DEFAULT_FONT)
        # 空气
        self.airtatus = self.canvas.create_text(X_AXIS_2_2, Y_AXIS_2_2 + 2 * Y_AXIS_2_2_ADD, text='是', fill='blue', font=DEFAULT_FONT)
        # 血泵门
        self.bloodDoorStatus = self.canvas.create_text(X_AXIS_2_2, Y_AXIS_2_2 + 3 * Y_AXIS_2_2_ADD, text='关', fill='blue', font=DEFAULT_FONT)
        # 超滤门
        self.ultraFilterDoorStatus = self.canvas.create_text(X_AXIS_2_2, Y_AXIS_2_2 + 4 * Y_AXIS_2_2_ADD, text='开', fill='blue', font=DEFAULT_FONT)

        # ---------------------第2行，第3列---------------
        # 血泵驱动电压
        self.bloodPumpPower = self.canvas.create_text(X_AXIS_2_3, Y_AXIS_2_3, text='24', fill='blue', font=DEFAULT_FONT_NUM)
        # 血泵驱动温度
        self.bloodPumpTemperature = self.canvas.create_text(X_AXIS_2_3 + X_AXIS_2_3_ADD, Y_AXIS_2_3, text='18', fill='blue', font=DEFAULT_FONT_NUM)
        # 超滤驱动电压
        self.ultraFilterPumpPower = self.canvas.create_text(X_AXIS_2_3, Y_AXIS_2_3 + Y_AXIS_2_3_ADD, text='20', fill='blue', font=DEFAULT_FONT_NUM)
        # 超滤驱动温度
        self.ultraFilterPumpTemperature = self.canvas.create_text(
            X_AXIS_2_3 + X_AXIS_2_3_ADD, Y_AXIS_2_3 + Y_AXIS_2_3_ADD, text='17', fill='blue', font=DEFAULT_FONT_NUM)
        # 系统电压
        self.systemPower = self.canvas.create_text(X_AXIS_2_3, Y_AXIS_2_3 + 2 * Y_AXIS_2_3_ADD, text='24', fill='blue', font=DEFAULT_FONT_NUM)
        # 风扇转速
        self.fanSpeed = self.canvas.create_text(X_AXIS_2_3, Y_AXIS_2_3 + 3 * Y_AXIS_2_3_ADD, text='1800', fill='blue', font=DEFAULT_FONT_NUM)
        # 通信
        self.comunication = self.canvas.create_text(X_AXIS_2_3, Y_AXIS_2_3 + 4 * Y_AXIS_2_3_ADD, text='开', fill='blue', font=DEFAULT_FONT)
        # 识别卡
        self.identificationCard = self.canvas.create_text(X_AXIS_2_3, Y_AXIS_2_3 + 5 * Y_AXIS_2_3_ADD, text='关', fill='blue', font=DEFAULT_FONT)


        # ---------------------第3行----------------------
        # 按键码
        self.keyCode = self.canvas.create_text(X_AXIS_3_1, Y_AXIS_3_1, text='按键码', fill='blue', font=DEFAULT_FONT)
        # 错误码
        self.errCode = self.canvas.create_text(X_AXIS_3_1, Y_AXIS_3_1 + Y_AXIS_3_1__ADD, text='错误码', fill='blue', font=DEFAULT_FONT)


        # ---------------------第4行----------------------
        # 返回
        self.returnimage = ImageTk.PhotoImage(Image.open("./image/ret.bmp"))
        self.retButton = ttk.Button(self.canvas, takefocus=False, image=self.returnimage,  command=self.ret, cursor='none')  #
        self.retButton.place(x=615, y=530)

        # ######退出程序，实际应用中去掉######
        self.exitButton = ttk.Button(self.canvas, takefocus=False, text='QUIT',  command=self.quit, cursor='none')  #
        self.exitButton.place(x=25, y=530)

    def parameter_update(self):
        """
        更新参数
        """
        # print(self.RQueue.qsize())
        # deviceId = s.dataDecode()
        # print(s.deviceId)

        if s.deviceId == 40:
            self.canvas.itemconfigure(self.arterialPressure, text=s.getAnalog_data_AP())
            self.canvas.itemconfigure(self.venousPressure, text=s.getAnalog_data_VP())
            self.canvas.itemconfigure(self.ultraFilterPressure, text=s.getAnalog_data_UFP())
            self.canvas.itemconfigure(self.filterFrontPressure, text=s.getAnalog_data_FFP())
            self.canvas.itemconfigure(self.bagWeight, text=s.getAnalog_data_BW())

        if s.deviceId == 50:
            self.canvas.itemconfigure(self.systemPower, text=s.getPower_data_SP())
            self.canvas.itemconfigure(self.fanSpeed, text=s.getPower_data_FS())

        if s.deviceId == 60:
            self.canvas.itemconfigure(self.bloodPumpPower, text=s.getBloodPump_data_BPP())
            self.canvas.itemconfigure(self.bloodPumpTemperature, text=s.getBloodPump_data_BPT())

            if s.getBloodPump_data_BPDS() == 1:
                self.canvas.itemconfigure(self.bloodDoorStatus, text='开')
            else:
                self.canvas.itemconfigure(self.bloodDoorStatus, text='关')

        if s.deviceId == 70:
            self.canvas.itemconfigure(self.ultraFilterPumpPower, text=s.getUltraFilterPump_data_UFPP())
            self.canvas.itemconfigure(self.ultraFilterPumpTemperature, text=s.getUltraFilterPump_data_UFPT())

            if s.getUltraFilterPump_data_UFPDS() == 1:
                self.canvas.itemconfigure(self.ultraFilterDoorStatus, text='开')
            else:
                self.canvas.itemconfigure(self.ultraFilterDoorStatus, text='关')

        if s.deviceId == 80:
            if s.getAir_data_Clip() == 1:
                self.canvas.itemconfigure(self.clipStatus, text='开')
            else:
                self.canvas.itemconfigure(self.clipStatus, text='关')

            if s.getAir_data_Air() == 1:
                self.canvas.itemconfigure(self.airtatus, text='是')
            else:
                self.canvas.itemconfigure(self.airtatus, text='否')

        if s.deviceId == 90:
            if s.getBloodLeak_data_BL() == 1:
                self.canvas.itemconfigure(self.bloodLeakStatus, text='是')
            else:
                self.canvas.itemconfigure(self.bloodLeakStatus, text='否')

        self.threadParameterUpdate = threading.Timer(0.1, self.parameter_update)
        self.threadParameterUpdate.setDaemon(True)
        self.threadParameterUpdate.start()

    

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

    def bloodPump_speed_up(self):
        if s.BPS <= 45:
            s.BPS += 5
            self.canvas.itemconfigure(self.bloodPumpSpeed, text=s.BPS)
            instruct_BpSpeedUp = 'aabbccdd0f4008A10600faff10fb01'
            self.TQueue.put(instruct_BpSpeedUp)

    def bloodPump_speed_down(self):
        if s.BPS >= 5:
            s.BPS -= 5
            self.canvas.itemconfigure(self.bloodPumpSpeed, text=s.BPS)
            instruct_BpSpeedDown = 'aabbccdd0f4008A10600faff10fb02'
            self.TQueue.put(instruct_BpSpeedDown)

    def ultraFliterPump_speed_up(self):
        if s.UFPS <= 450:
            s.UFPS += 50
            self.canvas.itemconfigure(self.ultraFilterPumpSpeed, text=s.UFPS)
            instruct_UpSpeedUp = 'aabbccdd0f4008A10600faff10fb03'
            self.TQueue.put(instruct_UpSpeedUp)

    def ultraFliterPump_speed_down(self):
        if s.UFPS >= 50:
            s.UFPS -= 50
            self.canvas.itemconfigure(self.ultraFilterPumpSpeed, text=s.UFPS)
            instruct_UpSpeedDown = 'aabbccdd0f4008A10600faff10fb04'
            self.TQueue.put(instruct_UpSpeedDown)
            print(self.TQueue.qsize())

    def ret(self):
        from UIselfcheck import Selfcheck
        # from UIstart import Start
        self.canvas.delete('ALL')
        self.bloodPumpSpeedUpButton.destroy()
        self.bloodPumpSpeedDownButton.destroy()
        self.ultraFliterPumpSpeedUpButton.destroy()
        self.ultraFliterPumpSpeedDownButton.destroy()

        self.retButton.destroy()
        self.exitButton.destroy()
        print('ret')
        selfcheck = Selfcheck(self.root, self.canvas)
        selfcheck.start()

        # start = Start(self.root, self.canvas)
        # start.start()

    def data_decode(self):
        s.dataDecode()
        self.threadDataDecode = threading.Timer(0.1, self.data_decode)
        self.threadDataDecode.setDaemon(True)
        self.threadDataDecode.start()

    def quit(self):
        sys.exit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('心衰超滤脱水装置--北京哈特凯尔医疗科技有限公司')
    canvas = tk.Canvas(root, width=800, height=600, bg='white', cursor='none')
    ui = Maintance(root, canvas)
    ui.start()
    root.mainloop()
