import sys
import os
import shutil
import tempfile

from PyQt5.QtCore import QUrl, QObject, pyqtSlot, Qt, QFile, QIODevice
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFormLayout, QLabel, QPushButton, QRadioButton, QButtonGroup,
    QSplitter, QFrame, QMessageBox, QTabWidget,QTextEdit, QScrollArea)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtGui import QFontInfo

from map_creator import create_big_island_map
from vent_utils import find_closest_vent

from style_sheets import *
from text_descriptions import *

# Configuration/Consts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Paths for assets
ICON_PATH = os.path.join(PROJECT_ROOT, "images", "volcano_icon.png")
JS_BRIDGE_PATH = os.path.join(PROJECT_ROOT, "js", "map_bridge.js")
VIDEO_DIR_PATH = os.path.join(PROJECT_ROOT, "animation_videos")

WINDOW_TITLE = "Lava Flow Simulation"



# Map Bridge (JS and Python link)
class MapBridge(QObject):
    def __init__(self, parentWindow):
        super().__init__()
        self.parentWindow = parentWindow

    @pyqtSlot(float, float) 
    def sendCoordinates(self, lat, lon):
        # Clicks from JS (the coords --> lat & long)
        try:
            print(f"Map clicked: {lat}, {lon}")
            
            coords = (lat, lon)
            self.parentWindow.currentCoords = coords
            
            # [coords, distance] returned
            ventData = find_closest_vent([lat, lon])
            
            if ventData is None:
                return

            closestVent = ventData[0]
            distanceKm = ventData[1]
            
            self.parentWindow.closestVent = closestVent
            statusText = f"Selected: {lat:.4f}, {lon:.4f} | Ready to Run"
            self.parentWindow.infoBubb.setText(statusText)
            
            # Reset state when new click
            self.parentWindow.isDataPlaying = False
            self.parentWindow.updateButtonState(isPlaying=False)

        except Exception as error:
            print(f"Bridge error: {error}") # In case

# Gui Class (main window)
class LavaGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        # Init window
        self.setWindowTitle(WINDOW_TITLE)
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.85), int(screen.height() * 0.85))
        
        try:
            if os.path.exists(ICON_PATH):
                self.setWindowIcon(QIcon(ICON_PATH))
        except Exception:
            pass

        # State
        self.closestVent = None
        self.tempFiles = list()
        self.isDataPlaying = False 

        # Splitter 
        windowSplit = QSplitter(Qt.Horizontal)
        
        leftPane = QWidget()
        leftPane.setStyleSheet(STYLE_PANES)
        self.setupControls(leftPane)
        
        rightPaneWidget = QWidget()
        rightPaneWidget.setStyleSheet(f"background-color: {COLOR_PANES};")
        self.setupMapArea(rightPaneWidget)

        windowSplit.addWidget(leftPane)
        windowSplit.addWidget(rightPaneWidget)
        windowSplit.setSizes([250, 790])
        windowSplit.setStyleSheet(STYLE_SPLITTER)
        windowSplit.setHandleWidth(6)

        self.setCentralWidget(windowSplit)

    def setupControls(self, panel):
        screen = QApplication.primaryScreen().availableGeometry()
        btn_width = int(screen.width()*.08)

        layout = QVBoxLayout()
        panel.setLayout(layout)

        hBox = QHBoxLayout()
        
        self.btnInfo = QPushButton("i")
        self.btnInfo.setFixedSize(30, 30)
        self.btnInfo.setStyleSheet(STYLE_INFO_BTN)
        self.btnInfo.clicked.connect(self.showInfo)

        # disclaimer button
        self.btnDisclaimer = QPushButton("▶  Disclaimer")
        self.btnDisclaimer.setStyleSheet(STYLE_DISC_PARAM_BTN)
        self.btnDisclaimer.setCheckable(True)
        self.btnDisclaimer.clicked.connect(self.toggleDisclaimerPanel)
        self.btnDisclaimer.setFixedWidth(btn_width)

        # parameter button
        self.btnParameter = QPushButton("▶  Parameters")
        self.btnParameter.setStyleSheet(STYLE_DISC_PARAM_BTN)
        self.btnParameter.setCheckable(True)
        self.btnParameter.clicked.connect(self.toggleParameterPanel)
        self.btnParameter.setFixedWidth(btn_width)

        hBox.addWidget(self.btnInfo)
        hBox.addWidget(self.btnDisclaimer)
        hBox.addWidget(self.btnParameter)
        hBox.addStretch()
        layout.addLayout(hBox)
        self.addSeparator(layout)

        # configuration parameter radio buttons
        self.groupVisc = self.createRadioGroup(layout, "Viscosity", ["Low \n(Pahoehoe)", "High \n('A'a)"])
        self.addSeparator(layout)

        self.groupVent = self.createRadioGroup(layout, "Vent Size", ["Small", "Large"])
        self.addSeparator(layout)

        self.groupEff = self.createRadioGroup(layout, "Effusion Rate", ["Low", "High"])
        self.addSeparator(layout)

        # text boxes for disclaimer and parameter boxes
        self.disclaimerBox = QTextEdit()
        self.disclaimerBox.setHtml(DISCLAIMER_TEXT)
        self.disclaimerBox.setStyleSheet(STYLE_DISC_PARAM_BOXES)
        self.disclaimerBox.setReadOnly(True)
        self.disclaimerBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.disclaimerBox.setFixedHeight(int(screen.height() * 0.30))
        self.disclaimerBox.setVisible(False)
        layout.addWidget(self.disclaimerBox)

        self.parameterBox = QTextEdit()
        self.parameterBox.setHtml(PARAMETER_TEXT)
        self.parameterBox.setStyleSheet(STYLE_DISC_PARAM_BOXES)
        self.parameterBox.setReadOnly(True)
        self.parameterBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.parameterBox.setFixedHeight(int(screen.height() * 0.30))
        self.parameterBox.setVisible(False)
        layout.addWidget(self.parameterBox)

        layout.addStretch()

        # Action bttns
        self.btnStart = QPushButton("RUN SIMULATION")
        self.btnStart.setStyleSheet(STYLE_RUN_BTN)
        self.btnStart.clicked.connect(self.handleRunClick)
        layout.addWidget(self.btnStart)

        self.btnReset = QPushButton("RESET ANIMATION")
        self.btnReset.setStyleSheet(STYLE_RESET_BTN)
        self.btnReset.clicked.connect(self.handleResetClick)
        layout.addWidget(self.btnReset)

    def createRadioGroup(self, parentLayout, labelText, optionsList):
        # outer container wraps label and buttons
        outerContainer = QWidget()
        outerContainer.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_PORCELAIN};
                border-radius: 6px;
            }}
        """)
        outerLayout = QVBoxLayout()
        outerLayout.setContentsMargins(8, 6, 8, 6)
        outerLayout.setSpacing(4)
        outerContainer.setLayout(outerLayout)

        # label is now inside the container
        label = QLabel(labelText)
        label.setStyleSheet(STYLE_CONFIG_LABELS + "border: none; background-color: transparent;")
        outerLayout.addWidget(label)

        # radio buttons
        group = QButtonGroup(self)
        hLayout = QHBoxLayout()
        hLayout.setSpacing(15)
        hLayout.setContentsMargins(0, 0, 0, 0)

        for idx, text in enumerate(optionsList):
            rb = QRadioButton(text)
            rb.setStyleSheet(STYLE_RADIO_BTN)
            if idx == 0:
                rb.setChecked(True)
            group.addButton(rb, idx)
            hLayout.addWidget(rb)

        hLayout.addStretch()
        outerLayout.addLayout(hLayout)

        parentLayout.addWidget(outerContainer)
        return group

    def setupMapArea(self, parentWidget):
        # RHS Map area builder (func)
        layout = QVBoxLayout()
        parentWidget.setLayout(layout)

        self.infoBubb = QLabel("Status: Idle | Adjust Settings & Click Map!") 
        self.infoBubb.setStyleSheet(STYLE_STATUS_BUBBLE)
        self.infoBubb.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.infoBubb)

        self.mapTab = QTabWidget()
        self.mapTab.setTabPosition(QTabWidget.South)
        
        self.viewTopo = QWebEngineView()
        self.initializeMap(self.viewTopo)
        self.mapTab.addTab(self.viewTopo, "Simulation Map") 

        self.viewZone = QWebEngineView()
        self.viewZone.setHtml("<h3>Lava Zone Map (Placeholder)</h3>")  # Not yet implemented but kept the tab
        self.mapTab.addTab(self.viewZone, "Lava Zone Map")
        
        layout.addWidget(self.mapTab)

    def initializeMap(self, webView):
        # QWebEngine without the HTML string injection --> I just found it hard to work with :( 
        self.channel = QWebChannel()
        self.bridge = MapBridge(self)
        self.channel.registerObject("bridge", self.bridge )
        webView.page().setWebChannel(self.channel)

        # Injects QWebChannel via Script obj <--> uses QFile to read
        scriptChannel = QWebEngineScript()
        fileQwc = QFile(":/qtwebchannel/qwebchannel.js")
        
        if fileQwc.open(QIODevice.ReadOnly):
            qwcContent = bytes(fileQwc.readAll()).decode('utf-8')
            scriptChannel.setSourceCode(qwcContent)
            fileQwc.close()
            
            scriptChannel.setInjectionPoint(QWebEngineScript.DocumentCreation)
            scriptChannel.setWorldId(QWebEngineScript.MainWorld)
            webView.page().scripts().insert(scriptChannel)
        else:
            print("QWebChannel Internal Resource Missing") # Should hopefully not happen agian

        # Custom JS bridge injecttion (from file)
        try:
            if os.path.exists(JS_BRIDGE_PATH):
                with open(JS_BRIDGE_PATH, "r", encoding="utf-8") as fileObj:
                    bridgeContent = fileObj.read()
                
                scriptBridge = QWebEngineScript()
                scriptBridge.setSourceCode(bridgeContent)
                scriptBridge.setInjectionPoint(QWebEngineScript.DocumentCreation)
                scriptBridge.setWorldId(QWebEngineScript.MainWorld)
                webView.page().scripts().insert(scriptBridge )
            else:
                print(f"JS Bridge not found at: {JS_BRIDGE_PATH }")
                self.infoBubb.setText("JS Bridge File Missing") # In case

        except Exception as error:
            print(f"Script Injection Failed: {error}") # Fallback just in case again

        #Pure HTML load 
        try:
            mapData = create_big_island_map()
            tempDir = tempfile.mkdtemp()
            self.tempFiles.append(tempDir)
            
            htmlPath = os.path.join(tempDir, "index.html")
            
            # Avoids the issue with the special characters like ō and such in hawaiian words by using utf 8
            with open(htmlPath, "w", encoding="utf-8") as fileObj:
                fileObj.write(mapData.getvalue().decode('utf-8'))

            webView.load(QUrl.fromLocalFile(os.path.abspath(htmlPath)))

        except Exception as error:
            print(f"Map Load Error: {error}")

    def handleRunClick(self):
        # Run/Pause (function)
        if not self.closestVent:
            self.infoBubb.setText("Please click a location on the map first. ")
            return

        if self.isDataPlaying:
            self.pauseSimulation()
        else:
            self.runSimulation()

    def handleResetClick(self):
        # Stop/Reset Sim
        try:
            self.isDataPlaying = False
            self.closestVent = None
            self.currentCoords = None
            
            self.updateButtonState(isPlaying=False)
            self.infoBubb.setText("Status: Reset | Click map to start new simulation")
            
            print("\nSTATE RESET") 
            
            jsCommand = "window.removeVideoOverlay();"
            self.viewTopo.page().runJavaScript(jsCommand)
            
        except Exception as error:
            print(f"Reset error: {error}")

    def updateButtonState(self, isPlaying):
        # Update button (text/clr)
        if isPlaying:
            self.btnStart.setText("PAUSE SIMULATION")
            self.btnStart.setStyleSheet(STYLE_PAUSE_BTN)
        else:
            self.btnStart.setText("RUN / RESUME")
            self.btnStart.setStyleSheet(STYLE_RUN_BTN)

    def runSimulation(self):
        # Video playback strt
        try:
            self.isDataPlaying = True
            self.updateButtonState(isPlaying=True)

            # Parameters to make backend setup easier  
            viscosity = "low" if self.groupVisc.checkedId() == 0 else "high"
            
            ventId = self.groupVent.checkedId()
            if ventId == 0:
                ventSize = "small"
            elif ventId == 1:
                ventSize = "medium"
            else:
                ventSize = "large"

            effId = self.groupEff.checkedId()
            if effId == 0:
                rate = "low"
            elif effId == 1:
                rate = "medium"
            else:
                rate = "high"

            # Debug output for backend :) 
            print("\nSIMULATION PARAMETERS")
            print(f"Viscosity:     {viscosity}")
            print(f"Vent Size:     {ventSize}")
            print(f"Effusion Rate: {rate}")
            print(f"Location:      {self.closestVent}")
            print("---------------------------------------\n")

            videoFile = self.getVideoFile(viscosity, ventSize, rate )
            videoPath = os.path.join(VIDEO_DIR_PATH, videoFile)

            if not os.path.exists(videoPath):
                self.infoBubb.setText(f"Error: {videoFile} not found.")
                return

            videoUrl = QUrl.fromLocalFile(videoPath).toString()
            lat = self.closestVent[0]
            lon = self.closestVent[1]
            
            jsCommand = f"window.playVideoOverlay({lat}, {lon}, '{videoUrl}');"
            self.viewTopo.page().runJavaScript(jsCommand)
            
            self.infoBubb.setText(f"Simulating: {videoFile}")

        except Exception as error:
            print(f"Run sim error: {error}")

    def pauseSimulation(self):
        # Pause video funct
        try:
            self.isDataPlaying = False
            self.updateButtonState(isPlaying= False)
            
            jsCommand = "window.pauseVideoOverlay();"
            self.viewTopo.page().runJavaScript(jsCommand)
            
            self.infoBubb.setText("Simulation Paused")
            print("SIMULATION PAUSED")
            
        except Exception as error:
            print(f"Pause error: {error}")

    # Video File Mapping --> When  the backend is linked, this is where the simulations will be mapped
    def getVideoFile(self, viscosity, ventSize, rate):
        # Map inputs to filename
        paramKey = (viscosity, ventSize, rate)
        
        # Fallback: all point to mlv5_3 
        # until specific files are added for medium/high rates
        videoMap = {
            # Low Viscosity
            ("low", "small", "low"): "mlv5_3.webm",
            ("low", "small", "medium"): "mlv5_3.webm",
            ("low", "small", "high"): "mlv5_3.webm",
            
            ("low", "medium", "low"): "mlv5_3.webm",
            ("low", "medium", "medium"): "mlv5_3.webm",
            ("low", "medium", "high"): "mlv5_3.webm",

            ("low", "large", "low"): "mlv5_3.webm",
            ("low", "large", "medium"): "mlv5_3.webm",
            ("low", "large", "high"): "mlv5_3.webm",

            # High Viscosity
            ("high", "small", "low"): "mlv5_3.webm",
            ("high", "small", "medium"): "mlv5_3.webm",
            ("high", "small", "high"): "mlv5_3.webm",

            ("high", "medium", "low"): "mlv5_3.webm",
            ("high", "medium", "medium"): "mlv5_3.webm",
            ("high", "medium", "high"): "mlv5_3.webm",

            ("high", "large", "low"): "mlv5_3.webm",
            ("high", "large", "medium"): "mlv5_3.webm",
            ("high", "large", "high"): "mlv5_3.webm" ,
        }
        # Explicit file --> to prevents crash (once again, when backend is linked htis can all be changed)
        return videoMap.get(paramKey, "mlv5_3.webm")

    # disclaimer button toggle; close parameter if disclaimer open
    def toggleDisclaimerPanel(self, checked):
        self.disclaimerBox.setVisible(checked)
        self.btnDisclaimer.setText("▼  Disclaimer" if checked else "▶  Disclaimer")
        if checked:
                self.parameterBox.setVisible(False)
                self.btnParameter.setChecked(False)
                self.btnParameter.setText("▶  Parameters")

    # parameter button toggle; close disclaimer if parameter open
    def toggleParameterPanel(self, checked):
        self.parameterBox.setVisible(checked)
        self.btnParameter.setText("▼  Parameters" if checked else "▶  Parameters")
        if checked:
            self.disclaimerBox.setVisible(False)
            self.btnDisclaimer.setChecked(False)
            self.btnDisclaimer.setText("▶  Disclaimer")

    def addSeparator(self, layout):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine) 
        sep.setFrameShadow(QFrame.Sunken) 
        layout.addWidget(sep)

    def showInfo(self):
        QMessageBox.information(self, "About", "1) Click Map\n2) Run/Pause\n3) Reset to start over")

    def closeEvent(self, event):
        # Cleanup any tmp files 
        try:
            for path in self.tempFiles:
                if os.path.exists(path):
                    shutil.rmtree(path)
        except Exception:
            pass
        super().closeEvent(event)
