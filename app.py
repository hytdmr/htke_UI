#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-23 11:55:00
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import tkinter as tk
from UIstart import Start


def main():
    root = tk.Tk()
    # root.overrideredirect(True)  # 隐藏边框
    canvas = tk.Canvas(root, width=800, height=600, bg='white') #, cursor='none'
    start = Start(root, canvas)
    start.start()
    root.mainloop()


if __name__ == '__main__':
    main()
