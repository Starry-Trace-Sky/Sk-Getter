# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-22 Sunday
weather: sunny
script name: Bilibili.py

"""
from re import findall
from os.path import getsize
import sys
from hashlib import md5
from json import loads
from threading import Thread
from subprocess import call, CREATE_NO_WINDOW

from requests import get, session
from showTk import showTk
from query import update_config
from writeError import writeError
from pyquery import PyQuery as pq
from writeHistory import writeHistory
from StandardClass import StandardClass
from selenium.webdriver.common.by import By


class Bilibili(StandardClass):
    def __init__(self, source_url, savePath, isEp=False) -> None:
        """
        初始化设置
        source_url: 分享出来的bilibili链接
        """
        super().__init__()
        self.isEp = isEp # 是否为番剧下载
        self.proxyStatus = False # 是否为浏览器提供代理
        self.url = source_url
        self.activate = True # 浏览器登录信号标志
        self.savePath = savePath
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
        self.headers2 = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
            'origin':'https://www.bilibili.com',
            'referer':'https://www.bilibili.com'
        }

    def getLinks(self):
        """获取视频,音频链接"""
        print('用户输入bilibili链接如下:')
        print(self.url)
        patternList = findall('ep(.*?)[?]', self.url)
        epId = None # 初始化
        # 判断为番剧链接
        if (patternList != []):
            epId = patternList[0]
            try:
                epId = int(epId)
            except:
                pass
        if isinstance(epId, int):
            # 匹配成功
            if 'Cookie' not in self.headers1:
                showTk(2, '错误', '检测到您还没有登录,请先登录再下载番剧哦~(bilibili有检测机制,无奈)')
                sys.exit()
            self.apiEpUrl = f'https://api.bilibili.com/pgc/player/web/playurl?support_multi_audio=true&ep_id={epId}&qn=80&fnver=0&fnval=4048&fourk=1'
            try:
                con = get(self.apiEpUrl, headers=self.headers2)
            except:
                writeError('下载时遇到错误,稍后为您打开错误日志')
            # 请求成功
            if con.status_code == 200:
                try:
                    EpVideoUrl = con.json()['result']['dash']['video'][0]['base_url']
                    EpAudioUrl = con.json()['result']['dash']['audio'][0]['base_url']
                except:
                    writeError('数据格式变化,稍后为您打开错误日志')
                data = {'video_url':EpVideoUrl, 'audio_url':EpAudioUrl}
                return data
            else:
                showTk(f'请求成功,但状态码为{con.status_code}')
                
            return None
        else:
            try:
                con = get(self.url, headers=self.headers)
            except:
                writeError('获取目标链接失败,稍后为您打开错误日志')

            if con.status_code == 200:
                data = pq(con.text)
                data = data('script')
                for i in data:
                    if i.text != None:
                        if '高清' in i.text:
                            data = i.text
                            break
                data = list(data)
                for i in range(20):
                    data.pop(0)
                data = ''.join(data)
                data = loads(data)
                try:
                    video_url = data['data']['dash']['video'][0]['baseUrl']
                    audio_url = data['data']['dash']['audio'][0]['baseUrl']
                except:
                    writeError('下载成功,但是提取视频音频链接失败,稍后为您打开错误日志')
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
        s = session()
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
                        currentSize = getsize(self.savePath + '/tmp/' + filename)
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
        call(command, creationflags=CREATE_NO_WINDOW)

    def get_name(self):
        """
        获取视频url md5值
        """
        return md5(self.url.encode('utf-8')).hexdigest()
    
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
                    self.headers2['Cookie'] = ck
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