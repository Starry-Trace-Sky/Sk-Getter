# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-22 Sunday
weather: sunny
script name: Bilibili.py

"""
import re
import os
import hashlib
from json import loads
from threading import Thread
from subprocess import Popen, CREATE_NO_WINDOW

import requests
from query import update_config
from pyquery import PyQuery as pq
from writeHistory import writeHistory
from StandardClass import StandardClass
from selenium.webdriver.common.by import By


class Bilibili(StandardClass):
    def __init__(self, source_url, savePath) -> None:
        """
        初始化设置
        source_url: 分享出来的bilibili链接
        """
        super().__init__()
        self.proxyStatus = False
        self.url = source_url
        self.bvid = re.findall('https://www.bilibili.com/video/(.*?)/', self.url)[0]
        self.api_get_aid_url = f'https://api.bilibili.com/x/web-interface/view?bvid={self.bvid}'
        self.api_get_cid_url = f'https://api.bilibili.com/x/player/pagelist?bvid={self.bvid}&jsonp=jsonp'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
            'origin':'https://www.bilibili.com',
            'referer':'https://www.bilibili.com',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'sec-ch-ua':'"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'same-origin',
            'sec-fetch-user':'?1',
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
        self.activate = True
        self.savePath = savePath

    def get_one_link(self):
        """获取视频,音频链接"""
        print('get_one_link')
        print(self.url)
        print(self.headers)
        con = requests.get(self.url, headers=self.headers)
        
        if con.status_code == 200:
            data = pq(con.text)
            data = data('script')
            for i in data:
                if '高清' in i.text:
                    data = i.text
                    break
            data = list(data)
            for i in range(20):
                data.pop(0)
            data = ''.join(data)
            data = loads(data)
            video_url = data['data']['dash']['video'][0]['baseUrl']
            audio_url = data['data']['dash']['audio'][0]['baseUrl']
            data = {'video_url':video_url, 'audio_url':audio_url}
            writeHistory(f'获取到B站视频,原链接为{self.url}')
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
        print(f"开始下载,链接如下:\n{input_url}")
        conn = s.get(input_url, headers=self.headers1, stream=True)
        connn = s.head(input_url, headers=self.headers1)

        if conn.status_code == 200 and connn.status_code == 200:
            print('获取成功,开始保存')
            fileSize = int(connn.headers.get('Content-Length'))
            update_config('d/config/download.json', 'max', fileSize)
            update_config('d/config/download.json', 'value', 0)
            with open(self.savePath + '/tmp/' + filename, 'wb') as f:
                for chunck in conn.iter_content(chunk_size=1024*1024*5):
                    if chunck:
                        f.write(chunck)
                        currentSize = os.path.getsize(self.savePath + '/tmp/' + filename)
                        update_config('d/config/download.json', 'value', currentSize)
            print("保存成功")

    def merge(self, filename:str):
        """
        合并音频和视频,删除源文件
        """
        print("合并B站视频和音频")
        file_path = self.savePath + '/' + filename
        video_path = self.savePath + '/tmp/a.mp4'
        audio_path = self.savePath + '/tmp/b.mp3'
        command = f'd/ffmpeg/ffmpeg.exe -i {video_path} -i {audio_path} -acodec copy -vcodec copy {file_path}'
        Popen(command, creationflags=CREATE_NO_WINDOW)

    def get_name(self):
        """
        获取视频bvid md5值
        """
        return hashlib.md5(self.url.encode('utf-8')).hexdigest()
    
    def setCookies(self):
        """
        设置浏览器cookies, 直至用户登录为止
        """
        while self.activate:
            tpCookies = self.driver.get_cookies()
            for i in tpCookies:
                if i['name'] == 'DedeUserID':
                    # 检测到登录
                    ck = ''
                    for ii in tpCookies:
                        ck += ii['name'] + '=' + ii['value'] + '; '
                    self.headers['Cookie'] = ck
                    self.headers1['Cookie'] = ck
                    self.activate = False
                    break
    
    def login(self):
        """
        登录
        """
        self.checkBrowser()
        if self.status:
            print('Start to request bilibili.com')
            self.driver.get('https://www.bilibili.com')
            self.driver.implicitly_wait(120)
            login_bt = self.driver.find_element(By.XPATH, '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div[1]/div')
            login_bt.click()
            setCookies_th = Thread(target=self.setCookies, daemon=True)
            setCookies_th.start()
            while True:
                if not self.activate:
                    self.driver.quit()
                    print('退出浏览器')
                    break