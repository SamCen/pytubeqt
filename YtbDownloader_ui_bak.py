# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'YtbDownloader.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QRect,QThread,Signal)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QProgressBar,
    QPushButton, QWidget,QMessageBox,QFileDialog)
from download import YouTubeDownloader
import random,time
class ProgressUpdateThread(QObject):
    """
    后台线程，模拟更新数据
    """
    finished = Signal(int)
    progress = Signal(int)
    stop = 0
    # update_success = Signal()  # 定义信号，用于更新成功后的操作
    value = 0
    def updateProgressWork(self):
        while True:
            if  self.stop == 0:
                if self.value <= 90:
                    self.value += random.randint(3,9)
                    self.progress.emit(self.value)
                print('当前进度' + str(self.value))
                QApplication.processEvents()
                time.sleep(1)
            else:
                print('收到下载结果跳出更新进度条循环')
                print('准备发送的self stop 是' + str(self.stop))
                self.progress.emit(self.stop == 1 and 100 or self.value)
                self.finished.emit(self.stop)
                break
        
        
    def changeStopSign(self,k):
        print('stop call 信号')
        print('change stop sign' + str(k))
        self.stop = k
        if(k == 0):
            self.value = 0
        print('当前stop:' + str(self.stop))
        

class DownloadThread(QObject):
    downSuccess = Signal(int)
    def __init__(self):
        super().__init__()
    def beginDownload(self,params):
        downloader = YouTubeDownloader()
        QApplication.processEvents()
        res = downloader.downloadAct(params['url'],params['path'])
        print('下载结果')
        print(res)
        self.downSuccess.emit(res)  # 发送下载完成信号
class Downloader(QWidget):
    downloadInfoSignal = Signal(dict) #下载需要的url和path信号
    maxProgressSignal = Signal(int)
    callStopSignal = Signal(int)
    def __init__(self) -> None:
        super().__init__()
        self.setupDownloadThread()
        self.setupUpdateProgressThread()
        
    # setupUi
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(720, 480)
        self.url = QLineEdit(Form)
        self.url.setObjectName(u"url")
        self.url.setGeometry(QRect(110, 50, 461, 21))
        self.url.setClearButtonEnabled(True)
        self.path = QLineEdit(Form)
        self.path.setObjectName(u"path")
        self.path.setGeometry(QRect(110, 110, 461, 21))
        self.path.setReadOnly(True)
        self.urlLabel = QLabel(Form)
        self.urlLabel.setObjectName(u"urlLabel")
        self.urlLabel.setGeometry(QRect(30, 50, 66, 16))
        self.pathLabel = QLabel(Form)
        self.pathLabel.setObjectName(u"pathLabel")
        self.pathLabel.setGeometry(QRect(40, 110, 53, 21))
        self.browserBtn = QPushButton(Form)
        self.browserBtn.setObjectName(u"browserBtn")
        self.browserBtn.setGeometry(QRect(590, 110, 75, 23))
        self.stratDownload = QPushButton(Form)
        self.stratDownload.setObjectName(u"stratDownload")
        self.stratDownload.setGeometry(QRect(110, 210, 75, 23))
        self.downloadProgress = QProgressBar(Form)
        self.downloadProgress.setObjectName(u"downloadProgress")
        self.downloadProgress.setGeometry(QRect(110, 160, 501, 23))
        self.downloadProgress.setValue(0)
        self.retranslateUi(Form)
        self.stratDownload.clicked.connect(self.downloadAction)
        self.browserBtn.clicked.connect(self.browserPath)
        QMetaObject.connectSlotsByName(Form)
    # retranslateUi
    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Ytb\u89c6\u9891\u4e0b\u8f7d\u5668", None))
        self.url.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u8981\u4e0b\u8f7d\u7684ytb\u89c6\u9891\u94fe\u63a5", None))
        self.urlLabel.setText(QCoreApplication.translate("Form", u"ytb\u89c6\u9891\u94fe\u63a5", None))
        self.pathLabel.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u5730\u5740", None))
        self.browserBtn.setText(QCoreApplication.translate("Form", u"\u6d4f\u89c8", None))
        self.stratDownload.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u4e0b\u8f7d", None))
    #装载下载线程
    def setupDownloadThread(self):
        self.downThreadInstance = QThread(self)  # 创建一个线程
        self.downThread = DownloadThread()  # 实例化线程类
        self.downThread.moveToThread(self.downThreadInstance)  # 将类移动到线程中运行
        self.downloadInfoSignal.connect(self.downThread.beginDownload)
        self.downThread.downSuccess.connect(self.downSuccessAct)
        print('下载线程装载完成')
    #装载进度条更新线程
    def setupUpdateProgressThread(self):
        self.progressThreadInstance = QThread(self)  # 创建一个线程
        self.progressThread = ProgressUpdateThread()  # 实例化线程类
        self.progressThread.moveToThread(self.progressThreadInstance)  # 将类移动到线程中运行
        self.progressThread.progress.connect(self.updateProgressBarAct)
        self.progressThread.finished.connect(self.stopProgressThread)
        self.maxProgressSignal.connect(self.progressThread.updateProgressWork)
        self.callStopSignal.connect(self.progressThread.changeStopSign)
        print('进度条线程装载完成')
    #开始进度条更新线程
    def startProgressThread(self):
        maxProgress = 98
        print('启动进度条更新线程')
        print('开始方法进度条线程状态:'+str(self.progressThreadInstance.isRunning()))
        self.progressThreadInstance.start()
        self.maxProgressSignal.emit(maxProgress)
        print('开始方法进度条线程状态:'+str(self.progressThreadInstance.isRunning()))
    #更新进度条信号对接方法
    def updateProgressBarAct(self, value):
        self.downloadProgress.setValue(value)
    #下载完成信号对接方法
    def downSuccessAct(self,res):
        print('下载完成对接方法的res是  '+str(res))
        self.callStopSignal.emit(res)
        self.stopDownloadThread(res)
            # QMessageBox.information(self,"下载结果","下载成功")
    #终止下载线程
    def stopDownloadThread(self,res):
        print('准备终止下载线程')
        print('终止方法下载线程状态:'+str(self.downThreadInstance.isRunning()))
        self.downThreadInstance.quit()
        self.downThreadInstance.wait()
        print('终止方法下载线程状态:'+str(self.downThreadInstance.isRunning()))
    #开始下载线程
    def startDownThread(self):
        downloadParams = {'url':self.url.text(),'path':self.path.text()}
        print('启动下载线程')
        self.downloadProgress.setValue(0)
        self.callStopSignal.emit(0)
        self.downThreadInstance.start()
        print('启动方法下载线程状态:'+str(self.downThreadInstance.isRunning()))
        self.downloadInfoSignal.emit(downloadParams)
    #终止进度条线程
    def stopProgressThread(self,res):
        print('准备终止进度条线程')
        print('终止方法进度条线程状态:'+str(self.progressThreadInstance.isRunning()))
        self.progressThreadInstance.quit()
        self.progressThreadInstance.wait()
        print('终止方法进度条线程状态:'+str(self.progressThreadInstance.isRunning()))
        print("终止线程方法收到的res："+str(res))
        if res == 1:
            QMessageBox.information(self,"下载结果","下载成功")
        else:
            QMessageBox.information(self,"下载结果","下载失败")
        self.stratDownload.setEnabled(True)
        self.browserBtn.setEnabled(True)
    #点击下载按钮处理方法
    def downloadAction(self):
        if self.url.text() == '':
            QMessageBox.information(self,"错误","请输入要下载的视频地址")
            return
        if self.path.text() == '':
            QMessageBox.information(self,"错误","请选择保存的路径")
            return
        self.stratDownload.setEnabled(False)
        self.browserBtn.setEnabled(False)
        print('开始下载action')
        self.startDownThread()
        self.startProgressThread()
    def browserPath(self):
        downloadPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.path.setText(str(downloadPath))
