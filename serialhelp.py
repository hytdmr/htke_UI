#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-13 09:25:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import threading
import serial
import binascii
import logging
import queue
from serial.tools import list_ports


logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    # filename='my.log',
                    datefmt='%a, %d %b %Y %H:%M:%S')


class SerialHelp(object):
    """
    串口辅助类
    """
    queue_maxsize = 10
    send_num = 0
    rec_num = 0
    receive_data = ""

    RQueue = queue.Queue(maxsize=queue_maxsize)
    TQueue = queue.Queue(maxsize=queue_maxsize)

    def __init__(self, Port="COM0", BaudRate="9600", ByteSize="8", Parity="N", Stopbits="1"):
        '''
        初始化串口参数
        '''
        self.l_serial = None
        self.alive = False
        self.port = Port
        self.baudrate = BaudRate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        self.timeout = 1

    def start(self):
        '''
        开始，打开串口
        '''
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = self.baudrate
        self.l_serial.bytesize = int(self.bytesize)
        self.l_serial.parity = self.parity
        self.l_serial.stopbits = int(self.stopbits)
        self.l_serial.timeout = self.timeout

        try:
            self.l_serial.open()
            if self.l_serial.isOpen():
                self.alive = True
        except Exception as e:
            self.alive = False
            logging.error(e)

    def stop(self):
        '''
        结束，关闭串口
        '''
        self.alive = False
        if self.l_serial.isOpen():
            self.l_serial.close()

    def read(self):
        '''
        读取数据
        '''
        if self.alive:
            # 预读1个数据，阻塞等待接收数据
            self.receive_data = self.l_serial.read(1)
            # print(self.receive_data)
            # 接收缓冲区数据个数
            if self.receive_data:
                self.rec_num += 1
                # print(self.rec_num)
                n = self.l_serial.inWaiting()
                # print(n)
                if n:
                    self.receive_data = self.receive_data + self.l_serial.read(n)
                    try:
                        self.RQueue.put(self.receive_data, True, 5)
                        # print(self.RQueue.qsize())

                    except queue.Full as e:
                        # print(self.receive_data)
                        logging.debug(e)

    def getread(self):
        if not self.RQueue.empty():
            return self.RQueue.get()

    def write(self, data, isHex=False):
        '''
        发送数据给串口设备
        '''
        if self.alive:
            if self.l_serial.isOpen():
                if isHex:
                    data = self.HexToByte(data)
                else:
                    data = data.encode()
                self.l_serial.write(data)
                self.send_num += 1
                print('>>>>>>>>>>>>>>>>>>>>>>>串口发送的数据<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                print(data)

    def HexToByte(self, hexStr):
        """
        串口发送方式为HEX方式，需将HEX字符串格式化为HEX字节串，HEX字符串中空格可有可无
        例：
        AABBCCDD0F9008A1060100001C0493--->b'\xaa\xbb\xcc\xdd\x0f\x90\x08\xa1\x06\x01\x00\x00\x1c\x04\x93'
        AA BB CC DD 0F 90 08 A1 06 01 00 00 1C 04 93--->b'\xaa\xbb\xcc\xdd\x0f\x90\x08\xa1\x06\x01\x00\x00\x1c\x04\x93'
        """
        return bytes.fromhex(hexStr)

    def ByteToHex(self, data):
        '''
        格式化接收到的数据字符串:
        两位十六进制，字母大写空缺补零
        strip删除空白符（包括'\n', '\r',  '\t',  ' ')
        例：
        123 --> 313233
        b'\xaa\xbb\xcc\xdd\x0f\x90\x08\xa1\x06\x01\x00\x00\x1c\x04\x93'
        ---> AABBCCDD0F9008A1060100001C0493
        '''
        return ''.join(["%02X" % x for x in data]).strip()

    def find_serial(self):
        '''
        获取到串口列表:
        (1) 即插即用，通过线程循环实现
        (2) UI中显示获取的串口
        '''
        self.ComList = list()
        try:
            self.temp_serial = list()
            for com in list_ports.comports():
                strCom = com[0]  # + ": " + com[1]  # 设备名称
                self.temp_serial.append(strCom)

            for item in self.temp_serial:
                self.ComList.append(item)
            return self.ComList

        except Exception as e:
            logging.error(e)
