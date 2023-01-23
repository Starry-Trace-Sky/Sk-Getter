# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-22 Sunday
weather: sunny
script name: CloudMusic.py

"""
import re

import cloudmusic
from writeHistory import writeHistory


class CloudMusic:
    def __init__(self, url) -> None:
        """下载网易云音乐的歌曲,使用cloudmusic"""
        self.url = url
        self.id = re.findall('.*?id=(.*)', self.url)
        
    def download(self, savePath):
        """下载歌曲"""
        tempMusic = cloudmusic.getMusic(self.id)
        tempMusic.download(dirs=savePath)
        writeHistory(f'下载网易云音乐歌曲,链接为{self.url}')