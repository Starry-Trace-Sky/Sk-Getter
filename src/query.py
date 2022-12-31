# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2022-10-23 Sunday
weather: sunny
script name: write_config.py

"""

import json, os, sys


def query_config(path:str):
    """
    查找config
    param path:文件路径
    return json字典
    """
    if os.path.exists(path):
        try:
            with open(path) as f:
                config = json.load(f)
        except json.JSONDecodeError:
            sys.exit()
    return config

def update_config(path:str, key, value):
    """
    更新配置
    param path:文件路径
    param key:键
    param value:值
    """
    original_config = query_config(path)
    original_config[key] = value
    if os.path.exists(path):
        with open(path, 'w') as f:
            json.dump(original_config, f, indent=4)
    