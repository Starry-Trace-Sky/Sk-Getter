# Sk Getter

#### 软件介绍
功能: 下载部分平台的视频,音乐(没错, 就是这么简洁@^_^@)
至于软件名, Sk取自作者英文名Skyler, Getter应该都知道吧
作者美术实在不行, 界面就写得很简洁

#### 安装教程

1.  [点击我下载最新版](https://gitee.com/skyler-sun/sk-getter/releases/download/v0.0.1/SkGetter_v001.7z)
2. [所有版本下载](https://skyler.lanzouo.com/b03pox9sd)提取密码:57m7
3. 下载完成并解压后, 双击main.exe即可打开
4. **切记第一次运行先设置保存路径!!!**

#### 使用说明

1.  本软件仅供学习研究, 请勿使用本软件做违法乱纪的事
2.  软件责任在[MIT License](https://gitee.com/skyler-sun/sk-getter/blob/master/LICENSE)写明
3.  api.txt会不定期更新, 若发现软件无法下载视频或音乐,请点击菜单栏的"设置->更新接口"(2022/12/31 周六 作者的话,api.txt没有实质作用,软件GUI没时间删除"更新接口"菜单了,不好意思)
4. 对于下载视频功能, Bilibili除大会员视频外大部分都能下载
5. 软件关闭后出现的"main.exe已停止工作"是正常情况,请忽略

#### 软件实现原理
采用正则表达式匹配链接,requests构造请求头并下载文件
使用开源ffmpeg合并视频和音频

本软件使用的第三方库如下
cloudmusic
pyquery   1.4.3
requests  2.28.1
PyQt      5.15.4
使用pyqt desinger对窗口进行设计
另外感谢国外一大佬提供的style.qss样式美化

[style.qss样式来源链接](https://www.programmerall.com/article/26091298015/)