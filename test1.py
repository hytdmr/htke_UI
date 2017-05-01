#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-28 09:18:04
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import tkinter as tk
import threading
import random
from PIL import Image, ImageTk


def show():
    text1 = random.randint(10, 1000)
    canvas.itemconfigure(c1, text=text1)
    text2 = random.randint(10, 1000)
    canvas.itemconfigure(c2, text=text2)
    # threading.Timer线程每隔2s获取串口列表
    thread_show = threading.Timer(1, show)
    # 守护线程(后台线程)，主程序结束，守护线程无论完成与否都结束
    thread_show.setDaemon(True)
    thread_show.start()


root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=600, bg='white')

image = Image.open("./image/maintance.bmp")
im = ImageTk.PhotoImage(image)
image2 = Image.open("./image/up.bmp")
im2 = ImageTk.PhotoImage(image2)

canvas.create_image(400, 300, image=im)
canvas.create_image(30, 20, image=im2)
c1 = canvas.create_text(160, 195, text='1000', fill='red', font='48')
c2 = canvas.create_text(160, 250, text='1000', fill='red', font='48')
show()

c3 = canvas.create_text(160, 115, text='50', fill='red', font='48')

global speed
speed = 0


def showlocation(event):
    x = event.x
    y = event.y
    print(x)
    print(y)
    if(260 <= x <= 320 and 75 <= y <= 110):
        global speed
        speed += 5
        canvas.itemconfigure(c3, text=speed)
    if(260 <= x <= 320 and 111 <= y <= 150):
        speed -= 5
        canvas.itemconfigure(c3, text=speed)

    if(625 <= x <= 775 and 535 <= y <= 575):
        canvas.quit()
canvas.bind("<Button>", showlocation)


canvas.pack()
root.mainloop()
