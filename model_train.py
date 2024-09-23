# from camera_worker import CameraWorker
from src.model_worker import Model, FlawDetectorTrain, FlawDetectorPredict

def task0():
    model_0 = Model()
    detector_0 = FlawDetectorTrain(model_0, 0)
    detector_0.train_model()

def task1():
    model_1 = Model()
    detector_1 = FlawDetectorTrain(model_1, 1)
    detector_1.train_model()

def task2():
    model_2 = Model()
    detector_2 = FlawDetectorTrain(model_2, 2)
    detector_2.train_model()

def task3():
    model_3 = Model()
    detector_3 = FlawDetectorTrain(model_3, 3)
    detector_3.train_model()


from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *

class Worker(QObject):
    progress = pyqtSignal(int)
    completed = pyqtSignal()

    @pyqtSlot()
    def do_work(self):
        print("do_work")
        task0()
        self.progress.emit(1)
        task1()
        self.progress.emit(2)
        task2()
        self.progress.emit(3)
        task3()
        self.progress.emit(4)
        

        import os
        import cv2 as cv
        import numpy as np
        
        for i in range(0, 4):
            print("range ", i)
            model__0 = Model()
            detector__0 = FlawDetectorPredict(model__0, i)
        
            directory_name = f"./detector/{i}/train/good/"
            array_data = list()
            images = os.listdir(directory_name)
            print(images)
            for j, image_name in enumerate(images):
                if (image_name.split('.')[-1] == 'png' or image_name.split('.')[-1] == 'jpg'):
                    image = cv.imread(directory_name + image_name)
                    result = detector__0.predict_model_frame(image, 0.015)
                    print(image_name, result)
                    array_data.append(result)
            
            array_data = np.asarray(array_data)

            np.save(f"./detector/{i}/coords.npy", array_data)
            self.progress.emit(5 + i)

        print("model_train ", "end")
        self.completed.emit()