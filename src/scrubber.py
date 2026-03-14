"""
scrubber.py

this is a self-contained script for everything to do with the scrubber, including
its style sheets.

this allows for easier moving of the scrubber within the gui script.

functions + variables with an underscore before their names are things that
only interact within this script
"""

from PyQt5.QtWidgets import ( QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLabel,
                              QPushButton, QStyle, QStyleOptionSlider)
from PyQt5.QtCore import Qt, QTimer


def _format_time(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"

class Scrubber(QWidget):

    INTERVAL_MS = 1000 # increased from 500 to reduce the number of py - js calls

    def __init__(self, theme, parent = None):
        super().__init__(parent)
        self._theme = theme          # enable theme switching
        self._page = None           
        self._duration = 0.0        # video duration in sec
        self._is_dragging = False   # true when user drags slider
        self._active = False        # true when video playing/paused

        self._build_ui()

        # js timer
        self._timer = QTimer(self)
        self._timer.setInterval(self.INTERVAL_MS)
        self._timer.timeout.connect(self._poll_time)

        self.setEnabled(False)

    def setPage(self, page):
        self._page = page

    def simulationStarted(self):
        self._active = True
        self.setEnabled(True)
        self._duration = 0.0
        self._slider.setValue(0)
        self._time_label.setText("0:00 / --:--")
        QTimer.singleShot(300, self._timer.start)

    def simulationPaused(self):
        pass

    def simulationReset(self):
        self._active = False
        self._timer.stop()
        self._duration = 0.0
        self._slider.setValue(0)
        self._time_label.setText("0:00 / 00:00")
        self.setEnabled(False)

    """
    SCRUBBER UI
    """

    def _build_ui(self):
        outer = QVBoxLayout()
        outer.setContentsMargins(4, 4, 4, 2)
        outer.setSpacing(3)
        self.setLayout(outer)

        t = self._theme # use to call theme styles

        # slider row
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(0, 1000)
        self._slider.setValue(0)
        self._slider.setStyleSheet(t.STYLE_SCRUBBER_SLIDER)
        self._slider.sliderPressed.connect(self._drag_start)
        self._slider.sliderReleased.connect(self._drag_end)
       
        outer.addWidget(self._slider)

        # control row: time, ff/rewind btn
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(4)
        ctrl_row.setContentsMargins(0, 0, 0, 0)

        self._time_label = QLabel("0:00 / 0:00")
        self._time_label.setStyleSheet(t.STYLE_SCRUBBER_LABEL)
        ctrl_row.addWidget(self._time_label)

        ctrl_row.addStretch()

        # rewind 10sec
        self._rw_btn = QPushButton( "<< 10s")
        self._rw_btn.setStyleSheet(t.STYLE_SCRUBBER_BTN)
        self._rw_btn.setFixedHeight(26)
        self._rw_btn.setToolTip("Rewind by 10 seconds")
        self._rw_btn.clicked.connect(lambda: self._seek_relative(-10))
        ctrl_row.addWidget(self._rw_btn)

        # ff 10 sec
        self._ff_btn = QPushButton("10s >>")
        self._ff_btn.setStyleSheet(t.STYLE_SCRUBBER_BTN)
        self._ff_btn.setFixedHeight(26)
        self._ff_btn.setToolTip("Fast forward 10 seconds")
        self._ff_btn.clicked.connect(lambda: self._seek_relative(10))
        ctrl_row.addWidget(self._ff_btn)

        # skip to end
        self._end_btn = QPushButton(" >>| End")
        self._end_btn.setStyleSheet(t.STYLE_SCRUBBER_BTN)
        self._end_btn.setFixedHeight(26)
        self._end_btn.setToolTip("Skip to end and pause")
        self._end_btn.clicked.connect(self._skip_to_end)
        ctrl_row.addWidget(self._end_btn)

        outer.addLayout(ctrl_row)

    def _js(self,script):
        if self._page:
            self._page.runJavaScript(script)

    # ask for current time + duration, update the ui
    def _poll_time(self):
        if not self._page or self._is_dragging:
            return
        self._page.runJavaScript ("""
            (function() {
                var v = window.currentVideoElement;
                if (!v) return null;
                return { current: v.currentTime, duration: v.duration || 0 };
                })()
                """,
                self._handle_time_result
            )

    def _handle_time_result(self, result):
        if result is None:
            return
        current = result.get("current", 0) or 0
        duration = result.get("duration", 0) or 0

        if duration > 0:
            self._duration = duration
            pos = int((current / duration) * 1000)
            self._slider.setValue(pos)
            self._time_label.setText(f"{_format_time(current)} / {_format_time(duration)}")

    def _drag_start(self):
        self._is_dragging = True

    # look to wherever user dropped slider
    def _drag_end(self):
        self._is_dragging = False
        if self._duration > 0:
            target = (self._slider.value() / 1000) * self._duration
            self._js(f"if(window.currentVideoElement) window.currentVideoElement.currentTime = {target};")

    # seek fwd/backward 
    def _seek_relative(self, delta_seconds):
        self._js(
            f"""
            if (window.currentVideoElement) {{
                var v = window.currentVideoElement;
                v.currentTime = Math.max(0, Math.min(v.currentTime + {delta_seconds}, v.duration));
            }}
            """
        )

    def _skip_to_end(self):
        self._js(
            """
            if (window.currentVideoElement) {
                var v = window.currentVideoElement;
                v.currentTime = v.duration;
                v.pause();
            }
            """
        )

    # change theme
    def applyTheme(self, theme):
        self._theme = theme
        self._slider.setStyleSheet(theme.STYLE_SCRUBBER_SLIDER)
        self._time_label.setStyleSheet(theme.STYLE_SCRUBBER_LABEL)
        self._rw_btn.setStyleSheet(theme.STYLE_SCRUBBER_BTN)
        self._ff_btn.setStyleSheet(theme.STYLE_SCRUBBER_BTN)
        self._end_btn.setStyleSheet(theme.STYLE_SCRUBBER_BTN)


