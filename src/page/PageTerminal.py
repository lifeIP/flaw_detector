from PyQt6.QtCore import QObject
from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *

    

class TerminalPage(QWidget):    
    pyqtSlot() 
    def terminal_update(self):
        with open("./terminal.log", "r") as file:
            lines = file.readlines()
            self.label_0.setText("\n".join(lines))
            
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
        self.timer.start(2500)

    def __init__(self):
        super().__init__()
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.terminal_update)
    

    def initUI(self):
        
        self.label_0 = QLabel()
        self.label_0.setTextFormat(Qt.TextFormat.AutoText)
        self.label_0.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_0.setScaledContents(True)

        font = QFont()
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1)
        self.label_0.setFont(font)

        
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.label_0)
        self.scrollArea.setStyleSheet("background-color: White")
        self.scrollArea.setWidgetResizable(True)

        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
    
    
        self.h_layout_0 = QHBoxLayout()
        self.h_layout_0.addWidget(self.scrollArea)

        self.setLayout(self.h_layout_0)

