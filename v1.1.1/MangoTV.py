# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-22 Sunday
weather: sunny
script name: MangoTV.py

"""
from re import findall
from time import strftime
from threading import Thread
from subprocess import Popen, CREATE_NO_WINDOW

from requests import get
from query import update_config
from showTk import showTk
from writeError import writeError
from writeHistory import writeHistory
from StandardClass import StandardClass


class MangoTV(StandardClass):
    def __init__(self, originUrl:str) -> None:
        """
        芒果tv视频下载
        originUrl:原视频链接
        """
        super().__init__()
        self.originUrl = originUrl
        self.apiUrl = f'https://jx.jsonplayer.com/player/?url={self.originUrl}'
        self.targetRequest = None
        self.checkBrowser()
        self.apiHeaders = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
            'connection':'keep-alive'
        }
    
    def download(self, savePath):
        print(f'芒果tv链接为\n{self.originUrl}')
        writeHistory(f'下载芒果tv:\n{self.originUrl}')
        if self.status:
            # 设置代理过滤
            self.driver.scopes = ['.*mgtv.*']
            self.driver.get(self.apiUrl)
            while self.status:
                for i in self.driver.requests:
                    if 'titan.mgtv.com' in i.host:
                        self.targetRequest = i
                        self.driver.quit()
                        self.status = False
                        break
            showTk(0, '信息', '成功获取到芒果TV m3u8链接')
            try:
                conn = get(self.targetRequest, headers=self.apiHeaders)
            except:
                writeError('下载m3u8数据失败,稍后为您打开错误日志')
            targetUrl = self.targetRequest.url
            try:
                targetUrl = findall('(.*?)ts[/]', targetUrl)[0]
            except:
                writeError('下载m3u8成功,但是提取视频链接失败,稍后为您打开错误日志')
            targetUrl += 'ts/'
            print(f'targetUrl:{targetUrl}')
            if conn.status_code == 200:
                apiData = conn.text
                apiData = apiData.split('\n')
                videoDataUrl = []
                update_config('d/config/download.json', 'value', 0)
                for i in apiData:
                    if 'ts' in i:
                        videoDataUrl.append(targetUrl + i)
                d_th_l = []
                for (num, i) in enumerate(videoDataUrl):
                    # 创建下载ts线程池
                    def d_th_f(*args):
                        try:
                            videoDataConn = get(args[1], headers=self.apiHeaders)
                            with open(savePath + '/' + str(args[0]) + '.ts', 'wb') as f:
                                f.write(videoDataConn.content)
                        except:
                            writeError('下载或保存时出错,稍后为您打开错误日志')
                    d_th = Thread(target=d_th_f, args=(num,i))
                    d_th_l.append(d_th)
                # 列表切片,30个线程同时下载
                temp = 0
                ttemp = 0
                update_config('d/config/download.json', 'max', len(d_th_l))
                while True:
                    templ = d_th_l[temp:temp+30:]
                    if templ != []:
                        temp += 30
                        for i in templ:
                            # 开始线程池
                            i.start()
                        for i in templ:
                            # 等待线程全部完成
                            i.join()
                            ttemp += 1
                            update_config('d/config/download.json', 'value', ttemp)
                    else:
                        break
                # 合并ts视频
                now = strftime('%Y%m%d%H%M%S')
                with open('d/ffmpeg/m3u8.txt', 'w') as f:
                    pass
                for i in range(len(d_th_l)):
                    with open('d/ffmpeg/m3u8.txt', 'a') as f:
                        f.write(f'file  {savePath}/' + str(i) + '.ts\n')
                ccmd = f'd/ffmpeg/ffmpeg.exe -f concat -safe 0 -i d/ffmpeg/m3u8.txt -vcodec copy -acodec copy {savePath}/{now}.mp4'
                Popen(ccmd, creationflags=CREATE_NO_WINDOW)
            else:
                showTk(2, '错误', '请求分片视频失败,请重试')