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
import os
from pytube import YouTube
from pytube import exceptions as pytubeException

class ProgressUpdateThread(QObject):
    finished = Signal(int)
    progress = Signal(int)
    def __init__(self):
        super().__init__()
    def updateProgressWork(self,num):
        print('进度条线程update方法接收到的num：'+str(num))
        self.progress.emit(num)
        # if num == 100:
        #     self.showRes(1)
    def showRes(self,res):
        print('发出finished信号，想终止进度条更新进程,res 是'+str(res))
        self.finished.emit(res)

class DownloadThread(QObject):
    downSuccess = Signal(int)
    newPercentage = Signal(int)
    def __init__(self):
        super().__init__()
    def on_progress(self,stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(percentage_of_completion)
        self.newPercentage.emit(int(percentage_of_completion))
    def beginDownload(self,params):
        try:
            # 创建YouTube对象并获取视频流和标题
            video = YouTube(params['url'])
            print('视频限制年龄：'+str(video.check_availability()))
            video_stream = video.streams.get_highest_resolution()
            # title = video.title
            video.register_on_progress_callback(self.on_progress)
            # 获取当前工作目录并在其中保存视频
            downloadPath = os.path.abspath(params['path'])
            video_stream.download(downloadPath)
            # print(f"Fetching \"{video_stream.title}\"..")
            # print(f"Fetching successful\n")
            # print(f"Information: \n"
            #     f"File size: {round(video_stream.filesize * 0.000001, 2)} MegaBytes\n"
            #     f"Highest Resolution: {video_stream.resolution}\n"
            #     f"Author: {youtube.author}")
            # print("Views: {:,}\n".format(youtube.views))

            # print(f"Downloading \"{video_stream.title}\"..")
            # print(f"视频 [{title}] 已成功下载到 {params['path']} 目录下！")
            self.downSuccess.emit(1)  # 发送下载完成信号
        except pytubeException.AgeRestrictedError as e:
            self.downSuccess.emit(3)  # 发送因年龄限制导致下载失败信号
        except Exception as e:
            print(e.__class__)
            self.downSuccess.emit(2)  # 发送下载失败信号
class Downloader(QWidget):
    downloadInfoSignal = Signal(dict) #下载需要的url和path信号
    newProgressSignal = Signal(int)
    downloadResSignal = Signal(int)
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
        self.downThread.newPercentage.connect(self.receiveNewPercentageSignal)
        print('下载线程装载完成')
    #装载进度条更新线程
    def setupUpdateProgressThread(self):
        self.progressThreadInstance = QThread(self)  # 创建一个线程
        self.progressThread = ProgressUpdateThread()  # 实例化线程类
        self.progressThread.moveToThread(self.progressThreadInstance)  # 将类移动到线程中运行
        self.progressThread.progress.connect(self.updateProgressBarAct)
        self.progressThread.finished.connect(self.stopProgressThread)
        self.newProgressSignal.connect(self.progressThread.updateProgressWork)
        self.downloadResSignal.connect(self.progressThread.showRes)
        print('进度条线程装载完成')
    def receiveNewPercentageSignal(self,num):
        print('从下载线程接受到的新进度：'+str(num))
        self.newProgressSignal.emit(num)
    #开始进度条更新线程
    def startProgressThread(self):
        print('启动进度条更新线程')
        print('开始方法进度条线程状态:'+str(self.progressThreadInstance.isRunning()))
        self.progressThreadInstance.start()
        print('开始方法进度条线程状态:'+str(self.progressThreadInstance.isRunning()))
    #更新进度条信号对接方法
    def updateProgressBarAct(self, value):
        self.downloadProgress.setValue(value)
    #下载完成信号对接方法
    def downSuccessAct(self,res):
        print('下载完成对接方法的res是  '+str(res))
        self.stopDownloadThread(res)
            # QMessageBox.information(self,"下载结果","下载成功")
    #终止下载线程
    def stopDownloadThread(self,res):
        print('准备终止下载线程')
        print('终止方法下载线程状态:'+str(self.downThreadInstance.isRunning()))
        self.downThreadInstance.quit()
        self.downThreadInstance.wait()
        print('终止方法下载线程状态:'+str(self.downThreadInstance.isRunning()))
        self.downloadResSignal.emit(res)
    #开始下载线程
    def startDownThread(self):
        downloadParams = {'url':self.url.text(),'path':self.path.text()}
        print('启动下载线程')
        self.downloadProgress.setValue(0)
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
        elif res == 2:
            QMessageBox.information(self,"下载结果","下载失败")
        elif res == 3 :
            QMessageBox.information(self,"下载结果","因年龄限制原因，下载失败")
        self.stratDownload.setEnabled(True)
        self.url.setEnabled(True)
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
        self.url.setEnabled(False)
        self.browserBtn.setEnabled(False)
        print('开始下载action')
        self.startDownThread()
        self.startProgressThread()
    def browserPath(self):
        downloadPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.path.setText(str(downloadPath))
