import sys
import os
import shutil
import tempfile

from PyQt5.QtCore import QUrl, QObject, pyqtSlot, Qt, QFile, QIODevice
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFormLayout, QLabel, QPushButton, QRadioButton, QButtonGroup,
    QSplitter, QFrame, QMessageBox, QTabWidget,QTextEdit, QScrollArea,
    QDialog, QVBoxLayout, QTextEdit, QSizePolicy, QListWidget, QListWidgetItem,
    QAbstractItemView)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtGui import QFontInfo

from map_creator import create_big_island_map

# supplementary script imports
from vent_utils import *
from text_descriptions import *
from overlay_config import *
from scrubber import Scrubber

# theme-related imports
from themes import get_theme, get_theme_button_icon
from theme_manager import apply_theme

# Configuration/Consts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Paths for assets
ICON_PATH = os.path.join(PROJECT_ROOT, "images", "volcano_icon.ico")
JS_BRIDGE_PATH = os.path.join(PROJECT_ROOT, "js", "map_bridge.js")
VIDEO_DIR_PATH = os.path.join(PROJECT_ROOT, "animation_videos")
#KMZ plugin used for displaying kmz,kml files directly as overlays
KMZ_PLUGIN_PATH = os.path.join(PROJECT_ROOT, "js", "leaflet-kmz.js")
LAYERS_DIR_PATH = os.path.join(PROJECT_ROOT, "overlayers")

WINDOW_TITLE = "Lava Flow Simulation"

"""
MAP BRIDGE AND PYTHON LINK
"""
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
            ventFile = ventData[2] 
            
            self.parentWindow.closestVent = closestVent
            self.parentWindow.closestVentFile = ventFile
            
            statusText = f"Selected: {lat:.4f}, {lon:.4f} | Ready to Run"
            self.parentWindow.infoBubb.setText(statusText)
            
            # Reset state when new click
            self.parentWindow.isDataPlaying = False
            self.parentWindow.updateButtonState(isPlaying=False)

        except Exception as error:
            print(f"Bridge error: {error}") # In case

"""
GUI CLASS: the main window
"""
class LavaGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        # Init window
        self.setWindowTitle(WINDOW_TITLE)
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.85), int(screen.height() * 0.85))
        self.currentThemeName = "light"
        self.currentTheme = get_theme(self.currentThemeName)
        
        try:
            if os.path.exists(ICON_PATH):
                self.setWindowIcon(QIcon(ICON_PATH))
        except Exception:
            pass

        # State
        self.closestVent = None
        self.closestVentFile = None
        self.currentCoords = None
        self.tempFiles = list()
        self.isDataPlaying = False
        self.currentAnimKey = None # for tracking current animation 

        # track active layers
        self.activeOverlays = {}

        # Splitter 
        windowSplit = QSplitter(Qt.Horizontal)
        
        leftPane = QWidget()
        self.setupControls(leftPane)
        
        rightPaneWidget = QWidget()
        self.setupMapArea(rightPaneWidget)

        self.windowSplit = windowSplit
        self.leftPane = leftPane
        self.rightPaneWidget = rightPaneWidget
        
        windowSplit.addWidget(leftPane)
        windowSplit.addWidget(rightPaneWidget)
        windowSplit.setSizes([250, 790])
        windowSplit.setHandleWidth(6)

        self.setCentralWidget(windowSplit)
        self.btnTheme.setText(get_theme_button_icon(self.currentThemeName))
        self.applyTheme()

    # left pane controls
    def setupControls(self, panel):
        screen = QApplication.primaryScreen().availableGeometry()
        btn_width = int(screen.width()*.08)

        layout = QVBoxLayout()
        panel.setLayout(layout)
        hBox = QHBoxLayout()
        
        """
        the top row of the left pane includes the info button, disclaimer
        button, parameter button, documentation
        """
        # info button
        self.btnInfo = QPushButton("i")
        self.btnInfo.setFixedSize(30, 30)
        self.btnInfo.clicked.connect(self.showInfo)

        # disclaimer button
        self.btnDisclaimer = QPushButton("▶  Disclaimer")
        self.btnDisclaimer.setCheckable(True)
        self.btnDisclaimer.clicked.connect(self.toggleDisclaimerPanel)
        self.btnDisclaimer.setFixedWidth(btn_width)

        # theme toggle button 
        self.btnTheme = QPushButton()
        self.btnTheme.setFixedSize(30, 30)
        self.btnTheme.clicked.connect(self.toggleTheme)
        self.btnTheme.setToolTip("Toggle light and dark mode")

        # parameter button
        self.btnParameter = QPushButton("▶  Parameters") 
        self.btnParameter.setCheckable(True)
        self.btnParameter.clicked.connect(self.toggleParameterPanel)
        self.btnParameter.setFixedWidth(btn_width)

        # sources button
        self.btnSources = QPushButton ("d")
        self.btnSources.setFixedSize(30, 30)
        self.btnSources.clicked.connect(self.showSource)

        # add buttons to the pane
        hBox.addWidget(self.btnInfo)
        hBox.addWidget(self.btnDisclaimer)
        hBox.addWidget(self.btnParameter)
        hBox.addWidget(self.btnSources)
        hBox.addStretch()
        hBox.addWidget(self.btnTheme)
        
        layout.addLayout(hBox)
        self.addSeparator(layout)

        # configuration parameter radio buttons
        # visocisty
        self.groupVisc = self.createRadioGroup(layout, "Viscosity", ["Low \n(Pahoehoe)", "High \n('A'a)"])

        # vent size
        self.groupVent = self.createRadioGroup(layout, "Vent Size", ["Small", "Large"])

        # """"effusion rate""""
        self.groupEff = self.createRadioGroup(layout, "Effusion Rate", ["Low", "High"])
        self.addSeparator(layout)

        # text boxes for disclaimer and parameter boxes
        self.disclaimerBox = QTextEdit()
        self.disclaimerBox.setHtml(DISCLAIMER_TEXT)
        self.disclaimerBox.setReadOnly(True)
        self.disclaimerBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.disclaimerBox.setFixedHeight(int(screen.height() * 0.30))
        self.disclaimerBox.setVisible(False)
        layout.addWidget(self.disclaimerBox)

        self.parameterBox = QTextEdit()
        self.parameterBox.setHtml(PARAMETER_TEXT)
        self.parameterBox.setReadOnly(True)
        self.parameterBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.parameterBox.setFixedHeight(int(screen.height() * 0.30))
        self.parameterBox.setVisible(False)
        layout.addWidget(self.parameterBox)

        # overlays section
        self.overlayLabel = QLabel("Map Overlays")
        layout.addWidget(self.overlayLabel)


        # drop down box for the overlay selection - ol/Ol short for overlay
        ol_row = QHBoxLayout()
        ol_row.setSpacing(4)

        #dropdown toggle to open + close dropdown
        self.btnOlDropdown = QPushButton("Overlay Options ▶")

        self.btnOlDropdown.clicked.connect(self.toggleDropdown)
        ol_row.addWidget(self.btnOlDropdown)

        # clear all button
        self.btnClearOverlays = QPushButton( "Clear Overlays")
        self.btnClearOverlays.clicked.connect(self.clearAllOverlays)
        ol_row.addWidget(self.btnClearOverlays)

        ol_row.addStretch()
        layout.addLayout(ol_row)

        self.overlayList = QListWidget()
        self.overlayList.setSelectionMode(QAbstractItemView.NoSelection)
        self.overlayList.setFocusPolicy(Qt.NoFocus)
        self.overlayList.setVisible(False)
        self.overlayList.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.overlayItems = {}
        for label, ol_filename in OVERLAY_LAYERS:
            ol_item = QListWidgetItem(self.formatOverlayText(label, False))
            ol_item.setData(Qt.UserRole, ol_filename)
            ol_item.setData(Qt.UserRole+1, label)
            self.overlayList.addItem(ol_item)
            self.overlayItems[ol_filename] = ol_item

        self.overlayList.itemClicked.connect(self.handleOlClick)
        layout.addWidget(self.overlayList)

        layout.addStretch()
        self.addSeparator(layout)

        # scrubber widget
        self.scrubber = Scrubber(self.currentTheme)
        layout.addWidget(self.scrubber)

        # Action bttns: run/reset
        self.btnStart = QPushButton("RUN SIMULATION")
        self.btnStart.clicked.connect(self.handleRunClick)
        layout.addWidget(self.btnStart)

        self.btnReset = QPushButton("RESET ANIMATION")
        self.btnReset.clicked.connect(self.handleResetClick)
        layout.addWidget(self.btnReset)

    """
    CREATE RADIO GROUP
    """
    def createRadioGroup(self, parentLayout, labelText, optionsList):
        if not hasattr(self, "themeRadioContainers"):
            self.themeRadioContainers = []
        if not hasattr(self, "themeRadioLabels"):
            self.themeRadioLabels = []
        if not hasattr(self, "themeRadioButtons"):
            self.themeRadioButtons = []
            
        # outer container wraps label and buttons
        outerContainer = QWidget()
        outerLayout = QVBoxLayout()
        outerLayout.setContentsMargins(8, 6, 8, 6)
        outerLayout.setSpacing(4)
        outerContainer.setLayout(outerLayout)

        # label is now inside the container
        label = QLabel(labelText)
        outerLayout.addWidget(label)
        self.themeRadioLabels.append(label)
        self.themeRadioContainers.append(outerContainer)

        # radio buttons
        group = QButtonGroup(self)
        hLayout = QHBoxLayout()
        hLayout.setSpacing(15)
        hLayout.setContentsMargins(0, 0, 0, 0)

        for idx, text in enumerate(optionsList):
            rb = QRadioButton(text)
            if idx == 0:
                rb.setChecked(True)
            group.addButton(rb, idx)
            hLayout.addWidget(rb)
            self.themeRadioButtons.append(rb)

        hLayout.addStretch()
        outerLayout.addLayout(hLayout)

        parentLayout.addWidget(outerContainer)
        return group

    """
    SETUP THE MAP AREA
    """
    def setupMapArea(self, parentWidget):
        # RHS Map area builder (func)
        layout = QVBoxLayout()
        parentWidget.setLayout(layout)

        self.infoBubb = QLabel("Status: Idle | Adjust Settings & Click Map!") 
        self.infoBubb.setAlignment(Qt.AlignCenter)
        self.infoBubb.setFixedHeight(36) # ensure top bubble doesnt get too big
        self.infoBubb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(self.infoBubb)
        
        self.viewTopo = QWebEngineView()
        self.initializeMap(self.viewTopo)
        layout.addWidget(self.viewTopo)
        self.scrubber.setPage(self.viewTopo.page())


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
            self.closestVentFile = None 
            self.currentCoords = None
            
            self.updateButtonState(isPlaying=False)
            self.infoBubb.setText("Status: Reset | Click map to start new simulation")
            
            print("\nSTATE RESET") 
            
            jsCommand = "window.removeVideoOverlay();"
            self.viewTopo.page().runJavaScript(jsCommand)
            self.scrubber.simulationReset()
            
        except Exception as error:
            print(f"Reset error: {error}")

    def updateButtonState(self, isPlaying):
        if isPlaying:
            self.btnStart.setText("PAUSE SIMULATION")
        else:
            self.btnStart.setText("RUN / RESUME")
    
    def runSimulation(self):
        # Video playback strt
        try:

            """
            Parameters to make backend setup easier
            removed melvin's original ventSize and effusion to account for
            only two choices for vent size and effusion rate
            """
            viscosity = "low" if self.groupVisc.checkedId() == 0 else "high"
            ventSize = "small" if self.groupVent.checkedId() == 0 else "large"
            effusion = "low" if self.groupEff.checkedId() == 0 else "high"

            animKey, animData = get_animation_data(
                self.closestVentFile, viscosity, ventSize, effusion)

            if animData is None:
                self.infoBubb.setText("Error: could not load animation data.")
                return

            # checking for if vid config is the same since last run
            changedAnimConfig = (animKey != self.currentAnimKey)

            # if no changes, resume existing video

            if not changedAnimConfig and self.currentAnimKey is not None:
                self.isDataPlaying = True
                self.updateButtonState(isPlaying = True)
                jsCommand = "window.playVideoOverlay();"
                self.viewTopo.page().runJavaScript(jsCommand)
                self.scrubber.simulationStarted()
                infoText = animData.get("information", animKey)
                self.infoBubb.setText(f"{animKey}: {infoText}")
                return

            # new configuration or first run -- validate theres a video before
            # changing the state of the button
            videoPath = os.path.join(VIDEO_DIR_PATH, animData["video_file"])
            if not os.path.exists(videoPath):
                self.infoBubb.setText(f"Error: {videoPath} not found.")
                return

            # new configuration/first run, load fresh
            self.currentAnimKey = animKey
            self.isDataPlaying = True
            self.updateButtonState(isPlaying = True)

            # Debug output for backend :) 
            print("\nSIMULATION PARAMETERS")
            print(f"Viscosity:     {viscosity}")
            print(f"Vent Size:     {ventSize}")
            print(f"Effusion Rate: {effusion}")
            print(f"Location:      {self.closestVent}")
            print("---------------------------------------\n")

            videoUrl = QUrl.fromLocalFile(videoPath).toString()
            bounds = animData["bounds"]
            swLat, swLon = bounds[0]
            neLat, neLon = bounds[1]
            
            # pass the coordinates of closest vent to JS 
            ventLat, ventLon = self.closestVent
            
            jsCommand = (
                f"window.playVideoOverlay("
                f"{swLat}, {swLon}, {neLat}, {neLon}, "
                f"{ventLat}, {ventLon}, "
                f"\"{videoUrl}\", true"
                f");"
            )
               
            self.viewTopo.page().runJavaScript(jsCommand)
            self.scrubber.simulationStarted()

            infoText = animData.get("information", animKey)
            self.infoBubb.setText(f"{animKey}: {infoText}")

        except Exception as error:
            print(f"Run sim error: {error}")

    def pauseSimulation(self):
        # Pause video funct
        try:
            self.isDataPlaying = False
            self.updateButtonState(isPlaying= False)
            
            jsCommand = "window.pauseVideoOverlay();"
            self.viewTopo.page().runJavaScript(jsCommand)
            self.scrubber.simulationPaused()
            
            self.infoBubb.setText("Simulation Paused")
            print("SIMULATION PAUSED")
            
        except Exception as error:
            print(f"Pause error: {error}")

    """
    Theme Functions      
    """
    def applyTheme(self):
        self.currentTheme = get_theme(self.currentThemeName)
        apply_theme(self, self.currentTheme)
        self.refreshOverlayIcons()
    
    def toggleTheme(self):
        if self.currentThemeName == "light":
            self.currentThemeName = "dark"
        else:
            self.currentThemeName = "light"

        self.btnTheme.setText(get_theme_button_icon(self.currentThemeName))
        self.applyTheme()


    """
    BUTTON FUNCTIONS
    """
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

    def showSource(self):
        QMessageBox.information(
            self,
            "Sources",
            SOURCES_TEXT,
            QMessageBox.Ok
        )

    """
    OVERLAY FUNCTIONS
    ol prefix indicates that this is something tied to the overlay
    functionality (files, etc)
    """
    def toggleDropdown(self):
        isVisible = self.overlayList.isVisible()
        self.overlayList.setVisible(not isVisible)
        self.btnOlDropdown.setText("▼  Overlay Options" if not isVisible else "▶  Overlay Options")

    def handleOlClick(self, ol_item):
        ol_filename = ol_item.data(Qt.UserRole)
        if ol_filename in self.activeOverlays:
            self.removeOverlay(ol_filename, ol_item)
        else:
            self.addOverlay(ol_filename, ol_item)

    def refreshOverlayIcons(self):
        for i in range(self.overlayList.count()):
            item = self.overlayList.item(i)
            ol_filename = item.data(Qt.UserRole)
            label = item.data(Qt.UserRole + 1)
            isActive = ol_filename in self.activeOverlays
            item.setText(self.formatOverlayText(label, isActive))

    def formatOverlayText(self, label, isActive):
        icon = self.currentTheme.OVERLAY_ON if isActive else self.currentTheme.OVERLAY_OFF
        return f" {icon} {label}"

    def addOverlay(self, ol_filename, ol_item):
        
        ol_layerPath = os.path.join(LAYERS_DIR_PATH, ol_filename)
        if not os.path.exists(ol_layerPath):
            self.infoBubb.setText(f"Layer file not found: {ol_filename}")
            return
        ol_layerUrl = QUrl.fromLocalFile(ol_layerPath).toString()
        jsCommand = f"window.loadKmzOverlay('{ol_filename}', '{ol_layerUrl}');"
        self.viewTopo.page().runJavaScript(jsCommand)
        self.activeOverlays[ol_filename] = ol_item   
        label = ol_item.data(Qt.UserRole + 1)
        ol_item.setText(self.formatOverlayText(label, True))
        print(f"Overlay ON: {ol_filename}")

    def removeOverlay(self, ol_filename, ol_item):
        jsCommand = f"window.removeKmzOverlay('{ol_filename}');"
        self.viewTopo.page().runJavaScript(jsCommand)
        self.activeOverlays.pop(ol_filename, None)
        label = ol_item.data(Qt.UserRole + 1)
        ol_item.setText(self.formatOverlayText(label, False))
        print(f"Overlay OFF: {ol_filename}")

    def clearAllOverlays(self):
        for ol_filename, ol_item in list(self.activeOverlays.items()):
            self.removeOverlay(ol_filename, ol_item)
        print("All overlays have been cleared.")
    
    # temp file cleaning
    def closeEvent(self, event):
        # Cleanup any tmp files 
        try:
            for path in self.tempFiles:
                if os.path.exists(path):
                    shutil.rmtree(path)
        except Exception:
            pass
        super().closeEvent(event)
