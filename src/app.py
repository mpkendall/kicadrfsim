from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(1000, 600))

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        button_action = QAction("Open from KiCad", self)
        button_action.setStatusTip("Open .kicad_pcb file from KiCad")

        file_menu.addAction(button_action)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()