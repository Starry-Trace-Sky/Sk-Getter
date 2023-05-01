# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2022-10-23 Sunday
weather: sunny
script name: write_config.py

"""

from os.path import exists
from json import load, JSONDecodeError, dump


def query_config(path:str):
    """
    查找config
    param path:文件路径
    return json字典
    """
    if exists(path):
        try:
            with open(path) as f:
                config = load(f)
            return config
        except JSONDecodeError:
            return None
    return None

def update_config(path:str, key, value):
    """
    更新配置
    param path:文件路径
    param key:键
    param value:值
    """
    original_config = query_config(path)
    original_config[key] = value
    if exists(path):
        with open(path, 'w') as f:
            dump(original_config, f, indent=4)
    