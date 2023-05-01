# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2022-12-31 Saturday
weather: sunny
script name: writeHistory.py


"""

from time import strftime


def writeHistory(content):
    """写入历史记录"""
    now = strftime('%Y') + '/' + strftime('%m') + '/' + strftime('%d') + ' ' + strftime('%H') + ':' + strftime('%M') + ':' + strftime('%S') + '\n'
    with open('history.txt', 'a') as f:
        f.write(now + content + '\n')
