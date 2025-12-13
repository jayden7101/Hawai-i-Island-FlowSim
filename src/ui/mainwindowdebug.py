# main_window.py
import sys
import os
import tempfile
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QFormLayout,
    QDoubleSpinBox, QPushButton, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from map_creator import create_big_island_map
from vent_utils import find_closest_vent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Main Window
        self.setWindowTitle("Hawai'i Island Lava Flow Simulator")
        self.resize(1050, 850)
        
        # Try to load icon, but don't crash if it's missing
        try:
            icon = QIcon("src/ui/images/volcano_icon.png")
            self.setWindowIcon(icon)
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")
        
        # Keep track of temp file path so we can clean up later
        self._map_temp_path = None
        
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
        
        # Add coordinate labels
        self.lat_label = QLabel("Latitude: ")
        self.lon_label = QLabel("Longitude: ")
        self.status_label = QLabel("Status: Ready")
        left_layout.addRow("Clicked Latitude:", self.lat_label)
        left_layout.addRow("Clicked Longitude:", self.lon_label)
        left_layout.addRow("Status:", self.status_label)
        
        left_panel.setLayout(left_layout)
        
        # ----- Right panel: Folium map -----
        right_panel = QWebEngineView()
        
        # Set up QWebChannel BEFORE loading the HTML
        self.channel = QWebChannel()
        self.bridge = MapBridge(self)
        self.channel.registerObject("bridge", self.bridge)
        right_panel.page().setWebChannel(self.channel)
        
        # Create map and write to temp file
        map_data = create_big_island_map()
        map_bytes = map_data.getvalue()
        
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        try:
            tmp.write(map_bytes)
            tmp.flush()
            tmp.close()
            
            self._map_temp_path = tmp.name
            
            # Inject JavaScript into HTML BEFORE loading
            self.inject_js_into_html(self._map_temp_path)
            
            file_url = QUrl.fromLocalFile(os.path.abspath(self._map_temp_path))
            right_panel.load(file_url)
            
        except Exception as e:
            print(f"ERROR creating map: {e}")
            try:
                tmp.close()
            except Exception:
                pass
            if tmp.name and os.path.exists(tmp.name):
                os.remove(tmp.name)
            raise
        
        # Add panels to layout with stretch factors
        h_layout.addWidget(left_panel, 1)
        h_layout.addWidget(right_panel, 3)
        
        central_widget.setLayout(h_layout)
        self._right_panel = right_panel
    
    def read_inputs(self):
        param1 = self.param1_input.value()
        param2 = self.param2_input.value()
        param3 = self.param3_input.value()
        print("Parameter 1:", param1)
        print("Parameter 2:", param2)
        print("Parameter 3:", param3)
    
    def play_video_at_location(self, lat, lon):
        """Play video overlay at specified coordinates."""
        try:
            self.status_label.setText("Status: Loading video...")
            print(f"play_video_at_location called with lat={lat}, lon={lon}")
            
            # Define video bounds around the point
            bounds = [
                [lat - 0.1, lon - 0.1],  # Southwest corner
                [lat + 0.1, lon + 0.1]   # Northeast corner
            ]
            
            # Get video path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            video_path = os.path.join(script_dir, "animation_videos", "mlv5_3.webm")
            
            print(f"Looking for video at: {video_path}")
            
            if not os.path.exists(video_path):
                error_msg = f"ERROR: Video not found at {video_path}"
                print(error_msg)
                self.status_label.setText(f"Status: {error_msg}")
                return
            
            print(f"Video found! Size: {os.path.getsize(video_path)} bytes")
            video_url = QUrl.fromLocalFile(video_path).toString()
            print(f"Video URL: {video_url}")
            
            # JavaScript to create video overlay
            js_code = f"""
            (function() {{
                console.log("JavaScript: Starting video overlay");
                var bounds = {bounds};
                var videoUrl = "{video_url}";
                console.log("Video URL:", videoUrl);
                console.log("Bounds:", bounds);
                
                // Find Leaflet map
                var map = null;
                for (var key in window) {{
                    if (window[key] instanceof L.Map) {{
                        map = window[key];
                        break;
                    }}
                }}
                
                if (!map) {{
                    console.error("Map not found");
                    return;
                }}
                
                console.log("Map found:", map);
                
                // Remove previous video if exists
                if (window.currentVideo) {{
                    console.log("Removing previous video");
                    if (window.currentVideo._video) {{
                        window.currentVideo._video.pause();
                    }}
                    map.removeLayer(window.currentVideo);
                }}
                
                // Create video element
                var video = document.createElement('video');
                video.src = videoUrl;
                video.autoplay = true;
                video.muted = true;
                video.loop = true;
                video.style.width = '100%';
                video.style.height = '100%';
                video.style.objectFit = 'fill';
                
                console.log("Video element created");
                
                // Custom Leaflet layer for video
                var VideoOverlay = L.ImageOverlay.extend({{
                    onAdd: function(map) {{
                        console.log("VideoOverlay onAdd called");
                        if (!this._image) {{
                            this._image = video;
                            this.getPane().appendChild(video);
                            this._reset();
                        }}
                    }},
                    
                    _reset: function() {{
                        var image = this._image;
                        var bounds = this._bounds;
                        var size = this._map.latLngToLayerPoint(bounds.getNorthEast())
                            .subtract(this._map.latLngToLayerPoint(bounds.getSouthWest()));
                        var pos = this._map.latLngToLayerPoint(bounds.getNorthWest());
                        
                        L.DomUtil.setPosition(image, pos);
                        image.style.width = size.x + 'px';
                        image.style.height = size.y + 'px';
                    }}
                }});
                
                // Create and add overlay
                window.currentVideo = new VideoOverlay(videoUrl, bounds, {{
                    opacity: 0.8,
                    interactive: false
                }});
                
                console.log("VideoOverlay created");
                
                window.currentVideo._video = video;
                window.currentVideo.addTo(map);
                
                console.log("VideoOverlay added to map");
                
                // Start playback
                video.play().then(function() {{
                    console.log("Video playback started successfully");
                }}).catch(function(err) {{
                    console.error("Error playing video:", err);
                }});
            }})();
            """
            
            print("Executing JavaScript...")
            self._right_panel.page().runJavaScript(js_code)
            self.status_label.setText("Status: Video playing")
            print("JavaScript execution completed")
            
        except Exception as e:
            error_msg = f"ERROR in play_video_at_location: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.status_label.setText(f"Status: {error_msg}")
    
    def closeEvent(self, event):
        # Clean up the temporary map file when the window is closed
        try:
            if self._map_temp_path and os.path.exists(self._map_temp_path):
                os.remove(self._map_temp_path)
        except Exception:
            pass
        super().closeEvent(event)
    
    def inject_js_into_html(self, path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        
        injection = """
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function () {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                window.bridge = channel.objects.bridge;
                
                // Find Folium's Leaflet map instance
                let leafletMap = null;
                for (let key in window) {
                    if (window[key] instanceof L.Map) {
                        leafletMap = window[key];
                        break;
                    }
                }
                
                if (!leafletMap) {
                    console.error("No Leaflet map object found.");
                    return;
                }
                
                console.log("Leaflet map found, adding click listener");
                
                leafletMap.on('click', function (e) {
                    console.log("Map clicked at:", e.latlng.lat, e.latlng.lng);
                    bridge.sendCoordinates(e.latlng.lat, e.latlng.lng);
                });
            });
        });
        </script>
        """
        
        # inject before </body>
        html = html.replace("</body>", injection + "\n</body>")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)


class MapBridge(QObject): 
    def __init__(self, main_window): 
        super().__init__()
        self.main_window = main_window
    
    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lon):
        try:
            print(f"MapBridge received coordinates: lat={lat}, lon={lon}")
            self.main_window.lat_label.setText(f"{lat:.6f}")
            self.main_window.lon_label.setText(f"{lon:.6f}")
            
            # Play video at clicked location
            self.main_window.play_video_at_location(lat, lon)
            
        except Exception as e:
            print(f"ERROR in sendCoordinates: {e}")
            import traceback
            traceback.print_exc()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
