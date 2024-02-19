import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap, QDrag
from PyQt6.QtCore import Qt, QMimeData


class Icon(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        self.setScaledContents(True)
        self.setFixedSize(64, 64)
        self.setFrameStyle(0)
        self.drag_start_position = True

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.drag_start_position is not None:
            distance = (event.pos() - self.drag_start_position).manhattanLength()
            if distance >= QApplication.startDragDistance():
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setImageData(self.pixmap().toImage())
                drag.setMimeData(mime_data)
                drag.setPixmap(self.pixmap())
                drag.setHotSpot(event.pos() - self.rect().topLeft())

                # Ocultar el cursor mientras se está arrastrando
                drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)

                self.drag_start_position = None

class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setFixedSize(400, 600)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.pos())
            if item:
                pixmap_item = self.scene.addPixmap(item.pixmap())
                pixmap_item.setPos(self.mapToScene(event.pos()))
                pixmap_item.setFlag(QGraphicsView.ItemIsMovable, True)
                pixmap_item.setFlag(QGraphicsView.ItemIsSelectable, True)

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Iconos y Pizarra")
    window.setGeometry(100, 100, 800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)

    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    icon_container = QWidget()
    icon_layout = QVBoxLayout()
    icon_container.setLayout(icon_layout)

     # Agregamos los iconos
    icons = [
            QPixmap("Bizagi\icono1.png"),
            QPixmap("Bizagi\icono2.png"),
            QPixmap("Bizagi\icono3.png")
        ]
    for icon in icons:
        icon_label = Icon(icon)
        icon_layout.addWidget(icon_label)

    layout.addWidget(icon_container)

    canvas = Canvas()
    layout.addWidget(canvas)

    window.show()
    sys.exit(app.exec())