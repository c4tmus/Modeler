import sys,os
from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QPixmap

class Icon(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        self.setScaledContents(True)
        self.setFixedSize(64, 64)
        self.setFrameStyle(0)
        self.drag_start_position = True

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
            
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("\n\n Drop image here \n\n")
        self.setStyleSheet('''
            QLabel{
                border : 4px dashed #aaa
            }
            ''')

    def setPixmap(self,image):
        super().setPixmap(image)


class  AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400,400)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout() 
        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)

        self.setLayout(mainLayout)
        
    def dragEnterEvent(self,event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.ClipOperation)
            file_path = event.mimeData().urls()[0].tolocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()
app = QApplication(sys.argv)    
demo = AppDemo()
demo.show()
sys.exit(app.exec())

