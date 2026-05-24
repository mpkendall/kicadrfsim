import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QVector3D, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QWidget,
    QFileDialog,
)
from PyQt6.Qt3DCore import QEntity, QTransform
from PyQt6.Qt3DExtras import (
    Qt3DWindow,
    QPhongMaterial,
    QOrbitCameraController,
)
import sexpdata


def parse_kicad_pcb(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = sexpdata.load(f)
    return data


def extract_fcu_segments(data):
    """Extract all F.Cu trace segments as (start, end, width) tuples."""
    segments = []

    def walk(node):
        if not isinstance(node, list) or len(node) == 0:
            return
        tag = node[0]
        if isinstance(tag, sexpdata.Symbol):
            tag = tag.value()

        if tag == "segment":
            layer = None
            start = None
            end = None
            width = 0.1  # default mm
            for item in node[1:]:
                if isinstance(item, list) and len(item) >= 1:
                    sub = item[0]
                    if isinstance(sub, sexpdata.Symbol):
                        sub = sub.value()
                    if sub == "layer" and len(item) >= 2:
                        layer = item[1]
                        if isinstance(layer, sexpdata.Symbol):
                            layer = layer.value()
                    elif sub == "start" and len(item) >= 3:
                        start = (float(item[1]), float(item[2]))
                    elif sub == "end" and len(item) >= 3:
                        end = (float(item[1]), float(item[2]))
                    elif sub == "width" and len(item) >= 2:
                        width = float(item[1])
            if layer == "F.Cu" and start and end:
                segments.append((start, end, width))

        for item in node[1:]:
            walk(item)

    walk(data)
    return segments


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kicadrfsim")
        self.setMinimumSize(QSize(1000, 600))

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        button_action = QAction("Open from KiCad", self)
        button_action.setStatusTip("Open .kicad_pcb file from KiCad")
        file_menu.addAction(button_action)
        button_action.triggered.connect(self.open_from_kicad)

        self.setStatusBar(QStatusBar(self))

    def open_from_kicad(self):
        _file_dialog = QFileDialog(self)
        _file_dialog.setNameFilter("KiCad PCB Files (*.kicad_pcb)")
        if not _file_dialog.exec():
            return

        file_path = _file_dialog.selectedFiles()[0]
        print(f"Selected file: {file_path}")

        data = parse_kicad_pcb(file_path)
        segments = extract_fcu_segments(data)
        print(f"Found {len(segments)} F.Cu segments")

        print("First 5 segments:")
        for i, (start, end, width) in enumerate(segments[:5]):
            print(f"  {i+1}. Start: {start}, End: {end}, Width: {width}")
