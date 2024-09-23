from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *

from src.worker.Thread import Thread

import numpy as np
import pyqtgraph as pg

class MyPage(QWidget):

    @pyqtSlot(QImage)
    def setPixmap(self, image: QImage):
        self.pixmap_0.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setFlawPixmap(self, image: QImage):
        self.pixmap_1.setPixmap(QPixmap.fromImage(image))
    

    @pyqtSlot(float)
    def setErrorValue(self, value: float):
        self.errorValue.setText(f"Значение полученное от нейросети: {value}")

        
        if self.last_index >= 1000:
            self.last_index = 0
            self.x_coord.clear()
            self.y_coord.clear()

        self.x_coord.append(self.last_index)
        self.y_coord.append(float(value))
        self.last_index += 1
        self.plotWidget.setData(np.asarray(self.x_coord), np.asarray(self.y_coord))
        


    start_train = pyqtSignal(int)
    end_train = pyqtSignal(int, int)

    reload_settings = pyqtSignal()
    @pyqtSlot()
    def reload_data(self):
        self.reload_settings.emit()

    @pyqtSlot()
    def train_app(self):
        import os
        from pathlib import Path
        folder_name = f"./detector/{self.detector_id}/train/good/"
        images = os.listdir(folder_name)
        for j, image_name in enumerate(images):
            if (image_name.split('.')[-1] == 'png' or image_name.split('.')[-1] == 'jpg'):
                os.remove(folder_name + image_name)

        self.start_train.emit(0)
    
    @pyqtSlot(int)
    def dataset_done(self, id):
        self.end_train.emit(1, id)
    

    @pyqtSlot()
    def delete_thread(self):
        print("Page ", "slot")
        self.th.delete_thread()


    @pyqtSlot()
    def addCountError(self):
        self.countError += 1
        self.errorCount.setText(f"Количество выбросов: {self.countError}")

    def __init__(self, detector_id: int, cam_id: int):
        self.detector_id = detector_id
        self.cam_id = cam_id
        self.countError = 0
        
        self.last_index = 0
        self.y_coord = list()
        self.x_coord = list()
        
        super().__init__()
        self.initUI()


    def initUI(self):
    
        self.th = Thread(self.detector_id, self.cam_id)
        
        self.pixmap_0 = QLabel()
        self.pixmap_0.setScaledContents(True)

        self.pixmap_1 = QLabel()
        self.pixmap_1.setScaledContents(True)



        self.plot = pg.plot()
        self.plotWidget = self.plot.plot(pen=(3,4))
        self.plot.setRange(xRange=[0, 150], yRange=[0.00001, 0.2])
        

        self.downLayout = QHBoxLayout()
        self.downLayout.addWidget(self.pixmap_0, 1)
        self.downLayout.addWidget(self.pixmap_1, 1)


        
        self.errorValue = QLabel()
        self.errorValue.setScaledContents(True)

        self.errorCount = QLabel()
        self.errorCount.setScaledContents(True)
        
        self.h_box_layout_0 = QHBoxLayout()
        self.h_box_layout_0.addWidget(self.errorValue, 1)
        self.h_box_layout_0.addWidget(self.errorCount, 1)
        
        self.v_box_layout_0 = QVBoxLayout()
        self.v_box_layout_0.addWidget(self.plot, 4)
        self.v_box_layout_0.addLayout(self.downLayout, 4)
        self.v_box_layout_0.addLayout(self.h_box_layout_0, 1)

        self.setLayout(self.v_box_layout_0)
        
        self.th.changePixmap.connect(self.setPixmap)
        self.th.changeFlawPixmap.connect(self.setFlawPixmap)
        self.th.changeErrorValue.connect(self.setErrorValue)
        self.th.dataset_done.connect(self.dataset_done)
        self.start_train.connect(self.th.train_app)
        self.th.changeCountError.connect(self.addCountError)
        self.reload_settings.connect(self.th.reload_data)

        self.th.start()
        