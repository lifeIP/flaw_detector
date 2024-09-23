from __future__ import print_function
import sys

import model_train
from src import *
from src.model_worker import *
from src.page import *
from src.worker import *

import math
import numpy as np

import cv2 as cv
import os
# os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

import tensorflow as tf
from tensorflow import keras
from keras import layers

from PIL import Image

import torch

# from model_worker import Model, FlawDetectorPredict


from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *

from sys import argv, executable

class App(QWidget):

    def __init__(self):
        super().__init__()
        print("main ", "init ", "start")
        self.title = 'Дефектоскоп'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        from model_train import Worker
        self.worker = Worker()
        self.worker_thread = QThread(self)
        self.ds_done = list()

        with open("./detector/settings.st", "r") as file:
            lines = file.readlines()
            self.cam_id_0 = lines[20].rstrip()
            self.cam_id_1 = lines[21].rstrip()
            self.cam_id_2 = lines[22].rstrip()
            self.cam_id_3 = lines[23].rstrip() 

        self.initUI()
        print("main ", "init ", "end")
    
    delete_thread_0 = pyqtSignal()
    delete_thread_1 = pyqtSignal()
    delete_thread_2 = pyqtSignal()
    delete_thread_3 = pyqtSignal()

    reload_settings = pyqtSignal()

    @pyqtSlot()
    def restart_app(self):
        self.reload_settings.emit()

        with open("./detector/settings.st", "r") as file:
            lines = file.readlines()
            cam_id_0 = lines[20].rstrip()
            cam_id_1 = lines[21].rstrip()
            cam_id_2 = lines[22].rstrip()
            cam_id_3 = lines[23].rstrip() 
            if self.cam_id_0 != cam_id_0 or self.cam_id_1 != cam_id_1 or \
                self.cam_id_2 != cam_id_2 or self.cam_id_3 != cam_id_3:
                
                self.restart()


    start_train = pyqtSignal(int)
    work_requested = pyqtSignal()
    start_terminal = pyqtSignal()


    @pyqtSlot(int, int)
    def train_app(self, id, detector_id):
        
        if id == 0:
            for j in range(0, 4):
                for i, image_name in enumerate(os.listdir(f"./detector/{j}/train/good/")):
                    if (image_name.split('.')[-1] == 'png' or image_name.split('.')[-1] == 'jpg'):
                        os.remove(f"./detector/{j}/train/good/" + image_name)
 
            self.start_train.emit(0)

        elif id == 1:
            if detector_id != -1:
                self.ds_done.append(detector_id)

            if len(self.ds_done) < 4:
                return
            
            self.main_layout.setCurrentIndex(1)
            self.start_terminal.emit()

            self.delete_thread_0.emit()
            self.delete_thread_1.emit()
            self.delete_thread_2.emit()
            self.delete_thread_3.emit()
                        
            print("main ", "signal ", "train_app")
            self.work_requested.emit()

    def initUI(self):

        print("main ", "initUI ", "start")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        

        from src.page.Page import MyPage
        self.page_0 = MyPage(0,int(self.cam_id_0))
        self.page_1 = MyPage(1,int(self.cam_id_1))
        self.page_2 = MyPage(2,int(self.cam_id_2))
        self.page_3 = MyPage(3,int(self.cam_id_3))
        from src.page.PageSettings import PageSettings
        self.settings = PageSettings()

        tabs = QTabWidget()
        tab0 = self.page_0
        tab1 = self.page_1
        tab2 = self.page_2
        tab3 = self.page_3
        settings = self.settings

        tabs.addTab(tab0,"1")
        tabs.addTab(tab1,"2")
        tabs.addTab(tab2,"3")
        tabs.addTab(tab3,"4")
        tabs.addTab(settings,"Настройки")
        

        from src.page.PageTerminal import TerminalPage
        self.terminal_page = TerminalPage()


        self.main_layout = QStackedLayout()
        self.main_layout.addWidget(tabs)
        self.main_layout.addWidget(self.terminal_page)
        self.main_layout.setCurrentIndex(0)
        
        self.setLayout(self.main_layout)
        
        
        self.delete_thread_0.connect(self.page_0.delete_thread)
        self.delete_thread_1.connect(self.page_1.delete_thread)
        self.delete_thread_2.connect(self.page_2.delete_thread)
        self.delete_thread_3.connect(self.page_3.delete_thread)

        self.settings.start_train.connect(self.train_app)
        self.page_0.end_train.connect(self.train_app)
        self.page_1.end_train.connect(self.train_app)
        self.page_2.end_train.connect(self.train_app)
        self.page_3.end_train.connect(self.train_app)
        
        self.start_train.connect(self.page_0.train_app)
        self.start_train.connect(self.page_1.train_app)
        self.start_train.connect(self.page_2.train_app)
        self.start_train.connect(self.page_3.train_app)
        
        self.start_terminal.connect(self.terminal_page.terminal_update)

        self.settings.restart_signal.connect(self.restart_app)
        self.reload_settings.connect(self.page_0.reload_data)
        self.reload_settings.connect(self.page_1.reload_data)
        self.reload_settings.connect(self.page_2.reload_data)
        self.reload_settings.connect(self.page_3.reload_data)

        self.work_requested.connect(self.worker.do_work)
        self.worker.completed.connect(self.restart)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        
        print("main ", "initUI ", "end")
        self.show()

    @pyqtSlot()
    def restart(self):
        print("main ", "slot ", "restart")
        # self.worker_thread.terminate()
        self.worker_thread.quit()
        self.delete_thread_0.emit()
        self.delete_thread_1.emit()
        self.delete_thread_2.emit()
        self.delete_thread_3.emit()
        

        self.close()
        self.__init__()
        print("main ", "slot ", "restart end")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())