# -*- coding: utf-8 -*-
"""
 
author: Skyler Sun
create date: 2022-10-23 Sunday
weather: sunny
script name: main.py

作者的话: 
这将是一个巨大的项目, 想放弃删文件的时候想想最初为什么要建立文件
正则表达虽然很难, 不也挺过来了吗
cookies, 验证码虽复杂, 总有办法的
既然选择了无言, 那就拿点实际行动吧
既然要做点什么, 那就不要模棱两可喔 @^_^@
就当是高中毕业给所有同学的礼物吧 -_-

"""
import sys
import os

from win_main import MainWindow, app
from win_setting import SettingWindow
from query import query_config, update_config


config = query_config('config/settings.json')


class Main:
    def run(self):
        MainWindow.show()
        app.exec_()


if __name__ == '__main__':
    # 验证设置保存目录是否存在
    if not os.path.exists(config['save_path']):
        try:
            os.mkdir(config['save_path'])
        except:
            pass
    if not os.path.exists(config['save_path'] + '/tmp'):
        try:
            os.mkdir(config['save_path'] + '/tmp')
        except:
            pass
    main = Main()
    main.run()
    sys.exit()