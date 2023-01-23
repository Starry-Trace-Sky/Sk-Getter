# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-20 Friday
weather: sunny
script name: autoWebdriver.py

"""
import os
import re
import zipfile

import requests


class autoWebdriver():
    def __init__(self, browser: str, configPath: str) -> None:
        """
        自动配置webdriver
        参数:
        browser: 'edge'/'chrome'/'firefox
        """
        self.browser = browser
        self.edgeVersionFile = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.VisualElementsManifest.xml'
        self.browserVersion = None
        self.edgeWebdriverUrl = None
        self.configPath = configPath
        
    def downloadWebdriver(self):
        """下载Webdriver"""
        if self.browser == 'edge':
            # 若浏览器为edge
            conn = requests.get(self.edgeWebdriverUrl)
            if conn.status_code == 200:
                # 下载成功
                with open(self.configPath + 'edgeWebdriver.zip', 'wb') as f:
                    f.write(conn.content)
                return True
            else:
                # 下载失败
                return False
        
    def queryEdgeVersion(self):
        """查询edge浏览器版本"""
        if os.path.exists(self.edgeVersionFile):
            with open(self.edgeVersionFile) as f:
                fileContent = f.readlines()
            fileContent = fileContent[3]
            # 正则匹配提取版本号
            fileContent = fileContent.replace('\\', '/')
            fileContent = re.findall('.*?[=]\'(.*?)/', fileContent)
            try:
                self.browserVersion = fileContent[0]
                print('浏览器版本为:', self.browserVersion)
                return True
            except IndexError:
                return 'IndexError'
        else:
            return 'FileNotFound'

    def updateEdgeUrl(self):
        """更新Edge Webdriver链接"""
        self.edgeWebdriverUrl = f'https://msedgedriver.azureedge.net/{self.browserVersion}/edgedriver_win64.zip'

    def extractZip(self):
        """解压zip文件"""
        if self.browser == 'edge':
            zip = zipfile.ZipFile(self.configPath + 'edgeWebdriver.zip', 'r')
            for file in zip.filelist:
                if file.filename == 'msedgedriver.exe':
                    #解压目标webdriver
                    zip.extract(file, self.configPath)
                    #删除zip
                    zip.close()
                    os.remove(self.configPath + 'edgeWebdriver.zip')
                    return True
            return False
