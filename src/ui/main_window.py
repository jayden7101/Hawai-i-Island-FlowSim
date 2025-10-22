# main_window.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QFormLayout,
    QDoubleSpinBox, QPushButton
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from map_creator import create_big_island_map  # import the map function
from vent_utils import find_closest_vent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Main Window
        self.setWindowTitle("Hawai'i Island Lava Flow Simulator")
        self.resize(1050, 850)
        icon = QIcon("src/ui/images/volcano_icon.png")
        self.setWindowIcon(icon)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main horizontal layout
        h_layout = QHBoxLayout()

        # ----- Left panel: 1/4 width, numeric inputs -----
        left_panel = QWidget()
        left_layout = QFormLayout()

        self.param1_input = QDoubleSpinBox()
        self.param1_input.setRange(0.0, 1000.0)
        self.param1_input.setSingleStep(0.1)

        self.param2_input = QDoubleSpinBox()
        self.param2_input.setRange(0.0, 1000.0)
        self.param2_input.setSingleStep(0.1)

        self.param3_input = QDoubleSpinBox()
        self.param3_input.setRange(0.0, 1000.0)
        self.param3_input.setSingleStep(0.1)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.read_inputs)

        left_layout.addRow("Param 1:", self.param1_input)
        left_layout.addRow("Param 2:", self.param2_input)
        left_layout.addRow("Param 3:", self.param3_input)
        left_layout.addRow(submit_btn)
        left_panel.setLayout(left_layout)

        # ----- Right panel: Folium map -----
        right_panel = QWebEngineView()
        map_data = create_big_island_map()
        right_panel.setHtml(map_data.getvalue().decode())

        # Add panels to layout with stretch factors
        h_layout.addWidget(left_panel, 1)   # 1/4 width
        h_layout.addWidget(right_panel, 3)  # 3/4 width

        central_widget.setLayout(h_layout)

    def read_inputs(self):
        param1 = self.param1_input.value()
        param2 = self.param2_input.value()
        param3 = self.param3_input.value()
        print("Parameter 1:", param1)
        print("Parameter 2:", param2)
        print("Parameter 3:", param3)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
