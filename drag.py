
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPixmap
from PyQt6.QtCore import Qt, QRectF,QMimeData
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,QPushButton
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen


class DiagramWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.items = []
        self.selected_item = True

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.pos())
            if item is not None:
                self.selected_item = item
            else:
                self.selected_item = self.addRect(event.pos().x(), event.pos().y(), 100, 50)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selected_item is not None:
            new_pos = self.mapToScene(event.pos())
            self.selected_item.setPos(new_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.selected_item is not None:
            self.selected_item = None
        super().mouseReleaseEvent(event)

    def addRect(self, x, y, w, h):
        rect_item = self.scene().addRect(x, y, w, h)
        rect_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        rect_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        return rect_item

    def addEllipse(self, x, y, w, h):
        ellipse_item = QGraphicsEllipseItem(x, y, w, h)
        ellipse_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        ellipse_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.scene().addItem(ellipse_item)
        return ellipse_item

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Diagramas de Flujo")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        self.shapes_layout = QVBoxLayout()
        layout.addLayout(self.shapes_layout)

        self.diagram_widget = DiagramWidget()
        layout.addWidget(self.diagram_widget)

        self.add_shape_button("Rectángulo", self.diagram_widget.addRect, 50, 50, 100, 50)
        self.add_shape_button("Elipse", self.diagram_widget.addEllipse, 50, 50, 100, 50)

    def add_shape_button(self, name, callback, *args):
        button = QPushButton(name)
        button.clicked.connect(lambda _, a=args: callback(*a))
        self.shapes_layout.addWidget(button)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
