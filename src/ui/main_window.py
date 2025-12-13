import sys
import os
import tempfile

from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QRadioButton, QButtonGroup
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon

from map_creator import create_big_island_map
from vent_utils import find_closest_vent


class MapBridge(QObject):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lon):

        # Update coordinate labels
        self.main_window.lat_label.setText(f"{lat:.5f}")
        self.main_window.lon_label.setText(f"{lon:.5f}")

        self.main_window.current_lat = lat
        self.main_window.current_lon = lon

        # Find closest vent
        closest_vent, distance_km = find_closest_vent([lat, lon])

        # Persist results on main window
        self.main_window.closest_vent = closest_vent
        self.main_window.closest_distance = distance_km

        # Update UI
        vent_lat, vent_lon = closest_vent
        self.main_window.closest_vent_label.setText(f"{vent_lat:.5f}, {vent_lon:.5f}")
        self.main_window.closest_distance_label.setText(f"{distance_km:.2f}")

        # Debug Output 
        print(
            f"Clicked at ({lat:.5f}, {lon:.5f}) → "
            f"nearest vent at ({closest_vent[0]:.5f}, {closest_vent[1]:.5f}), "
            f"{distance_km:.2f} km away"
        )



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ----- Main window setup -----
        self.setWindowTitle("Hawai'i Island Lava Flow Simulator")
        self.resize(1050, 850)
        self.setWindowIcon(QIcon("src/ui/images/volcano_icon.png"))

        # State
        self._map_temp_path = None
        self.current_lat = None
        self.current_lon = None
        self.current_viscosity = None
        self.current_vent_size = None
        self.current_effusion_rate = None
        self.closest_vent = None
        self.closest_distance = None

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        h_layout = QHBoxLayout(central_widget)

        # ===========================================================
        # LEFT PANEL
        # ===========================================================
        left_panel = QWidget()
        left_layout = QFormLayout(left_panel)

        # Viscosity
        self.viscosity_group = QButtonGroup(self)
        self.viscosity_low = QRadioButton("Low")
        self.viscosity_high = QRadioButton("High")
        self.viscosity_low.setChecked(True)
        self.viscosity_group.addButton(self.viscosity_low, 0)
        self.viscosity_group.addButton(self.viscosity_high, 1)

        visc_widget = QWidget()
        visc_layout = QHBoxLayout(visc_widget)
        visc_layout.setContentsMargins(0, 0, 0, 0)
        visc_layout.addWidget(self.viscosity_low)
        visc_layout.addWidget(self.viscosity_high)
        left_layout.addRow("Viscosity:", visc_widget)

        # Vent size
        self.ventsize_group = QButtonGroup(self)
        self.vent_small = QRadioButton("Small")
        self.vent_large = QRadioButton("Large")
        self.vent_small.setChecked(True)
        self.ventsize_group.addButton(self.vent_small, 0)
        self.ventsize_group.addButton(self.vent_large, 1)

        vent_widget = QWidget()
        vent_layout = QHBoxLayout(vent_widget)
        vent_layout.setContentsMargins(0, 0, 0, 0)
        vent_layout.addWidget(self.vent_small)
        vent_layout.addWidget(self.vent_large)
        left_layout.addRow("Vent Size:", vent_widget)

        # Effusion rate
        self.effusion_group = QButtonGroup(self)
        self.effusion_low = QRadioButton("Low")
        self.effusion_high = QRadioButton("High")
        self.effusion_low.setChecked(True)
        self.effusion_group.addButton(self.effusion_low, 0)
        self.effusion_group.addButton(self.effusion_high, 1)

        eff_widget = QWidget()
        eff_layout = QHBoxLayout(eff_widget)
        eff_layout.setContentsMargins(0, 0, 0, 0)
        eff_layout.addWidget(self.effusion_low)
        eff_layout.addWidget(self.effusion_high)
        left_layout.addRow("Effusion Rate:", eff_widget)

        # Submit
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.read_inputs)
        left_layout.addRow(submit_btn)

        # Coordinate labels
        self.lat_label = QLabel("—")
        self.lon_label = QLabel("—")
        left_layout.addRow("Clicked Latitude:", self.lat_label)
        left_layout.addRow("Clicked Longitude:", self.lon_label)

        # Closest vent labels
        self.closest_vent_label = QLabel("—")
        self.closest_distance_label = QLabel("—")
        left_layout.addRow("Closest Vent:", self.closest_vent_label)
        left_layout.addRow("Distance (km):", self.closest_distance_label)

        # ===========================================================
        # RIGHT PANEL (Map)
        # ===========================================================
        right_panel = QWebEngineView()

        self.channel = QWebChannel()
        self.bridge = MapBridge(self)
        self.channel.registerObject("bridge", self.bridge)
        right_panel.page().setWebChannel(self.channel)

        map_data = create_big_island_map()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmp.write(map_data.getvalue())
        tmp.close()
        self._map_temp_path = tmp.name

        self.inject_js_into_html(self._map_temp_path)
        right_panel.load(QUrl.fromLocalFile(os.path.abspath(self._map_temp_path)))

        h_layout.addWidget(left_panel, 1)
        h_layout.addWidget(right_panel, 3)

    def inject_js_into_html(self, path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        injection = """
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function () {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.bridge = channel.objects.bridge;
        var leafletMap = null;
        for (var key in window) {
            if (window[key] instanceof L.Map) {
                leafletMap = window[key];
                break;
            }
        }
        if (!leafletMap) return;
        leafletMap.on('click', function (e) {
            bridge.sendCoordinates(e.latlng.lat, e.latlng.lng);
        });
    });
});
</script>
"""
        html = html.replace("</body>", injection + "\n</body>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    def read_inputs(self):
        self.current_viscosity = "low" if self.viscosity_group.checkedId() == 0 else "high"
        self.current_vent_size = "small" if self.ventsize_group.checkedId() == 0 else "large"
        self.current_effusion_rate = "low" if self.effusion_group.checkedId() == 0 else "high"

        print("Viscosity:", self.current_viscosity)
        print("Vent Size:", self.current_vent_size)
        print("Effusion Rate:", self.current_effusion_rate)
        print("Clicked Lat:", self.current_lat)
        print("Clicked Lon:", self.current_lon)

        if self.closest_vent:
            print("Closest Vent:", self.closest_vent["name"])
            print("Distance (km):", self.closest_distance)
        else:
            print("Closest Vent: None selected")

    def closeEvent(self, event):
        if self._map_temp_path and os.path.exists(self._map_temp_path):
            os.remove(self._map_temp_path)
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
