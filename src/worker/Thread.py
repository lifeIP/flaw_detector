import cv2 as cv
import numpy as np
from PIL import Image
import time

from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *

from src.model_worker import Model, FlawDetectorPredict


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    changeFlawPixmap = pyqtSignal(QImage)
    changeErrorValue = pyqtSignal(float)
    changeCountError = pyqtSignal()

    @pyqtSlot(int)
    def setDetectorId(self, id: int):
        self.tab_id = id

    @pyqtSlot(int)
    def setCamId(self, id: int):
        self.tab_id = id
    
    @pyqtSlot(int)
    def setFokus(self, fokus: int):
        self.cap.set(28, fokus)

    @pyqtSlot()
    def delete_thread(self):
        self.cap.release()
        self.exit()

    @pyqtSlot()
    def train_app(self):
        self.is_train = True
        self.counter = 0

    @pyqtSlot()
    def reload_data(self):
        with open("./detector/settings.st", "r") as file:
            lines = file.readlines()
            
            self.angle = float(lines[0 + self.detector_id].rstrip())
            self.left  = int(lines[4 + self.detector_id].rstrip())
            self.right = int(lines[8 + self.detector_id].rstrip())
            self.fokus = int(lines[12 + self.detector_id].rstrip())
            self.cap.set(28, self.fokus)
            self.threshold_value = float(str(lines[16 + self.detector_id].rstrip()).replace( ',', '.'))
            self.max_counter = int(lines[24].rstrip())

    dataset_done = pyqtSignal(int)
    

    
    def __init__(self, detector_id: int, cam_id: int):
        super().__init__()

        self.detector_id = detector_id
        self.cam_id = cam_id

        self.is_train = False
        self.counter = 0

        with open("./detector/settings.st", "r") as file:
            lines = file.readlines()

            self.angle = float(lines[0 + detector_id].rstrip())
            self.left  = int(lines[4 + detector_id].rstrip())
            self.right = int(lines[8 + detector_id].rstrip())
            self.fokus = int(lines[12 + detector_id].rstrip())
            self.threshold_value = float(str(lines[16 + detector_id].rstrip()).replace( ',', '.'))
            self.max_counter = int(lines[24].rstrip())
            


        # print(self.detector_id, self.cam_id)

    def run(self):

        # import time
        model = Model()
        flaw_detector = FlawDetectorPredict(model, self.detector_id)
        
        # self.cap = cv.VideoCapture(self.cam_id)
        # self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 640)
        # self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 480)
        # self.cap.set(28, self.fokus)
        self.cap = cv.VideoCapture("./video/3.avi")

        while True:
            # self.start_time = time.time()
            ret, src = self.cap.read(cv.IMREAD_GRAYSCALE)
            if not ret: continue

            src_copy = src.copy()
            h, w = src.shape[:2]

            cv.line(src_copy, (self.left, 0), (self.left, h), (0,255,0), 4)
            cv.line(src_copy, (w - self.right, 0), (w - self.right, h), (0,255,0), 4)     
            

            src = src[180: h - 200, self.left: w-self.right]
            src = cv.blur(src, (1,5))
            h, w = src.shape[:2]

            sharp_filter = np.array([[4, -10, 1], [-5, 14, -5], [-1, 4, -1]])
            sharpen_img = cv.filter2D(src, ddepth=-1, kernel=sharp_filter)
            
                
            if self.is_train:
                import time
                cv.imwrite(f"./detector/{self.detector_id}/train/good/{time.time()}.png", sharpen_img)
                self.counter += 1
                print(self.counter, "/", self.max_counter)
                if self.counter >= self.max_counter: 
                    self.is_train = False
                    time.sleep(3)
                    self.dataset_done.emit(self.detector_id)
            else:
                result = flaw_detector.predict_model_frame(sharpen_img, self.threshold_value)
                self.changeErrorValue.emit(result)

                if self.threshold_value < result:
                    import time
                    cv.imwrite(f"./detector/{self.detector_id}/errors/{time.time()}_{result}.png", sharpen_img)
                    self.changeCountError.emit()

                    from pathlib import Path
                    folder_name = f"./detector/{self.detector_id}/errors/"
                    folder = Path(folder_name)
                    if len(list(folder.iterdir())) > 1000:
                        import zipfile
                        import time
                        import os

                        archive = f"./detector/zips/errors_{time.time()}.zip"

                        with zipfile.ZipFile(archive, "w") as zf:
                            for j in range(0, 4):
                                for i, image_name in enumerate(os.listdir(f"./detector/{j}/errors")):
                                    if (image_name.split('.')[-1] == 'png' or image_name.split('.')[-1] == 'jpg'):
                                        zf.write(f"./detector/{j}/errors/" + image_name)
                                        os.remove(f"./detector/{j}/errors/" + image_name)

            
            
            rgbImage_0 = cv.cvtColor(src_copy, cv.COLOR_BGR2RGB)
            h0, w0, ch0 = rgbImage_0.shape
            bytesPerLine_0 = ch0 * w0
            convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format.Format_RGB888)
            p_0 = convertToQtFormat_0.scaled(300, 250, Qt.AspectRatioMode.KeepAspectRatio)
            self.changePixmap.emit(p_0)


            rgbImage_1 = cv.cvtColor(sharpen_img, cv.COLOR_BGR2RGB)
            h1, w1, ch1 = rgbImage_1.shape
            bytesPerLine_1 = ch1 * w1
            convertToQtFormat_1 = QImage(rgbImage_1.data, w1, h1, bytesPerLine_1, QImage.Format.Format_RGB888)
            p_1 = convertToQtFormat_1.scaled(300, 250, Qt.AspectRatioMode.KeepAspectRatio)
            self.changeFlawPixmap.emit(p_1)

            # print("FPS: ", 1.0 / (time.time() - self.start_time))