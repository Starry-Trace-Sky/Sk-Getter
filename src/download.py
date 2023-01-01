# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2022-12-05 Monday
weather: small rain
script name: download.py

"""
import re
import os
import hashlib
from subprocess import Popen, CREATE_NO_WINDOW

import requests
import cloudmusic
from query import query_config
from writeHistory import writeHistory


# 读取保存位置
save_path = query_config('config/settings.json')
save_path = save_path['save_path']

"""
====================================视频====================================
"""
class Bilibili:
    def __init__(self, source_url) -> None:
        """
        初始化设置
        source_url: 分享出来的bilibili链接
        """
        self.source_url = source_url
        self.bvid = re.findall('https://www.bilibili.com/video/(.*?)/', self.source_url)[0]
        self.api_get_aid_url = f'https://api.bilibili.com/x/web-interface/view?bvid={self.bvid}'
        self.api_get_cid_url = f'https://api.bilibili.com/x/player/pagelist?bvid={self.bvid}&jsonp=jsonp'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
            'origin':'https://www.bilibili.com',
            'referer':'https://www.bilibili.com'
        }
        self.headers1 = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
            'origin':'https://www.bilibili.com',
            'referer':'https://www.bilibili.com',
            'connection':'keep-alive'
        }
        # 获取cid
        res = requests.get(self.api_get_cid_url, headers=self.headers)
        self.cid = res.json()['data'][0]['cid']
        # 获取avid
        res = requests.get(self.api_get_aid_url, headers=self.headers)
        self.avid = res.json()['data']['aid']
        self.url = 'https://api.bilibili.com/x/player/playurl?fnver=0&fnval=4048&fourk=1&voice_balance=1&qn=80&'
        self.url += f'avid={self.avid}&bvid={self.bvid}&cid={self.cid}'

    def get_one_link(self):
        """获取视频,音频链接"""
        con = requests.get(self.url, headers=self.headers)
        
        if con.status_code == 200:
            data_js = con.json()
            video_url = data_js['data']['dash']['video'][0]['backupUrl'][0]
            audio_url = data_js['data']['dash']['audio'][0]['backupUrl'][0]
            data = {'video_url':video_url, 'audio_url':audio_url}
            writeHistory(f'获取到B站视频,原链接为{self.source_url}')
            return data
        return None

    def download(self, input_url:str, filename:str):
        """
        下载函数
        input_url: 下载链接
        filename: 文件名
        """
        s = requests.session()
        s.options(input_url, headers=self.headers1)
        conn = s.get(input_url, headers=self.headers1)

        if conn.status_code == 200:
            with open(save_path + '/tmp/' + filename, 'wb') as f:
                f.write(conn.content)

    def merge(self, filename:str):
        """
        合并音频和视频,删除源文件
        """
        file_path = save_path + '/' + filename
        video_path = save_path + '/tmp/a.mp4'
        audio_path = save_path + '/tmp/b.mp3'
        command = f'ffmpeg/bin/ffmpeg.exe -i {video_path} -i {audio_path} -acodec copy -vcodec copy {file_path}'
        Popen(command, creationflags=CREATE_NO_WINDOW)

    def get_name(self):
        """
        获取视频bvid md5值
        """
        return hashlib.md5(self.url.encode('utf-8')).hexdigest()


"""
====================================歌曲====================================
"""
class CloudMusic:
    def __init__(self, id) -> None:
        """下载网易云音乐的歌曲,使用cloudmusic"""
        self.id = id
        
    def download(self, path):
        """下载歌曲"""
        tempMusic = cloudmusic.getMusic(self.id)
        tempMusic.download(dirs=path)