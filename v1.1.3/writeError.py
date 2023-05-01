# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-24 Tuesday
weather: sunny
script name: writeError.py

"""
from traceback import format_exc
from time import strftime
from showTk import showTk
from subprocess import Popen, CREATE_NO_WINDOW

def writeError(win_content:str):
    """
    记录错误日志并打开错误文件
    win_content:tkinter显示内容
    """
    now = '[' + strftime('%Y') + '/' + strftime('%m') + '/' + strftime('%d')
    now += ' ' + strftime('%H') + ':' + strftime('%M') + ':' + strftime('%S') + ']'
    with open('error.log', 'a') as f:
        f.write(now + '\n' + format_exc() + '\n')
    showTk(2, '错误', win_content)
    Popen('notepad.exe error.log', creationflags=CREATE_NO_WINDOW)
