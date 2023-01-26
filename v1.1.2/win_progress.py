# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'downloadProgress.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

"""
 
author: Skyler Sun
create date: 2022-12-05 Monday
weather: haze(霾)
script name: win_progress.py

"""
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BilibiliWin(object):
    def setupUi(self, BilibiliWin):
        BilibiliWin.setObjectName("BilibiliWin")
        BilibiliWin.resize(351, 49)
        BilibiliWin.move(30, 30)
        BilibiliWin.setFixedSize(351, 49)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BilibiliWin.setWindowIcon(icon)
        self.progressBar = QtWidgets.QProgressBar(BilibiliWin)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 330, 25))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMinimum(0)

        self.retranslateUi(BilibiliWin)
        QtCore.QMetaObject.connectSlotsByName(BilibiliWin)

    def retranslateUi(self, BilibiliWin):
        _translate = QtCore.QCoreApplication.translate
        BilibiliWin.setWindowTitle(_translate("BilibiliWin", "Sk Getter下载进度"))
        BilibiliWin.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)        
        
    def setProgressMax(self, maxValue:int):
        """设置进度条最大值"""
        self.progressBar.setMaximum(maxValue)
    
    def setProgressValue(self, value:int):
        """设置进度条当前进度"""
        self.progressBar.setValue(value)
