# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2023-01-22 Sunday
weather: sunny
script name: StandardClass.py

"""
from os.path import exists

from showTk import showTk
from writeError import writeError


class StandardClass:
    """标准类"""
    def __init__(self) -> None:
        self.status = False
        self.proxyStatus = True
    
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
            if exists('browserDriver/geckodriver.exe'):
                print('firefox webdriver found')
                if self.proxyStatus:
                    from seleniumwire.webdriver import Firefox
                    from selenium.webdriver.firefox.options import Options
                    self.opt = Options()
                    self.opt.add_argument('--headless')
                    self.driver = Firefox(executable_path='browserDriver/geckodriver', options=self.opt)
                else:
                    from selenium.webdriver import Firefox
                    self.driver = Firefox(executable_path='browserDriver/geckodriver')
                self.driver.get("about:blank")
                self.status = True
            # 检查Edge
            elif exists('browserDriver/msedgedriver.exe'):
                print('edge webdriver found')
                # 代理开启时
                if self.proxyStatus:
                    from seleniumwire.webdriver import Edge
                    from selenium.webdriver.edge.options import Options
                    self.opt = Options()
                    self.opt.use_chromium = True
                    self.opt.add_argument('--headless') # 无头模式，不显示窗口
                    self.opt.add_argument('--disable-features=HideToolbar') # 隐藏工具栏
                    self.opt.add_argument('--hide-scrollbars')  # 隐藏滚动条
                    self.opt.add_argument('--disable-infobars')  # 禁用信息栏
                    self.opt.add_argument('--disable-gpu')  # 禁用GPU加速
                    self.opt.add_argument('--disable-dev-shm-usage')  # 禁用 /dev/shm 使用
                    self.opt.add_argument('--disable-setuid-sandbox')  # 禁用 setuid 沙箱
                    self.opt.add_argument('--disable-extensions')  # 禁用扩展程序
                    self.opt.add_argument('--no-sandbox')  # 禁用沙箱
                    self.opt.add_argument('--disable-features=TranslateUI')
                    self.driver = Edge(executable_path='browserDriver/msedgedriver.exe', options=self.opt)
                # 代理关闭时
                else:
                    from selenium.webdriver import Edge
                    from selenium.webdriver.edge.options import Options
                    self.opt = Options()
                    self.opt.use_chromium = True
                    self.opt.add_argument('--auto-hide-toolbar')
                    self.opt.add_argument('--disable-features=HideToolbar') # 隐藏工具栏
                    self.opt.add_argument('--hide-scrollbars')  # 隐藏滚动条
                    self.opt.add_argument('--disable-infobars')  # 禁用信息栏
                    self.opt.add_argument('--disable-gpu')  # 禁用GPU加速
                    self.opt.add_argument('--disable-dev-shm-usage')  # 禁用 /dev/shm 使用
                    self.opt.add_argument('--disable-setuid-sandbox')  # 禁用 setuid 沙箱
                    self.opt.add_argument('--disable-extensions')  # 禁用扩展程序
                    self.opt.add_argument('--no-sandbox')  # 禁用沙箱
                    self.opt.add_argument('--disable-features=TranslateUI')
                    # 禁用共享内存
                    self.opt.add_argument('--disable-dev-shm-usage')
                    self.driver = Edge(executable_path='browserDriver/msedgedriver.exe', options=self.opt)
                self.driver.get('about:blank')
                self.status = True
            # 检查Chrome
            elif exists('browserDriver/chromedriver.exe'):
                print('chrome webdriver found')
                if self.proxyStatus:
                    from seleniumwire.webdriver import Chrome
                    from selenium.webdriver.chrome.options import Options
                    self.opt = Options()
                    self.opt.add_argument('--headless')
                    self.driver = Chrome(executable_path='browserDriver/chromedriver', options=self.opt)
                else:
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
            writeError('@_@未知错误,很可能是webdriver与您的浏览器版本不匹配,稍后为您打开错误日志')
