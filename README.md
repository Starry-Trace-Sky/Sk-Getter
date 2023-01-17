# Sk Getter

## 软件介绍
功能: 下载部分平台的视频,音乐(没错, 就是这么简洁@^_^@)
至于软件名, Sk取自作者英文名Skyler, Getter应该都知道吧
因为想更注重实用性, 界面就写得很简洁

## 安装教程

1.  [点击我下载最新版](https://gitee.com/skyler-sun/sk-getter/releases/download/v0.0.3/SkGetter_v003.7z)
2. [所有版本下载（蓝奏云链接）](https://skyler.lanzouo.com/b03pox9sd)提取密码:57m7
3. 下载完成并解压后, 双击main.exe即可打开
4. **切记第一次运行先设置保存路径!!!**
5. 软件第一次打开可能会遇到自动退出的现象,多试几次就好了

## 使用说明

![软件截图1](2022-12-31_213256.png)
![软件截图2](2022-12-31_213320.png)

1.  本软件仅供学习研究及日常使用
2.  软件关闭后出现的"main.exe已停止工作"是正常情况,请忽略
3. 对于下载视频功能, Bilibili除大会员视频外大部分都能下载
4. 下载安装使用本软件就代表用户仔细阅读并同意[软件协议MIT License](https://gitee.com/skyler-sun/sk-getter/blob/master/LICENSE)

![停止工作截图](2022-12-31_213500.png)

------------


对于**网易云音乐**黑胶和非黑胶歌曲下载, 链接获取方式如下

![网易云音乐](cloudmusic.png)


![网易云音乐勾画](cloudmusic_high.png)


------------


### 腾讯视频下载功能
##### 第一步:下载配置webdriver
1. **确定浏览器**
**Microsoft Edge**, **Firefox**, **Chrome**之中的任意一个(若没有,请自行安装), 推荐Microsoft Edge. ~~其他浏览器没测试过>_<~~
2. **确定浏览器版本**, 下面给出**Microsoft Edge**的确定方法 (其他浏览器类似)

打开浏览器

![打开浏览器](t1.png)

打开设置

![打开设置](t2.png)

点击**关于Microsoft Edge**并记住**浏览器版本**(tips:可以写下来或记在电脑上)

![点击关于Microsoft Edge](t3.png)

到这里你已经成功了一半了@^_^@接下来是下载webdriver[点这里打开下载页面](https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/ "是")
例如我的浏览器版本是**109.0.1518.55**系统为**64位**,就点这个(一般系统都是64位)

![下载webdriver](t4.png)

下载完成后是这个样子滴

![下载完成](t5.png)

因为是zip文件,就把他解压出来,然后是这样

![解压webdriver](t6.png)

Driver_Notes文件夹是文档说明,可以直接删掉
重要的是**msedgedriver.exe**文件,我们鼠标右键复制它
然后根据下面这张**软件目录结构思维导图**找到**browserDriver**文件夹

![软件目录结构](catalogueStructure.png)

粘贴到里面就可以了
成功后是这个样子

![复制粘贴webdriver](t7.png)

#### 到这里就算安装配置完成了,祝贺祝贺!@^_^@!

关于这个功能你需要了解的事情
- 暂不支持批量下载, 请一个一个来
- 有的视频可能等很久都没反应, 请关闭软件后重试几次
- 开始下载后出现的黑色窗口显示的是webdriver启动的浏览器的日志,最小化该窗口即可[**切记不要关闭该窗口,否则会导致下载失败**]

------------


## 软件实现原理
采用正则表达式匹配链接,requests构造请求头并下载文件
使用开源ffmpeg合并视频和音频
对于腾讯视频的获取,接口来源如下(xxx为填充的腾讯视频链接)
https://jx.jsonplayer.com/player/?url=xxx

本软件使用的第三方库如下
cloudmusic 0.1.0
pyquery   1.4.3
requests  2.28.1
PyQt      5.15.4
使用pyqt desinger对窗口进行设计

[style.qss样式来源](https://www.programmerall.com/article/26091298015/)

## 联系作者
邮箱:3385213313@qq.com