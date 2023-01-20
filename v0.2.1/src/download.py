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
import traceback
import sys
from json import loads
from time import strftimefrom time import strftime
from threading import Thread
from subprocess import Popen, CREATE_NO_WINDOW

import requests
import cloudmusic
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from writeHistory import writeHistory
from showTk import showTk


def openSave():
    """打开保存位置"""
    path = save_path.replace('/', '\\')
    Popen(f'explorer.exe {path}', creationflags=CREATE_NO_WINDOW)

"""
====================================视频====================================
"""
class Bilibili:
    def __init__(self, source_url) -> None:
        """
        初始化设置
        source_url: 分享出来的bilibili链接
        """
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
        #self.url = 'https://api.bilibili.com/x/player/playurl?fnver=0&fnval=4048&fourk=1&voice_balance=1&qn=80&'
        #self.url += f'avid={self.avid}&cid={self.cid}'
        self.status = False
        self.activate = True

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

        if conn.status_code == 200:
            print('获取成功,开始保存')
            with open(save_path + '/tmp/' + filename, 'wb') as f:
                for chunck in conn.iter_content(chunk_size=100):
                    if chunck:
                        f.write(chunck)
            print("保存成功")

    def merge(self, filename:str):
        """
        合并音频和视频,删除源文件
        """
        print("合并B站视频和音频")
        file_path = save_path + '/' + filename
        video_path = save_path + '/tmp/a.mp4'
        audio_path = save_path + '/tmp/b.mp3'
        command = f'ffmpeg/ffmpeg.exe -i {video_path} -i {audio_path} -acodec copy -vcodec copy {file_path}'
        Popen(command, creationflags=CREATE_NO_WINDOW)

    def get_name(self):
        """
        获取视频bvid md5值
        """
        return hashlib.md5(self.url.encode('utf-8')).hexdigest()
    
    def checkBrowser(self):
        """
        检查是否安装支持的浏览器
        selenium支持浏览器如下
        Chrome
        Edge
        IE
        Safari(windows不支持)
        """
        try:
            # 检查Firefox
            if os.path.exists('browserDriver/geckodriver.exe'):
                print('firefox webdriver found')
                from selenium.webdriver import Firefox
                self.driver = Firefox(executable_path='browserDriver/geckodriver')
                self.driver.get("about:blank")
                self.status = True
            # 检查Edge
            elif os.path.exists('browserDriver/msedgedriver.exe'):
                print('edge webdriver found')
                from selenium.webdriver import Edge
                self.driver = Edge(executable_path='browserDriver/msedgedriver.exe')
                self.driver.get('about:blank')
                self.status = True
            # 检查Chrome
            elif os.path.exists('browserDriver/chromedriver.exe'):
                print('chrome webdriver found')
                from selenium.webdriver import Chrome
                self.driver = Chrome(executable_path='browserDriver/chromedriver')
                self.driver.get('about:blank')
                self.status = True
            # 未找到webdriver
            else:
                print('webdriver not found')
                showTk(2, '错误', '@_@未找到支持的webdriver文件')
        except:
            # 错误处理
            showTk(2, '错误', '@_@未知错误,很可能是webdriver与您的浏览器版本不匹配,具体日志已写入本软件所在目录下的error.log')
            now = '[' + strftime('%Y') + '/' + strftime('%m') + '/' + strftime('%d')
            now += ' ' + strftime('%H') + ':' + strftime('%M') + ':' + strftime('%S') + ']'
            with open('error.log', 'a') as f:
                f.write(now + '\n' + traceback.format_exc() + '\n')
            Popen('notepad.exe error.log', creationflags=CREATE_NO_WINDOW)
    
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

class VTencent:
    def __init__(self, url: str) -> None:
        """
        腾讯视频下载
        参数
        url: 视频链接
        """
        self.status = False # 初始化就绪标志
        self.url = url
        self.api_url = f'https://jx.jsonplayer.com/player/?url={self.url}'
        self.target_request = None
        self.checkBrowser()
    
    def checkBrowser(self):
        """
        检查是否安装支持的浏览器
        selenium支持浏览器如下
        Chrome
        Edge
        IE
        Safari(windows不支持)
        """
        try:
            # 检查Firefox
            if os.path.exists('browserDriver/geckodriver.exe'):
                print('firefox webdriver found')
                from seleniumwire.webdriver import Firefox
                from selenium.webdriver.firefox.options import Options
                self.options = Options()
                self.options.add_argument('-headless')
                self.driver = Firefox(executable_path='browserDriver/geckodriver', options=self.options)
                self.driver.get("about:blank")
                self.status = True
            # 检查Edge
            elif os.path.exists('browserDriver/msedgedriver.exe'):
                print('edge webdriver found')
                from seleniumwire.webdriver import Edge
                from selenium.webdriver.edge.options import Options
                self.options = Options()
                self.options.add_argument('-headless')
                self.driver = Edge(executable_path='browserDriver/msedgedriver', options=self.options)
                self.driver.get('about:blank')
                self.status = True
            # 检查Chrome
            elif os.path.exists('browserDriver/chromedriver.exe'):
                print('chrome webdriver found')
                from seleniumwire.webdriver import Chrome
                from selenium.webdriver.chrome.options import Options
                self.options = Options()
                self.options.add_argument('-headless')
                self.driver = Chrome(executable_path='browserDriver/chromedriver', options=self.options)
                self.driver.get('about:blank')
                self.status = True
            # 未找到webdriver
            else:
                print('webdriver not found')
                showTk(2, '错误', '@_@未找到支持的webdriver文件')
        except:
            # 错误处理
            showTk(2, '错误', '@_@未知错误,很可能是webdriver与您的浏览器版本不匹配,具体日志已写入本软件所在目录下的error.log')
            from time import strftime
            now = '[' + strftime('%Y') + '/' + strftime('%m') + '/' + strftime('%d')
            now += ' ' + strftime('%H') + ':' + strftime('%M') + ':' + strftime('%S') + ']'
            with open('error.log', 'a') as f:
                f.write(now + '\n' + traceback.format_exc() + '\n')
            Popen('notepad.exe error.log', creationflags=CREATE_NO_WINDOW)
            
    def download(self):
        """
        开始下载
        """
        if self.status:
            print(f'start to request\n{self.api_url}')
            # 设置代理过滤
            self.driver.scopes = ['.*om.*']
            self.driver.get(self.api_url)
            self.driver.implicitly_wait(120)
            while self.status:
                for i in self.driver.requests:
                    # 提取目标url
                    if i.host == 'om.tc.qq.com':
                        header = i.headers._headers
                        for (key, value) in header:
                            if key.lower() == 'range':
                                # 提取到目标url
                                self.target_request = i
                                self.status = False
                                # 关闭浏览器,清理抓包数据
                                self.driver.requests.clear()
                                self.driver.quit()
                                showTk(0, '信息', '^_^ 成功获取到视频链接,开始准备下载')
                        break
            if self.target_request:
                self.headers = dict()
                for (key, value) in self.target_request.headers._headers:
                    self.headers[key] = value
                print('Start to download tencent video')
                print('Start to download')

                # 更改请求头分段下载,避免内存过高程序崩溃
                showTk(0, '信息', '开始下载')
                video_request = requests.get(self.target_request.url, headers=self.headers, stream=True)
                now = strftime('%Y%m%d%H%M%S')
                with open(f'{save_path}/{now}.mp4', 'wb') as f:
                    for chunck in video_request.iter_content(100):
                        if chunck:
                            f.write(chunck)
                            chunck = None
                showTk(0, '信息', '下载完成^o^,清理完成缓存后会自动打开文件夹')
                del chunck # 清理缓存
                print('Save successful')
                writeHistory(f'下载腾讯视频,链接如下\n{self.url}')
                Popen('taskkill /f /im download.exe', shell=True, creationflags=CREATE_NO_WINDOW)
            else:
                showTk(2, '错误', '@_@ 未查询到接口信息,请先重试,若多次出现该状况请查看软件地址或联系作者')
                self.driver.quit()
            print('Driver closed')


"""
====================================歌曲====================================
"""
class CloudMusic:
    def __init__(self, url) -> None:
        """下载网易云音乐的歌曲,使用cloudmusic"""
        self.url = url
        self.id = re.findall('.*?id=(.*)', self.url)
        
    def download(self):
        """下载歌曲"""
        tempMusic = cloudmusic.getMusic(self.id)
        tempMusic.download(dirs=save_path)
        writeHistory(f'下载网易云音乐歌曲,链接为{self.url}')


patternsList = sys.argv
print(patternsList)
save_path = patternsList[3]
# 传参运行
if patternsList[1] == 'bilibili':
    downloader = Bilibili(patternsList[2])
    urls = downloader.get_one_link()
    if urls:
        tips = "检测为bilibili链接,默认下载标清画质,更高画质需要登录[要求配置webdriver(见软件地址)](本软件不会收"
        tips += "集您的任何信息,源码download.py可查),下载完成后会-自动打"
        tips += "开文件夹,文件名经过md5加密(看起来像乱码的mp4)###点击确认下载高清画"
        tips += "质,取消下载标清画质"
        decision = showTk(3, '提示', tips)
        if decision:
            # 下载高清画质
            print('下载高清画质')
            downloader.login()
            urls = downloader.get_one_link()
        else:
            # 下载标清画质
            print('下载标清画质')
        downloader.download(urls['video_url'], 'a.mp4')
        downloader.download(urls['audio_url'], 'b.mp3')
        videoName = downloader.get_name()
        downloader.merge(f'{videoName}.mp4')
        openSave()
    else:
        showTk(2, '错误', '未获取到视频链接, 请重复尝试, 若多次失败, 请点击"帮助"->"软件地址"查看最新消息或询问作者')

elif patternsList[1] == 'tencent':
    downloader = VTencent(patternsList[2])
    downloader.download()
    openSave()

elif patternsList[1] == 'cloudmusic':
    showTk(0, '信息', '下载开始')
    downloader = CloudMusic(patternsList[2])
    downloader.download()
    openSave()
