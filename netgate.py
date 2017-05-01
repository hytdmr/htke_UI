#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-01 11:09:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import threading
import os
import sys
from serialhelp import *
from dataAnalysis import s

class NetGate(SerialHelp):
    """
    网关类，查找所有可用串口，确认网关
    """    
    def __init__(self):
        self.netGateFind = False
        self.ser_init()

    def ser_init(self):
        '''
        串口初始化
        '''
        self.ser = SerialHelp()
        self.find_available_serial()
        self.threadRead = threading.Thread(target=self.serialRead)
        self.threadRead.setDaemon(True)
        self.threadRead.start()
        self.serialWrite()

    def find_available_serial(self):
        '''
        查找所有可用串口，确认网关，并发送开机状态
        '''
        self.ComList = self.ser.find_serial()  # 获取串口列表
        if self.ComList:
            for sernum in range(len(self.ComList)):  # 遍历串口
                self.ser.port = self.ComList[sernum]
                self.ser.start()  # 打开串口
                if self.ser.alive:
                    self.data_decode()
                    self.ser.read() # 读取串口数据
                try:
                    mes = self.RQueue.get(False) # b'\xaa\xbb\xcc\xdd\x0f\x90\x08\xa1\x06\x01\x00\x00\x1c\x04\x93'
                    # print(mes)
                    mes = self.ser.ByteToHex(mes) # AABBCCDD0F8008A1060105FFE70E20
                    # print(mes)
                    if mes.find("AABBCCDD0F") != -1:
                        print('ok')
                        '''找到网关，发送主机状态：开机 abbccdd0fff086000000000000000'''                     
                        self.netGateFind = True
                        hostStatus = 'aa bb cc dd 0f ff 08 60 00 00 00 00 00 00 00'
                        self.TQueue.put(hostStatus)
                        print(self.RQueue.qsize())
                        break
                except:
                    # print('empty')
                    self.ser.stop()

    def serialRead(self):
        '''
        读取串口数据，
        '''
        while self.ser.alive:
            self.ser.read()

    def serialWrite(self):
        '''
        串口发送数据
        '''
        if self.ser.alive:
            if not self.TQueue.empty():
                data = self.TQueue.get() 
                print('>>>>>>>>>>>>>>>>>>>>>>>TQueue得到的数据<<<<<<<<<<<<<<<<<<<<<<<<<<') 
                print(data)              
                self.ser.write(data, True)               
        self.threadSerialWrite = threading.Timer(0.1, self.serialWrite)
        self.threadSerialWrite.setDaemon(True)
        self.threadSerialWrite.start()

    def data_decode(self):
        s.dataDecode()
        # self.threadDataDecode = threading.Timer(0.1, self.data_decode)
        # self.threadDataDecode.setDaemon(True)
        # self.threadDataDecode.start()