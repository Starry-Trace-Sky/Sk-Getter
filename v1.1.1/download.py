# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2022-12-05 Monday
weather: small rain
script name: download.py

"""
from subprocess import Popen, CREATE_NO_WINDOW

from showTk import showTk
from query import query_config
from CloudMusic import CloudMusic
from VTencent import VTencent
from BiliBili import Bilibili
from MangoTV import MangoTV


def openSave():
    """打开保存位置"""
    path = save_path.replace('/', '\\')
    Popen(f'explorer.exe {path}', creationflags=CREATE_NO_WINDOW)

config = query_config('d/config/settings.json')
save_path = config['save_path']
save_path = list(save_path)
if save_path[-1] == '/':
    save_path.pop()
save_path = ''.join(save_path)
videoType = config['videoType']
videoUrl = config['videoUrl']
# 传参运行
if __name__ == '__main__':
    if videoType == 'bilibili':
        downloader = Bilibili(videoUrl, save_path)
        tips = "检测为bilibili链接,默认下载标清画质,更高画质和番剧下载需要登录"
        tips += "[要求配置webdriver(见软件地址)]下载完成后会自动打"
        tips += "开文件夹,文件名经过md5加密(看起来像乱码的mp4)###点击确认下载高清画"
        tips += "质,取消下载标清画质"
        decision = showTk(3, '提示', tips)
        if decision:
            # 下载高清画质
            print('下载高清画质或番剧')
            downloader.login()
            urls = downloader.getLinks()
        else:
            # 下载标清画质
            print('下载标清画质')
            urls = downloader.getLinks()
        if urls:
            downloader.download(urls['video_url'], 'a.mp4')
            downloader.download(urls['audio_url'], 'b.mp3')
            videoName = downloader.get_name()
            showTk(0, '信息', '下载完成,开始合并视频和音频')
            downloader.merge(f'{videoName}.mp4')
            openSave()
        else:
            showTk(2, '错误', '链接获取失败,请重新尝试,若情况依旧,请查看菜单栏的"帮助"=>"软件地址"')

    elif videoType == 'tencent':
        downloader = VTencent(videoUrl)
        downloader.download(save_path)
        openSave()

    elif videoType == 'cloudmusic':
        showTk(0, '信息', '下载开始')
        downloader = CloudMusic(videoUrl)
        downloader.download(save_path)
        openSave()

    elif videoType == 'mgtv':
        #检测为芒果tv
        downloader = MangoTV(videoUrl)
        downloader.download(save_path)
        openSave()
