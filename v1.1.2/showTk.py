# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-14 Saturday
weather: heavy rain
script name: showInfo.py

"""
from tkinter import Tk
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno


def showTk(tkType: int, tkTitle: str, tkContent: str):
    """
    显示tkinter窗口
    tkType:窗口类型
    0为信息窗口
    1为警告窗口
    2为错误窗口
    3为询问窗口
    
    tkTitle:窗口标题
    tkContent:显示文字
    """
    root = Tk()
    root.withdraw()
    root.iconbitmap('img/icon.ico')
    # 窗口置顶显示
    root.attributes('-topmost', 1)
    if tkType == 0:
        showinfo(tkTitle, tkContent)
    elif tkType == 1:
        showwarning(tkTitle, tkContent)
    elif tkType == 2:
        showerror(tkTitle, tkContent)
    elif tkType == 3:
        result = askyesno(tkTitle, tkContent)
        return result
    root.quit()
    