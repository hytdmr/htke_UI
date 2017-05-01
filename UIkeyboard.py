#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-20 09:54:16
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk


class Keyboard:
    """
    虚拟键盘
    """
    keyBoardCall = False
    def __init__(self, master, canvas, x, y):

        self.root = master
        self.canvas = canvas
        self.keynum = ''
        self.number = ''
        self.input_ok = False
        self.input_cancel = False


        self.imagekeyboard = Image.open("./image/keyboard.bmp")
        self.keyboard = ImageTk.PhotoImage(self.imagekeyboard)
        self.idKeyboard = self.canvas.create_image(x, y, image=self.keyboard)

        self.imagekey0 = Image.open("./image/key0.bmp")
        self.key0 = ImageTk.PhotoImage(self.imagekey0)
        self.imagekey1 = Image.open("./image/key1.bmp")
        self.key1 = ImageTk.PhotoImage(self.imagekey1)
        self.imagekey2 = Image.open("./image/key2.bmp")
        self.key2 = ImageTk.PhotoImage(self.imagekey2)
        self.imagekey3 = Image.open("./image/key3.bmp")
        self.key3 = ImageTk.PhotoImage(self.imagekey3)
        self.imagekey4 = Image.open("./image/key4.bmp")
        self.key4 = ImageTk.PhotoImage(self.imagekey4)
        self.imagekey5 = Image.open("./image/key5.bmp")
        self.key5 = ImageTk.PhotoImage(self.imagekey5)
        self.imagekey6 = Image.open("./image/key6.bmp")
        self.key6 = ImageTk.PhotoImage(self.imagekey6)
        self.imagekey7 = Image.open("./image/key7.bmp")
        self.key7 = ImageTk.PhotoImage(self.imagekey7)
        self.imagekey8 = Image.open("./image/key8.bmp")
        self.key8 = ImageTk.PhotoImage(self.imagekey8)
        self.imagekey9 = Image.open("./image/key9.bmp")
        self.key9 = ImageTk.PhotoImage(self.imagekey9)
        self.imagekeyplus = Image.open("./image/keyplus.bmp")
        self.keyplus = ImageTk.PhotoImage(self.imagekeyplus)
        self.imagekeyminus = Image.open("./image/keyminus.bmp")
        self.keyminus = ImageTk.PhotoImage(self.imagekeyminus)
        self.imagekeyok = Image.open("./image/keyok.bmp")
        self.keyok = ImageTk.PhotoImage(self.imagekeyok)
        self.imagekeycancel = Image.open("./image/keycancel.bmp")
        self.keycancel = ImageTk.PhotoImage(self.imagekeycancel)
        self.imagekeyx = Image.open("./image/keyx.bmp")
        self.keyx = ImageTk.PhotoImage(self.imagekeyx)

        self.butkey1 = ttk.Button(self.canvas, takefocus=False, image=self.key1,  command=self.but_key1)  # , cursor='none'
        self.butkey1.place(x=x - 152, y=y - 90)

        self.butkey2 = ttk.Button(self.canvas, takefocus=False, image=self.key2,  command=self.but_key2)  # , cursor='none'
        self.butkey2.place(x=x - 102, y=y - 90)

        self.butkey3 = ttk.Button(self.canvas, takefocus=False, image=self.key3,  command=self.but_key3)  # , cursor='none'
        self.butkey3.place(x=x - 51, y=y - 90)

        self.butkey4 = ttk.Button(self.canvas, takefocus=False, image=self.key4,  command=self.but_key4)  # , cursor='none'
        self.butkey4.place(x=x - 0, y=y - 90)

        self.butkey5 = ttk.Button(self.canvas, takefocus=False, image=self.key5,  command=self.but_key5)  # , cursor='none'
        self.butkey5.place(x=x + 51, y=y - 90)

        self.butkeyminus = ttk.Button(self.canvas, takefocus=False, image=self.keyminus,  command=self.but_keyminus)  # , cursor='none'
        self.butkeyminus.place(x=x + 102, y=y - 90)

        self.butkey6 = ttk.Button(self.canvas, takefocus=False, image=self.key6,  command=self.but_key6)  # , cursor='none'
        self.butkey6.place(x=x - 152, y=y - 25)

        self.butkey7 = ttk.Button(self.canvas, takefocus=False, image=self.key7,  command=self.but_key7)  # , cursor='none'
        self.butkey7.place(x=x - 102, y=y - 25)

        self.butkey8 = ttk.Button(self.canvas, takefocus=False, image=self.key8,  command=self.but_key8)  # , cursor='none'
        self.butkey8.place(x=x - 51, y=y - 25)

        self.butkey9 = ttk.Button(self.canvas, takefocus=False, image=self.key9,  command=self.but_key9)  # , cursor='none'
        self.butkey9.place(x=x - 0, y=y - 25)

        self.butkey0 = ttk.Button(self.canvas, takefocus=False, image=self.key0,  command=self.but_key0)  # , cursor='none'
        self.butkey0.place(x=x + 51, y=y - 25)

        self.butkeyplus = ttk.Button(self.canvas, takefocus=False, image=self.keyplus,  command=self.but_keyplus)  # , cursor='none'
        self.butkeyplus.place(x=x + 102, y=y - 25)

        self.butkeyx = ttk.Button(self.canvas, takefocus=False, image=self.keyx,  command=self.but_keyx)  # , cursor='none'
        self.butkeyx.place(x=x - 152, y=y + 35)

        self.butkeyok = ttk.Button(self.canvas, takefocus=False, image=self.keyok,  command=self.but_keyok)  # , cursor='none'
        self.butkeyok.place(x=x - 102, y=y + 35)

        self.butkeycancel = ttk.Button(self.canvas, takefocus=False, image=self.keycancel,  command=self.but_keycancel)  # , cursor='none'
        self.butkeycancel.place(x=x + 25, y=y + 35)

    def but_key1(self):
        self.keynum += '1'

    def but_key2(self):
        self.keynum += '2'

    def but_key3(self):
        self.keynum += '3'

    def but_key4(self):
        self.keynum += '4'

    def but_key5(self):
        self.keynum += '5'

    def but_keyminus(self):
        if len(self.keynum) == 0:
            self.keynum = '-'

    def but_key6(self):
        self.keynum += '6'

    def but_key7(self):
        self.keynum += '7'

    def but_key8(self):
        self.keynum += '8'

    def but_key9(self):
        self.keynum += '9'

    def but_key0(self):
        if len(self.keynum) > 0:
            self.keynum += '0'

    def but_keyplus(self):
        if len(self.keynum) == 0:
            self.keynum = '+'

    def but_keyx(self):
        self.keynum = self.keynum[0:len(self.keynum) - 1]

    def but_keyok(self):
        self.number = self.keynum
        self.keynum = ''
        self.input_ok = True
        KEYBOARDCALL = False
        print(self.number)
        self.keyboard_exit()

    def but_keycancel(self):
        self.keynum = ''
        self.input_ok = True
        self.input_cancel = True
        KEYBOARDCALL = False
        self.keyboard_exit()


    def keyboard_exit(self):
        '''
        退出键盘
        '''
        self.canvas.delete(self.idKeyboard)
        self.butkey1.destroy()
        self.butkey2.destroy()
        self.butkey3.destroy()
        self.butkey4.destroy()
        self.butkey5.destroy()
        self.butkey6.destroy()
        self.butkey7.destroy()
        self.butkey8.destroy()
        self.butkey9.destroy()
        self.butkey0.destroy()
        self.butkeyplus.destroy()
        self.butkeyminus.destroy()
        self.butkeyok.destroy()
        self.butkeycancel.destroy()
        self.butkeyx.destroy()


def test():
    root = tk.Tk()
    root.geometry('800x600')
    canvas = tk.Canvas(root, width=800, height=600, bg='white')  # , cursor='none'
    image1 = Image.open("./image/start1.bmp")
    im1 = ImageTk.PhotoImage(image1)
    canvas.create_image(400, 300, image=im1)
    canvas.pack()
    keyboard = Keyboard(root, canvas, 450, 250)

    root.mainloop()


if __name__ == '__main__':
    test()
