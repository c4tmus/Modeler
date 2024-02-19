# Import necessary modules
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,  QPushButton)
from PyQt6.QtCore import Qt, QMimeData, QEvent
from PyQt6.QtGui import QDrag, QPixmap, QPainter, QCursor

class ButtonNew(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)


    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.MouseButton.LeftButton:
            print('press')
            
    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.MouseButton.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)

        drag.setHotSpot(e.position().toPoint() - self.rect().topLeft())

        dropAction = drag.exec(Qt.DropAction.MoveAction)

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.setAcceptDrops(True)
        
    def initializeUI(self):
        """Set up the application's GUI."""
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("QPushButton Example")
        self.setMinimumSize(500,300)
        #setfixedsize for not changing size
        self.setUpMainWindow()
        self.show()
        
    def dragEnterEvent(self, e):
        e.accept()
  
    def dropEvent(self, e):
        position = e.position()
        self.button.move(position.toPoint())

        e.setDropAction(Qt.DropAction.MoveAction)
        e.accept()
    
    def setUpMainWindow(self):
        self.button1 = ButtonNew("Push Me1", self)
        self.button1.move(10, 20)
        self.button1.clicked.connect(self.buttonClicked1)

    def buttonClicked1(self):
        button_Number = "button1_" + str(self.times_pressed1)
        self.button_Number = ButtonNew(button_Number, self)
        self.button_Number.move(90, 20)
        self.button_Number.setDragEnabled(True)
        self.button_Number.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())