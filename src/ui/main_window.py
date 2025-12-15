import sys
import os
import tempfile

from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QRadioButton, QButtonGroup
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon

from map_creator import create_big_island_map
from vent_utils import find_closest_vent


# ==========================================================
# MAP ↔ PYTHON BRIDGE
# ==========================================================
class MapBridge(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lon):
        print(f"[DEBUG] Map clicked at lat={lat}, lon={lon}")

        self.main_window.current_lat = lat
        self.main_window.current_lon = lon

        self.main_window.lat_label.setText(f"{lat:.5f}")
        self.main_window.lon_label.setText(f"{lon:.5f}")

        closest_vent, distance_km = find_closest_vent([lat, lon])

        self.main_window.closest_vent = closest_vent
        self.main_window.closest_distance = distance_km

        vent_lat, vent_lon = closest_vent
        self.main_window.closest_vent_label.setText(
            f"{vent_lat:.5f}, {vent_lon:.5f}"
        )
        self.main_window.closest_distance_label.setText(
            f"{distance_km:.2f}"
        )

        print(
            f"[DEBUG] Closest vent: ({vent_lat:.5f}, {vent_lon:.5f}) "
            f"distance={distance_km:.2f} km"
        )

        self.main_window.run_simulation_for_current_state()


# ==========================================================
# MAIN WINDOW
# ==========================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print("[DEBUG] Initializing MainWindow")

        self.setWindowTitle("Hawai'i Island Lava Flow Simulator")
        self.resize(1050, 850)

        try:
            self.setWindowIcon(QIcon("src/ui/images/volcano_icon.png"))
        except Exception as e:
            print(f"[DEBUG] Icon load failed: {e}")

        # --------------------------------------------------
        # STATE
        # --------------------------------------------------
        self._map_temp_path = None

        self.current_lat = None
        self.current_lon = None
        self.current_viscosity = "low"
        self.current_vent_size = "small"
        self.current_effusion_rate = "low"

        self.closest_vent = None
        self.closest_distance = None

        # --------------------------------------------------
        # LAYOUT
        # --------------------------------------------------
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        h_layout = QHBoxLayout(central_widget)

        # ==================================================
        # LEFT PANEL
        # ==================================================
        left_panel = QWidget()
        left_layout = QFormLayout(left_panel)

        # -------- Viscosity --------
        self.viscosity_group = QButtonGroup(self)
        visc_low = QRadioButton("Low")
        visc_high = QRadioButton("High")
        visc_low.setChecked(True)

        self.viscosity_group.addButton(visc_low, 0)
        self.viscosity_group.addButton(visc_high, 1)

        visc_widget = QWidget()
        visc_layout = QHBoxLayout(visc_widget)
        visc_layout.setContentsMargins(0, 0, 0, 0)
        visc_layout.addWidget(visc_low)
        visc_layout.addWidget(visc_high)

        left_layout.addRow("Viscosity:", visc_widget)

        # -------- Vent Size --------
        self.vent_group = QButtonGroup(self)
        vent_small = QRadioButton("Small")
        vent_large = QRadioButton("Large")
        vent_small.setChecked(True)

        self.vent_group.addButton(vent_small, 0)
        self.vent_group.addButton(vent_large, 1)

        vent_widget = QWidget()
        vent_layout = QHBoxLayout(vent_widget)
        vent_layout.setContentsMargins(0, 0, 0, 0)
        vent_layout.addWidget(vent_small)
        vent_layout.addWidget(vent_large)

        left_layout.addRow("Vent Size:", vent_widget)

        # -------- Effusion Rate --------
        self.effusion_group = QButtonGroup(self)
        eff_low = QRadioButton("Low")
        eff_high = QRadioButton("High")
        eff_low.setChecked(True)

        self.effusion_group.addButton(eff_low, 0)
        self.effusion_group.addButton(eff_high, 1)

        eff_widget = QWidget()
        eff_layout = QHBoxLayout(eff_widget)
        eff_layout.setContentsMargins(0, 0, 0, 0)
        eff_layout.addWidget(eff_low)
        eff_layout.addWidget(eff_high)

        left_layout.addRow("Effusion Rate:", eff_widget)

        submit_btn = QPushButton("Submit Parameters")
        submit_btn.clicked.connect(self.read_inputs)
        left_layout.addRow(submit_btn)

        # -------- Labels --------
        self.lat_label = QLabel("—")
        self.lon_label = QLabel("—")
        self.closest_vent_label = QLabel("—")
        self.closest_distance_label = QLabel("—")
        self.status_label = QLabel("Ready")

        left_layout.addRow("Clicked Latitude:", self.lat_label)
        left_layout.addRow("Clicked Longitude:", self.lon_label)
        left_layout.addRow("Closest Vent:", self.closest_vent_label)
        left_layout.addRow("Distance (km):", self.closest_distance_label)
        left_layout.addRow("Status:", self.status_label)

        # ==================================================
        # RIGHT PANEL (MAP)
        # ==================================================
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

        self._right_panel = right_panel

        print("[DEBUG] MainWindow initialized successfully")

    # ==================================================
    # PARAMETER INPUT
    # ==================================================
    def read_inputs(self):
        self.current_viscosity = (
            "low" if self.viscosity_group.checkedId() == 0 else "high"
        )
        self.current_vent_size = (
            "small" if self.vent_group.checkedId() == 0 else "large"
        )
        self.current_effusion_rate = (
            "low" if self.effusion_group.checkedId() == 0 else "high"
        )

        print("[DEBUG] Parameters updated:")
        print("  Viscosity:", self.current_viscosity)
        print("  Vent Size:", self.current_vent_size)
        print("  Effusion:", self.current_effusion_rate)

    # ==================================================
    # SIMULATION DISPATCH
    # ==================================================
    def run_simulation_for_current_state(self):
        if not self.closest_vent:
            print("[DEBUG] No vent selected, aborting simulation")
            return

        animation_file = self.select_animation()
        lat, lon = self.closest_vent

        print(f"[DEBUG] Running animation '{animation_file}'")

        self.play_video_at_location(lat, lon, animation_file)

    def select_animation(self):
        key = (
            self.current_viscosity,
            self.current_vent_size,
            self.current_effusion_rate,
        )

        animation_map = {
            ("low", "small", "low"): "mlv5_3.webm",
            ("low", "small", "high"): "mlv5_3.webm",
            ("low", "large", "low"): "mlv5_3.webm",
            ("low", "large", "high"): "mlv5_3.webm",
            ("high", "small", "low"): "mlv5_3.webm",
            ("high", "small", "high"): "mlv5_3.webm",
            ("high", "large", "low"): "mlv5_3.webm",
            ("high", "large", "high"): "mlv5_3.webm",
        }

        return animation_map.get(key, "default.webm")

    # ==================================================
    # VIDEO OVERLAY
    # ==================================================
    def play_video_at_location(self, lat, lon, filename):
        print(f"[DEBUG] Playing video {filename} at {lat}, {lon}")

        bounds = [
            [lat - 0.1, lon - 0.1],
            [lat + 0.1, lon + 0.1],
        ]

        video_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "animation_videos",
            filename,
        )

        if not os.path.exists(video_path):
            print(f"[ERROR] Video not found: {video_path}")
            self.status_label.setText("Video not found")
            return

        video_url = QUrl.fromLocalFile(video_path).toString()

        js = f"""
        (function() {{
            var bounds = {bounds};
            var map = null;
            for (var k in window) {{
                if (window[k] instanceof L.Map) {{
                    map = window[k];
                    break;
                }}
            }}
            if (!map) return;

            if (window.currentVideo) {{
                map.removeLayer(window.currentVideo);
            }}

            window.currentVideo = L.videoOverlay(
                "{video_url}",
                bounds,
                {{ autoplay: true, loop: true, opacity: 0.8 }}
            ).addTo(map);
        }})();
        """

        self._right_panel.page().runJavaScript(js)
        self.status_label.setText("Simulation running")

    # ==================================================
    # MAP JS INJECTION
    # ==================================================
    def inject_js_into_html(self, path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        injection = """
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function () {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.bridge = channel.objects.bridge;
        var map = null;
        for (var k in window) {
            if (window[k] instanceof L.Map) {
                map = window[k];
                break;
            }
        }
        if (!map) return;
        map.on('click', function (e) {
            bridge.sendCoordinates(e.latlng.lat, e.latlng.lng);
        });
    });
});
</script>
"""
        html = html.replace("</body>", injection + "\n</body>")

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    def closeEvent(self, event):
        print("[DEBUG] Cleaning up temporary files")
        if self._map_temp_path and os.path.exists(self._map_temp_path):
            os.remove(self._map_temp_path)
        super().closeEvent(event)


# ==========================================================
# ENTRY POINT
# ==========================================================
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
