# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-22 Sunday
weather: sunny
script name: VTencent.py

"""
import os
from time import strftime
from subprocess import Popen, CREATE_NO_WINDOW

import requests
from showTk import showTk
from query import update_config
from writeError import writeError
from writeHistory import writeHistory
from StandardClass import StandardClass


class VTencent(StandardClass):
    def __init__(self, url: str) -> None:
        """
        腾讯视频下载
        参数
        url: 视频链接
        """
        super().__init__()
        self.url = url
        self.api_url = f'https://jx.jsonplayer.com/player/?url={self.url}'
        self.target_request = None
        self.checkBrowser()
            
    def download(self, savePath):
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
                try:
                    video_r_header =requests.head(self.target_request.url, headers=self.headers)
                except:
                    writeError('请求文件大小时出错,稍后为您打开错误日志')
                fileSize = int(video_r_header.headers.get('Content-Length'))
                update_config('d/config/download.json', 'max', fileSize)
                update_config('d/config/download.json', 'value', 0)
                try:
                    video_request = requests.get(self.target_request.url, headers=self.headers, stream=True)
                except:
                    writeError('下载出错,稍后为您打开错误日志')
                now = strftime('%Y%m%d%H%M%S')
                with open(f'{savePath}/{now}.mp4', 'wb') as f:
                    for chunck in video_request.iter_content(1024*1024*5):
                        if chunck:
                            f.write(chunck)
                            currentSize = os.path.getsize(f'{savePath}/{now}.mp4')
                            update_config('d/config/download.json', 'value', currentSize)
                showTk(0, '信息', '下载完成^o^,清理完成缓存后会自动打开文件夹')
                del chunck # 清理缓存
                print('Save successful')
                writeHistory(f'下载腾讯视频,链接如下\n{self.url}')
                Popen('taskkill /f /im download.exe', shell=True, creationflags=CREATE_NO_WINDOW)
            else:
                showTk(2, '错误', '@_@ 未查询到接口信息,请先重试,若多次出现该状况请查看软件地址或联系作者')
                self.driver.quit()
            print('Driver closed')