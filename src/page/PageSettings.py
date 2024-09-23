from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *
from PyQt6.QtCore import Qt


import pyqtgraph as pg
import numpy as np

class PageSettings(QWidget):

    restart_signal = pyqtSignal()   
    start_train = pyqtSignal(int,int)
    
    @pyqtSlot()
    def zipPressed(self):
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


    @pyqtSlot()
    def learnPressed(self):
        self.flag = True

        self.lineEdit_left_0.setDisabled(self.flag)
        self.lineEdit_left_1.setDisabled(self.flag)
        self.lineEdit_left_2.setDisabled(self.flag)
        self.lineEdit_left_3.setDisabled(self.flag)

        self.lineEdit_right_0.setDisabled(self.flag)
        self.lineEdit_right_1.setDisabled(self.flag)
        self.lineEdit_right_2.setDisabled(self.flag)
        self.lineEdit_right_3.setDisabled(self.flag)

        self.lineEdit_fokus_0.setDisabled(self.flag)
        self.lineEdit_fokus_1.setDisabled(self.flag)
        self.lineEdit_fokus_2.setDisabled(self.flag)
        self.lineEdit_fokus_3.setDisabled(self.flag)
        
        self.lineEdit_cam_id_0.setDisabled(self.flag)
        self.lineEdit_cam_id_1.setDisabled(self.flag)
        self.lineEdit_cam_id_2.setDisabled(self.flag)
        self.lineEdit_cam_id_3.setDisabled(self.flag)


        self.lineEdit_threshold_value_0.setDisabled(self.flag)
        self.lineEdit_threshold_value_1.setDisabled(self.flag)
        self.lineEdit_threshold_value_2.setDisabled(self.flag)
        self.lineEdit_threshold_value_3.setDisabled(self.flag)

        self.button_zip.setDisabled(self.flag)

        self.learn_button.setDisabled(self.flag)

        self.saveButton.setDisabled(self.flag)

        self.train_button.setDisabled(self.flag)
        self.lineEdit_password.setDisabled(self.flag)

        self.lineEdit_count_of_dataset.setDisabled(self.flag)

        self.start_train.emit(0, -1)

    @pyqtSlot()
    def savePressed(self):
        with open("./detector/settings.st", "w") as file:

            lines = [self.angle_0,
                     self.angle_1, 
                     self.angle_2,
                     self.angle_3,

                     self.left_0,
                     self.left_1,
                     self.left_2,
                     self.left_3,

                     self.right_0,
                     self.right_1,
                     self.right_2,
                     self.right_3,
                    
                     self.fokus_0,
                     self.fokus_1,
                     self.fokus_2,
                     self.fokus_3,

                     self.threshold_value_0,
                     self.threshold_value_1,
                     self.threshold_value_2,
                     self.threshold_value_3,
                     
                     self.cam_id_0,
                     self.cam_id_1,
                     self.cam_id_2,
                     self.cam_id_3,
                     
                     self.dataset_count,
                     self.count_of_epochs
                     ]
            
            for line in lines: 
                file.write(line.rstrip() + '\n')

        print(self.threshold_value_3)

        self.restart_signal.emit()


        self.lineEdit_left_0.setPlaceholderText(f"{self.left_0}")
        self.lineEdit_left_1.setPlaceholderText(f"{self.left_1}")
        self.lineEdit_left_2.setPlaceholderText(f"{self.left_2}")
        self.lineEdit_left_3.setPlaceholderText(f"{self.left_3}")
        
        self.lineEdit_right_0.setPlaceholderText(f"{self.right_0}")
        self.lineEdit_right_1.setPlaceholderText(f"{self.right_1}")
        self.lineEdit_right_2.setPlaceholderText(f"{self.right_2}")
        self.lineEdit_right_3.setPlaceholderText(f"{self.right_3}")

        self.lineEdit_fokus_0.setPlaceholderText(f"{self.fokus_0}")
        self.lineEdit_fokus_1.setPlaceholderText(f"{self.fokus_1}")
        self.lineEdit_fokus_2.setPlaceholderText(f"{self.fokus_2}")
        self.lineEdit_fokus_3.setPlaceholderText(f"{self.fokus_3}")
        
        self.lineEdit_cam_id_0.setPlaceholderText(f"{self.cam_id_0}")
        self.lineEdit_cam_id_1.setPlaceholderText(f"{self.cam_id_1}")
        self.lineEdit_cam_id_2.setPlaceholderText(f"{self.cam_id_2}")
        self.lineEdit_cam_id_3.setPlaceholderText(f"{self.cam_id_3}")

        self.lineEdit_threshold_value_0.setPlaceholderText(f"{self.threshold_value_0}")
        self.lineEdit_threshold_value_1.setPlaceholderText(f"{self.threshold_value_1}")
        self.lineEdit_threshold_value_2.setPlaceholderText(f"{self.threshold_value_2}")
        self.lineEdit_threshold_value_3.setPlaceholderText(f"{self.threshold_value_3}")

    def __init__(self):
        super().__init__()

        with open("./detector/settings.st", "r") as file:
            lines = file.readlines()

            self.angle_0 = lines[0].rstrip()
            self.angle_1 = lines[1].rstrip()
            self.angle_2 = lines[2].rstrip()
            self.angle_3 = lines[3].rstrip()

            self.left_0 = lines[4].rstrip()
            self.left_1 = lines[5].rstrip()
            self.left_2 = lines[6].rstrip()
            self.left_3 = lines[7].rstrip()

            self.right_0 = lines[8].rstrip()
            self.right_1 = lines[9].rstrip()
            self.right_2 = lines[10].rstrip()
            self.right_3 = lines[11].rstrip()
            
            self.fokus_0 = lines[12].rstrip()
            self.fokus_1 = lines[13].rstrip()
            self.fokus_2 = lines[14].rstrip()
            self.fokus_3 = lines[15].rstrip()

            self.threshold_value_0 = lines[16].rstrip()
            self.threshold_value_1 = lines[17].rstrip()
            self.threshold_value_2 = lines[18].rstrip()
            self.threshold_value_3 = lines[19].rstrip()

            self.cam_id_0 = lines[20].rstrip()
            self.cam_id_1 = lines[21].rstrip()
            self.cam_id_2 = lines[22].rstrip()
            self.cam_id_3 = lines[23].rstrip()          

            self.dataset_count = lines[24].rstrip()
            self.count_of_epochs = lines[25].rstrip()  

        self.initUI()
        self.login("")

    def login(self, password):
        
        if password == "admin123":
            self.flag = False
            self.label_2.setText("<b style='color: green;'>***Пароль введен***</b>")
        else:
            self.flag = True
            self.label_2.setText("<b style='color: red;'>***Для принятия всех изменений и/или начала обучения введите пароль***</b>")


        self.lineEdit_left_0.setDisabled(self.flag)
        self.lineEdit_left_1.setDisabled(self.flag)
        self.lineEdit_left_2.setDisabled(self.flag)
        self.lineEdit_left_3.setDisabled(self.flag)

        self.lineEdit_right_0.setDisabled(self.flag)
        self.lineEdit_right_1.setDisabled(self.flag)
        self.lineEdit_right_2.setDisabled(self.flag)
        self.lineEdit_right_3.setDisabled(self.flag)

        self.lineEdit_fokus_0.setDisabled(self.flag)
        self.lineEdit_fokus_1.setDisabled(self.flag)
        self.lineEdit_fokus_2.setDisabled(self.flag)
        self.lineEdit_fokus_3.setDisabled(self.flag)

        self.lineEdit_cam_id_0.setDisabled(self.flag)
        self.lineEdit_cam_id_1.setDisabled(self.flag)
        self.lineEdit_cam_id_2.setDisabled(self.flag)
        self.lineEdit_cam_id_3.setDisabled(self.flag)

        self.lineEdit_threshold_value_0.setDisabled(self.flag)
        self.lineEdit_threshold_value_1.setDisabled(self.flag)
        self.lineEdit_threshold_value_2.setDisabled(self.flag)
        self.lineEdit_threshold_value_3.setDisabled(self.flag)

        self.button_zip.setDisabled(self.flag)

        self.learn_button.setDisabled(self.flag)

        self.saveButton.setDisabled(self.flag)

        self.lineEdit_count_of_dataset.setDisabled(self.flag)



    def anglechanged_0(self, angle):
        pass
        # if len(angle) > 0: self.angle_0 = str(angle)
        # else: self.angle_0 = self.lineEdit_angle_0.placeholderText()

    def anglechanged_1(self, angle):
        pass
        # if len(angle) > 0: self.angle_1 = str(angle)
        # else: self.angle_1 = self.lineEdit_angle_1.placeholderText()

    def anglechanged_2(self, angle):
        pass
        # if len(angle) > 0: self.angle_2 = str(angle)
        # else: self.angle_2 = self.lineEdit_angle_2.placeholderText()
    
    def anglechanged_3(self, angle):
        pass
        # if len(angle) > 0: self.angle_3 = str(angle)
        # else: self.angle_3 = self.lineEdit_angle_3.placeholderText()


    
    def leftchanged_0(self, left):
        if len(left) > 0: self.left_0 = str(left)
        else: self.left_0 = self.lineEdit_left_0.placeholderText()
    def leftchanged_1(self, left):
        if len(left) > 0: self.left_1 = str(left)
        else: self.left_1 = self.lineEdit_left_1.placeholderText()
    def leftchanged_2(self, left):
        if len(left) > 0: self.left_2 = str(left)
        else: self.left_2 = self.lineEdit_left_2.placeholderText()
    def leftchanged_3(self, left):
        if len(left) > 0: self.left_3 = str(left)
        else: self.left_3 = self.lineEdit_left_3.placeholderText()


    def rightchanged_0(self, right):
        if len(right) > 0: self.right_0 = str(right)
        else: self.right_0 = self.lineEdit_right_0.placeholderText()
    def rightchanged_1(self, right):
        if len(right) > 0: self.right_1 = str(right)
        else: self.right_1 = self.lineEdit_right_1.placeholderText()
    def rightchanged_2(self, right):
        if len(right) > 0: self.right_2 = str(right)
        else: self.right_2 = self.lineEdit_right_2.placeholderText()
    def rightchanged_3(self, right):
        if len(right) > 0: self.right_3 = str(right)
        else: self.right_3 = self.lineEdit_right_3.placeholderText()



    def fokuschanged_0(self, fokus):
        if len(fokus) > 0: self.fokus_0 = str(fokus)
        else: self.fokus_0 = self.lineEdit_fokus_0.placeholderText()
    def fokuschanged_1(self, fokus):
        if len(fokus) > 0: self.fokus_1 = str(fokus)
        else: self.fokus_1 = self.lineEdit_fokus_1.placeholderText()
    def fokuschanged_2(self, fokus):
        if len(fokus) > 0: self.fokus_2 = str(fokus)
        else: self.fokus_2 = self.lineEdit_fokus_2.placeholderText()
    def fokuschanged_3(self, fokus):
        if len(fokus) > 0: self.fokus_3 = str(fokus)
        else: self.fokus_3 = self.lineEdit_fokus_3.placeholderText()
        
    def cam_id_changed_0(self, cam_id):
        self.cam_id_0 = str(cam_id)
    def cam_id_changed_1(self, cam_id):
        self.cam_id_1 = str(cam_id)
    def cam_id_changed_2(self, cam_id):
        self.cam_id_2 = str(cam_id)
    def cam_id_changed_3(self, cam_id):
        self.cam_id_3 = str(cam_id)
        

    def threshold_value_changed_0(self, value):
        if len(value) > 0: self.threshold_value_0 = str(value)
        else: self.threshold_value_0 = self.lineEdit_threshold_value_0.placeholderText()
    def threshold_value_changed_1(self, value):
        if len(value) > 0: self.threshold_value_1 = str(value)
        else: self.threshold_value_1 = self.lineEdit_threshold_value_1.placeholderText()
    def threshold_value_changed_2(self, value):
        if len(value) > 0: self.threshold_value_2 = str(value)
        else: self.threshold_value_2 = self.lineEdit_threshold_value_2.placeholderText()
    def threshold_value_changed_3(self, value):
        if len(value) > 0: self.threshold_value_3 = str(value)
        else: self.threshold_value_3 = self.lineEdit_threshold_value_3.placeholderText()


    def dataset_count_changed(self, value):
        if len(value) > 0: self.dataset_count = str(value)
        else: self.dataset_count = self.lineEdit_count_of_dataset.placeholderText()

    def initUI(self):
    
        self.learn_button = QPushButton()
        self.learn_button.setText("Обучить")
        self.learn_button.pressed.connect(self.learnPressed)

        self.label_0 = QLabel()
        self.label_0.setText("Обучение нейросети  ")
        # self.label_0.setAlignment(Qt.AlignRight)

        self.lineEdit_count_of_dataset = QLineEdit()
        self.lineEdit_count_of_dataset.textChanged.connect(self.dataset_count_changed)
        self.lineEdit_count_of_dataset.setValidator(QIntValidator())
        self.lineEdit_count_of_dataset.setMaxLength(3)
        self.lineEdit_count_of_dataset.setPlaceholderText(f"{self.dataset_count}")


        self.h_box_layout = QHBoxLayout()
        self.h_box_layout.addWidget(self.label_0, 3)
        self.h_box_layout.addWidget(self.lineEdit_count_of_dataset, 3)
        self.h_box_layout.addWidget(self.learn_button, 3)

        self.train_button = QWidget()
        self.train_button.setLayout(self.h_box_layout)
        self.train_button.setMaximumWidth(950)

        self.h_box_layout_1 = QHBoxLayout()
        self.h_box_layout_1.addWidget(self.train_button)

        self.label_1 = QLabel()
        self.label_1.setText("<b style='color: red;'>***Перед обучением надо ОБЯЗАТЕЛЬНО прочесть инструкцию***</b>")
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.label_2 = QLabel()
        self.label_2.setText("<b style='color: red;'>***Для принятия всех изменений и/или начала обучения введите пароль***</b>")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.textChanged.connect(self.login)
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)


        # 0 детектор левая линия
        self.lineEdit_left_0 = QLineEdit()
        self.lineEdit_left_0.textChanged.connect(self.leftchanged_0)
        self.lineEdit_left_0.setValidator(QIntValidator())
        self.lineEdit_left_0.setMaxLength(3)
        self.lineEdit_left_0.setPlaceholderText(f"{self.left_0}")

        # 1 детектор левая линия
        self.lineEdit_left_1 = QLineEdit()
        self.lineEdit_left_1.textChanged.connect(self.leftchanged_1)
        self.lineEdit_left_1.setValidator(QIntValidator())
        self.lineEdit_left_1.setMaxLength(3)
        self.lineEdit_left_1.setPlaceholderText(f"{self.left_1}")
        
        # 2 детектор левая линия
        self.lineEdit_left_2 = QLineEdit()
        self.lineEdit_left_2.textChanged.connect(self.leftchanged_2)
        self.lineEdit_left_2.setValidator(QIntValidator())
        self.lineEdit_left_2.setMaxLength(3)
        self.lineEdit_left_2.setPlaceholderText(f"{self.left_2}")
        
        # 3 детектор левая линия
        self.lineEdit_left_3 = QLineEdit()
        self.lineEdit_left_3.textChanged.connect(self.leftchanged_3)
        self.lineEdit_left_3.setValidator(QIntValidator())
        self.lineEdit_left_3.setMaxLength(3)
        self.lineEdit_left_3.setPlaceholderText(f"{self.left_3}")



        # 0 детектор правая линия
        self.lineEdit_right_0 = QLineEdit()
        self.lineEdit_right_0.textChanged.connect(self.rightchanged_0)
        self.lineEdit_right_0.setValidator(QIntValidator())
        self.lineEdit_right_0.setMaxLength(3)
        self.lineEdit_right_0.setPlaceholderText(f"{self.right_0}")

        # 1 детектор правая линия
        self.lineEdit_right_1 = QLineEdit()
        self.lineEdit_right_1.textChanged.connect(self.rightchanged_1)
        self.lineEdit_right_1.setValidator(QIntValidator())
        self.lineEdit_right_1.setMaxLength(3)
        self.lineEdit_right_1.setPlaceholderText(f"{self.right_1}")
        
        # 2 детектор правая линия
        self.lineEdit_right_2 = QLineEdit()
        self.lineEdit_right_2.textChanged.connect(self.rightchanged_2)
        self.lineEdit_right_2.setValidator(QIntValidator())
        self.lineEdit_right_2.setMaxLength(3)
        self.lineEdit_right_2.setPlaceholderText(f"{self.right_2}")
        
        # 3 детектор правая линия
        self.lineEdit_right_3 = QLineEdit()
        self.lineEdit_right_3.textChanged.connect(self.rightchanged_3)
        self.lineEdit_right_3.setValidator(QIntValidator())
        self.lineEdit_right_3.setMaxLength(3)
        self.lineEdit_right_3.setPlaceholderText(f"{self.right_3}")




        # 0 детектор фокус
        self.lineEdit_fokus_0 = QLineEdit()
        self.lineEdit_fokus_0.textChanged.connect(self.fokuschanged_0)
        self.lineEdit_fokus_0.setValidator(QIntValidator())
        self.lineEdit_fokus_0.setMaxLength(3)
        self.lineEdit_fokus_0.setPlaceholderText(f"{self.fokus_0}")

        # 1 детектор фокус
        self.lineEdit_fokus_1 = QLineEdit()
        self.lineEdit_fokus_1.textChanged.connect(self.fokuschanged_1)
        self.lineEdit_fokus_1.setValidator(QIntValidator())
        self.lineEdit_fokus_1.setMaxLength(3)
        self.lineEdit_fokus_1.setPlaceholderText(f"{self.fokus_1}")
        
        # 2 детектор фокус
        self.lineEdit_fokus_2 = QLineEdit()
        self.lineEdit_fokus_2.textChanged.connect(self.fokuschanged_2)
        self.lineEdit_fokus_2.setValidator(QIntValidator())
        self.lineEdit_fokus_2.setMaxLength(3)
        self.lineEdit_fokus_2.setPlaceholderText(f"{self.fokus_2}")
        
        # 3 детектор фокус
        self.lineEdit_fokus_3 = QLineEdit()
        self.lineEdit_fokus_3.textChanged.connect(self.fokuschanged_3)
        self.lineEdit_fokus_3.setValidator(QIntValidator())
        self.lineEdit_fokus_3.setMaxLength(3)
        self.lineEdit_fokus_3.setPlaceholderText(f"{self.fokus_3}")




        # 0 детектор
        self.lineEdit_threshold_value_0 = QLineEdit()
        self.lineEdit_threshold_value_0.textChanged.connect(self.threshold_value_changed_0)
        self.lineEdit_threshold_value_0.setValidator(QDoubleValidator(-40.1, 40.1, 8))
        self.lineEdit_threshold_value_0.setPlaceholderText(f"{self.threshold_value_0}")

        # 1 детектор
        self.lineEdit_threshold_value_1 = QLineEdit()
        self.lineEdit_threshold_value_1.textChanged.connect(self.threshold_value_changed_1)
        self.lineEdit_threshold_value_1.setValidator(QDoubleValidator(-40.1, 40.1, 8))
        self.lineEdit_threshold_value_1.setPlaceholderText(f"{self.threshold_value_1}")
        
        # 2 детектор
        self.lineEdit_threshold_value_2 = QLineEdit()
        self.lineEdit_threshold_value_2.textChanged.connect(self.threshold_value_changed_2)
        self.lineEdit_threshold_value_2.setValidator(QDoubleValidator(-40.1, 40.1, 8))
        self.lineEdit_threshold_value_2.setPlaceholderText(f"{self.threshold_value_2}")
        
        # 3 детектор
        self.lineEdit_threshold_value_3 = QLineEdit()
        self.lineEdit_threshold_value_3.textChanged.connect(self.threshold_value_changed_3)
        self.lineEdit_threshold_value_3.setValidator(QDoubleValidator(-40.1, 40.1, 8))
        self.lineEdit_threshold_value_3.setPlaceholderText(f"{self.threshold_value_3}")
        




        # 0 детектор id cam
        self.lineEdit_cam_id_0 = QLineEdit()
        self.lineEdit_cam_id_0.textChanged.connect(self.cam_id_changed_0)
        self.lineEdit_cam_id_0.setValidator(QIntValidator())
        self.lineEdit_cam_id_0.setMaxLength(2)
        self.lineEdit_cam_id_0.setPlaceholderText(f"{self.cam_id_0}")

        # 1 детектор id cam
        self.lineEdit_cam_id_1 = QLineEdit()
        self.lineEdit_cam_id_1.textChanged.connect(self.cam_id_changed_1)
        self.lineEdit_cam_id_1.setValidator(QIntValidator())
        self.lineEdit_cam_id_1.setMaxLength(2)
        self.lineEdit_cam_id_1.setPlaceholderText(f"{self.cam_id_1}")
        
        # 2 детектор id cam
        self.lineEdit_cam_id_2 = QLineEdit()
        self.lineEdit_cam_id_2.textChanged.connect(self.cam_id_changed_2)
        self.lineEdit_cam_id_2.setValidator(QIntValidator())
        self.lineEdit_cam_id_2.setMaxLength(2)
        self.lineEdit_cam_id_2.setPlaceholderText(f"{self.cam_id_2}")
        
        # 3 детектор id cam
        self.lineEdit_cam_id_3 = QLineEdit()
        self.lineEdit_cam_id_3.textChanged.connect(self.cam_id_changed_3)
        self.lineEdit_cam_id_3.setValidator(QIntValidator())
        self.lineEdit_cam_id_3.setMaxLength(2)
        self.lineEdit_cam_id_3.setPlaceholderText(f"{self.cam_id_3}")


        self.formLayout_6 = QFormLayout()
        self.formLayout_6.addRow("Индекс камеры 1", self.lineEdit_cam_id_0)
        self.formLayout_6.addRow("Индекс камеры 2", self.lineEdit_cam_id_1)

        self.formLayout_7 = QFormLayout()
        self.formLayout_7.addRow("Индекс камеры 3", self.lineEdit_cam_id_2)
        self.formLayout_7.addRow("Индекс камеры 4", self.lineEdit_cam_id_3)



        # self.formLayout = QFormLayout()
        # self.formLayout.addRow("Угол для 1 детектора", self.lineEdit_angle_0)
        # self.formLayout.addRow("Угол для 2 детектора", self.lineEdit_angle_1)
        # self.formLayout.addRow("Угол для 3 детектора", self.lineEdit_angle_2)
        # self.formLayout.addRow("Угол для 4 детектора", self.lineEdit_angle_3)

        self.formLayout_1 = QFormLayout()
        self.formLayout_1.addRow("Детектор 1, левая линия", self.lineEdit_left_0)
        self.formLayout_1.addRow("Детектор 2, левая линия", self.lineEdit_left_1)
        self.formLayout_1.addRow("Детектор 3, левая линия", self.lineEdit_left_2)
        self.formLayout_1.addRow("Детектор 4, левая линия", self.lineEdit_left_3)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.addRow("Детектор 1, правая линия", self.lineEdit_right_0)
        self.formLayout_2.addRow("Детектор 2, правая линия", self.lineEdit_right_1)
        self.formLayout_2.addRow("Детектор 3, правая линия", self.lineEdit_right_2)
        self.formLayout_2.addRow("Детектор 4, правая линия", self.lineEdit_right_3)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.addRow("Детектор 1, фокус", self.lineEdit_fokus_0)
        self.formLayout_3.addRow("Детектор 2, фокус", self.lineEdit_fokus_1)
        self.formLayout_3.addRow("Детектор 3, фокус", self.lineEdit_fokus_2)
        self.formLayout_3.addRow("Детектор 4, фокус", self.lineEdit_fokus_3)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.addRow("Детектор 1, порог", self.lineEdit_threshold_value_0)
        self.formLayout_4.addRow("Детектор 2, порог", self.lineEdit_threshold_value_1)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.addRow("Детектор 3, порог", self.lineEdit_threshold_value_2)
        self.formLayout_5.addRow("Детектор 4, порог", self.lineEdit_threshold_value_3)


        self.h_box_layout_form = QHBoxLayout()
        self.h_box_layout_form.addLayout(self.formLayout_1, 1)
        self.h_box_layout_form.addLayout(self.formLayout_2, 1)


        self.h_box_layout_form_2 = QHBoxLayout()
        self.h_box_layout_form_2.addLayout(self.formLayout_3, 1)
        

        self.h_box_layout_form_3 = QHBoxLayout()
        self.h_box_layout_form_3.addLayout(self.formLayout_4, 1)
        self.h_box_layout_form_3.addLayout(self.formLayout_5, 1)

        self.h_box_layout_form_4 = QHBoxLayout()
        self.h_box_layout_form_4.addLayout(self.formLayout_6, 1)
        self.h_box_layout_form_4.addLayout(self.formLayout_7, 1)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.addRow("Пароль", self.lineEdit_password)
        self.saveButton = QPushButton("Сохранить изменения")
        self.saveButton.pressed.connect(self.savePressed)
        self.h_box_layout_password = QHBoxLayout()
        self.h_box_layout_password.addLayout(self.formLayout_2, 1)
        self.h_box_layout_password.addWidget(self.saveButton, 1)


        self.v_box_layout_form = QVBoxLayout()
        self.v_box_layout_form.addLayout(self.h_box_layout_form, 4)
        self.v_box_layout_form.addLayout(self.h_box_layout_form_2, 4)
        self.v_box_layout_form.addLayout(self.h_box_layout_form_3, 4)
        self.v_box_layout_form.addLayout(self.h_box_layout_form_4, 4)
        self.v_box_layout_form.addLayout(self.h_box_layout_password, 1)
        

        self.form_0 = QWidget()
        self.form_0.setLayout(self.v_box_layout_form)
        self.form_0.setMaximumWidth(950)
        self.form_0.setMaximumHeight(400)


        self.h_box_layout_form_1 = QHBoxLayout()
        self.h_box_layout_form_1.addWidget(self.form_0)
        self.h_box_layout_form_1.setAlignment(Qt.AlignmentFlag.AlignCenter)



        self.button_zip = QPushButton("Заархивировать все выбросы принудительно")
        self.button_zip.setMaximumWidth(950)
        self.button_zip.pressed.connect(self.zipPressed)

        self.h_box_layout_form_5 = QHBoxLayout()
        self.h_box_layout_form_5.addWidget(self.button_zip, 1)

        self.v_box_layout = QVBoxLayout()
        self.v_box_layout.addLayout(self.h_box_layout_1)
        self.v_box_layout.addWidget(self.label_1)
        self.v_box_layout.addLayout(self.h_box_layout_form_1)
        self.v_box_layout.addLayout(self.h_box_layout_form_5)
        self.v_box_layout.addWidget(self.label_2)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.v_box_layout)
        self.mainWidget.setMaximumHeight(500)
        


        y = np.load("./detector/0/coords.npy")
        x = np.arange(0, y.size)
        plotWidget = pg.plot(title="1")
        plotWidget.plot(x, y, pen=(0, 3))
        
        y_1 = np.load("./detector/1/coords.npy")
        x_1 = np.arange(0, y_1.size)
        plotWidget_1 = pg.plot(title="2")
        plotWidget_1.plot(x_1, y_1, pen=(1, 3))

        y_2 = np.load("./detector/2/coords.npy")
        x_2 = np.arange(0, y_2.size)
        plotWidget_2 = pg.plot(title="3")
        plotWidget_2.plot(x_2, y_2, pen=(2, 3))

        y_3 = np.load("./detector/3/coords.npy")
        x_3 = np.arange(0, y_3.size)
        plotWidget_3 = pg.plot(title="4")
        plotWidget_3.plot(x_3, y_3, pen=(3, 4))

        self.uppergraphLayout = QHBoxLayout()
        self.uppergraphLayout.addWidget(plotWidget, 1)
        self.uppergraphLayout.addWidget(plotWidget_1, 1)

        self.downgraphLayout = QHBoxLayout()
        self.downgraphLayout.addWidget(plotWidget_2, 1)
        self.downgraphLayout.addWidget(plotWidget_3, 1)

        self.allgraphLayout = QVBoxLayout()
        self.allgraphLayout.addLayout(self.uppergraphLayout, 1)
        self.allgraphLayout.addLayout(self.downgraphLayout, 1)

        self.allgraph = QWidget()
        self.allgraph.setLayout(self.allgraphLayout)
        self.allgraph.setMaximumHeight(500)
        self.allgraph.setMaximumWidth(950)

        self.centerGraphLayout = QHBoxLayout()
        self.centerGraphLayout.addWidget(self.allgraph)
        self.centerGraphLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)




        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.mainWidget, 2)
        self.mainLayout.addLayout(self.centerGraphLayout, 2)

        self.setLayout(self.mainLayout)
        