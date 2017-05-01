#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-18 16:45:07
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
-----------------各模块CAN地址---------------
CAN地址ID     模块名称
0x10          网关
0x20          电源板
0x30          模拟板
0x40          空气检测器
0x50          漏血检测器
0x60          静脉夹（备用）
0x70          血泵驱动板
0x80          超滤泵驱动板
0x90          维护模块
0xFF          广播地址

-----------------工作状态定义---------------
状态编号      状态名称
0x00          开机
0x10          开机动画
0x11          系统自检
0x12          称重定标
0x13          准备预冲
0x20          进行预冲
0x21          进行治疗
0x22          确认结束
0x23          治疗结束
0x31          系统维护
0x32          称重校准
0x33          治疗参数设置
0x34          系统设置1
0x35          系统设置2

"""

import threading
import logging
import serialhelp


class DA(serialhelp.SerialHelp):
    """
    数据解析
    """

    def __init__(self):
        self.deviceId = 0
        self.temp_data = "".encode()
        self.can_data = "".encode()

        '模拟板'
        self.analog_data = "".encode()
        self.AP = 0      # Arterial Pressure，动脉压
        self.VP = 0      # Venous Pressure，静脉压
        self.UFP = 0     # Ultra Filter Pressure，超滤压
        self.FFP = 0     # Filter Front Pressure，虑前压
        self.TP = 0      # Transmembrane Pressure ，跨膜压
        self.BW = 0      # Bag Weight，超滤袋重量
        self.ASCR = 0    # Analog Self Check Result, 模拟板自检结果

        '电源板'
        self.power_data = "".encode()
        self.SP = 0      # System Power，系统电压
        self.FS = 0      # Fan Speed，风扇转速
        self.PSCR = 0    # Power Self Check Result, 电源板自检结果

        '血泵'
        self.bloodpump_data = "".encode()
        self.BPP = 0     # Blood Pump Power，血泵电压
        self.BPT = 0     # Blood Pump Temperature，血泵温度
        self.BPS = 0     # Blood Pump Speed，血泵转速
        self.BPDS = 0    # Blood Pump Door Status，血泵门状态
        self.BPSCR = 0   # Blood Pump Self Check Result, 血泵自检结果

        '超滤泵'
        self.ultrafliterpump_data = "".encode()
        self.UFPP = 0    # Ultra Filter Pump Power，超滤泵电压
        self.UFPT = 0    # Ultra Filter Pump Temperature，超滤泵温度
        self.UFPS = 0    # Ultra Filter Pump Speed，超滤泵转速
        self.UFPDS = 0   # Ultra Filter Pump Door Status，超滤泵门状态
        self.UFPSCR = 0  # Ultra Filter Pump Self Check Result, 超滤泵自检结果

        '漏血'
        self.bloodleak_data = "".encode()
        self.BL = 0      # Blood Leak，漏血
        self.BLSCR = 0   # 漏血自检结果

        '空气'
        self.air_data = "".encode()
        self.AIR = 0     # Air，空气
        self.Clip = 0    # Clip，静脉夹
        self.ASCR = 0    # Air Self Check Result，空气自检结果
        self.CSCR = 0    # Clip Self Check Result，静脉夹自检结果

        self.ser = serialhelp.SerialHelp()

    def dataLoad(self):
        self.temp_data = self.ser.getread()
        return self.temp_data

    def dataDecode(self):
        # can_data = AABBCCDD0F4008A1060091FFA905D4
        self.can_data = self.dataLoad()
        # print(self.can_data)
        if self.can_data:
            try:
                self.can_data = self.ByteToHex(self.can_data)
                # print(self.can_data)

                self.can_data = self.can_data.encode()
                # print(self.can_data)
                if type(self.can_data) is bytes:
                    # print(self.can_data.decode())
                    if self.can_data.decode().find("AABBCCDD0F") != -1:
                        # print('ok')
                        # print(self.can_data[10:12])
                        # 模拟板
                        if self.can_data[10:12].decode() == '40':
                            self.analog_data = self.can_data[14:30]
                            self.deviceId = 40
                        # 电源板
                        elif self.can_data[10:12].decode() == '50':
                            self.power_data = self.can_data[14:30]
                            self.deviceId = 50
                        # 血泵
                        elif self.can_data[10:12].decode() == '60':
                            self.bloodpump_data = self.can_data[14:30]
                            self.deviceId = 60
                        # 超滤泵
                        elif self.can_data[10:12].decode() == '70':
                            self.ultrafliterpump_data = self.can_data[14:30]
                            self.deviceId = 70
                        # 漏血
                        elif self.can_data[10:12].decode() == '80':
                            self.bloodleak_data = self.can_data[14:30]
                            self.deviceId = 80
                        # 空气
                        elif self.can_data[10:12].decode() == '90':
                            self.air_data = self.can_data[14:30]
                            self.deviceId = 90

            except Exception as e:
                logging.error(e)

    def getCan_data(self):
        return self.can_data

    "以下方法为模拟板数据解析"

    def getAnalog_data(self):
        return self.analog_data

    # Arterial Pressure，动脉压
    def getAnalog_data_AP(self):
        # print(self.getAnalog_data()[0:2])
        if self.getAnalog_data()[0:2].decode() == 'A1':
            # print('AP')
            self.AP = self.signedFromHex16(self.getAnalog_data()[4:8])
        return self.AP

    # Venous Pressure，静脉压
    def getAnalog_data_VP(self):
        if self.getAnalog_data()[0:2].decode() == 'A1':
            self.VP = self.signedFromHex16(self.getAnalog_data()[8:12])
        return self.VP

    # Ultra Filter Pressure，超滤压
    def getAnalog_data_UFP(self):
        if self.getAnalog_data()[0:2].decode() == 'A1':
            self.UFP = self.signedFromHex16(self.getAnalog_data()[12:16])
        return self.UFP

    # Filter Front Pressure，虑前压
    def getAnalog_data_FFP(self):
        if self.getAnalog_data()[0:2].decode() == 'A2':
            # print('AP')
            self.FFP = self.signedFromHex16(self.getAnalog_data()[4:8])
        return self.FFP

    # Transmembrane Pressure ，跨膜压
    def getAnalog_data_TP(self):
        if self.getAnalog_data()[0:2].decode() == 'A2':
            self.TP = self.signedFromHex16(self.getAnalog_data()[8:12])
        return self.TP

    # Bag Weight，超滤袋重量
    def getAnalog_data_BW(self):
        if self.getAnalog_data()[0:2].decode() == 'A2':
            self.BW = self.signedFromHex16(self.getAnalog_data()[12:16])
        return self.BW

    "以下方法为电源板数据解析"

    def getPower_data(self):
        return self.power_data

    # System Power，系统电压
    def getPower_data_SP(self):
        if self.getPower_data()[0:2].decode() == 'A1':
            self.SP = self.signedFromHex16(self.getPower_data()[10:12])
        return self.SP

    # Fan Speed，风扇转速
    def getPower_data_FS(self):
        if self.getPower_data()[0:2].decode() == 'A1':
            self.FS = self.signedFromHex16(self.getPower_data()[12:16])
        return self.FS

    "以下方法为血泵驱动板数据解析"

    def getBloodPump_data(self):
        return self.bloodpump_data

    # Blood Bump Power，血泵电压
    def getBloodPump_data_BPP(self):
        if self.getBloodPump_data()[0:2].decode() == 'A2':
            self.BPP = self.signedFromHex16(self.getBloodPump_data()[4:8])
        return self.BPP

    # Blood Bump Temperature，血泵温度
    def getBloodPump_data_BPT(self):
        if self.getBloodPump_data()[0:2].decode() == 'A2':
            self.BBT = self.signedFromHex16(self.getBloodPump_data()[8:12])
        return self.BPT

    # Blood Bump Speed，血泵速度
    def getBloodPump_data_BPS(self):
        if self.getBloodPump_data()[0:2].decode() == 'A2':
            self.BBS = self.signedFromHex16(self.getBloodPump_data()[12:16])
        return self.BPS

    # Blood Bump Door Status，血泵门状态
    def getBloodPump_data_BPDS(self):
        if self.getBloodPump_data()[0:2].decode() == 'A1':
            self.BBDS = self.signedFromHex16(self.getBloodPump_data()[14:16])
            # print(self.BBDS)
        return self.BPDS

    "以下方法为超滤泵驱动板数据解析"

    def getUltraFilterPump_data(self):
        return self.ultrafliterpump_data

    # Ultra Filter Bump Power，超滤泵电压
    def getUltraFilterPump_data_UFPP(self):
        if self.getUltraFilterPump_data()[0:2].decode() == 'A2':
            self.UFPP = self.signedFromHex16(self.getUltraFilterPump_data()[4:8])
        return self.UFPP

    # Ultra Filter Bump Temperature，超滤泵温度
    def getUltraFilterPump_data_UFPT(self):
        if self.getUltraFilterPump_data()[0:2].decode() == 'A2':
            self.UFPT = self.signedFromHex16(self.getUltraFilterPump_data()[8:12])
        return self.UFPT

    # Ultra Filter Bump Speed，超滤泵速度
    def getUltraFilterPump_data_UFPS(self):
        if self.getUltraFilterPump_data()[0:2].decode() == 'A2':
            self.UFPS = self.signedFromHex16(self.getUltraFilterPump_data()[12:16])
        return self.UFPS

    # Ultra Filter Bump Door Status，超滤泵门状态
    def getUltraFilterPump_data_UFPDS(self):
        if self.getUltraFilterPump_data()[0:2].decode() == 'A1':
            self.UFPDS = self.signedFromHex16(self.getUltraFilterPump_data()[14:16])
        return self.UFPDS

    "以下方法为漏血板数据解析"

    def getBloodLeak_data(self):
        return self.bloodleak_data

    # Blood Leak，漏血检测
    def getBloodLeak_data_BL(self):
        if self.getBloodLeak_data()[0:2].decode() == 'A1':
            self.BL = self.signedFromHex16(self.getBloodLeak_data()[4:6])
        return self.BL

    "以下方法为空气板数据解析"

    def getAir_data(self):
        return self.air_data

    # Air，空气检测
    def getAir_data_Air(self):
        if self.getAir_data()[0:2].decode() == 'A1':
            self.AIR = self.signedFromHex16(self.getAir_data()[4:6])
        return self.AIR

    def getAir_data_Clip(self):
        if self.getAir_data()[0:2].decode() == 'A1':
            self.Clip = self.signedFromHex16(self.getAir_data()[6:8])
        return self.Clip

    def signedFromHex16(self, s):
        '''
        十六进制转换为十进制，有符号
        '''
        v = int(s, 16)
        if not 0 <= v < 65536:
            raise ValueError("hex number outside 16 bit range")
        if v >= 32768:
            v = v - 65536
        return v

    def ByteToHex(self, data):
        '''
        格式化接收到的数据字符串
        123 --> 313233
        '''
        return ''.join(["%02X" % x for x in data]).strip()


s = DA()
sdata = s.ser.getread()
if __name__ == '__main__':

    print(sdata)
