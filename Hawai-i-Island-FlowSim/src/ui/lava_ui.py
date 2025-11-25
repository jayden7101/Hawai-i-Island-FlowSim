'''
Holds the Lava Flow UI Class for options and map display. 
Code still needs to be connected with backend as it uses OpenStreetMap and CartoDB, not the QGIS data.

TODO: Need to export tfrom QGIS to some other format (like Geo JSON) and load that in for lava zone mapping prog does not work offline yet (relies on web tiles).
There has been talks about downloading once and using offline however that is still in the works.
'''

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QFrame, QSplitter, QTabWidget) 
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from map_creator import create_big_island_map 

class LavaFlowUI(QMainWindow):
    def __init__(self):
        super().__init__()  
        
        self.title = "Lava Flow Simulation"
        self.rateText = "Effusion Rate"
        self.viscText = "Viscosity (0 = Pahoehoe, 1 = 'A'a)" # From photo 
        self.ventText = "Vent Size (0 = Medium, 1 = Large)"  
    
        self.ventSize = 0 
        self.viscosity = 0 
        self.effRate = 50  # Default but can adjust as needed

        self.initUI() 

    def initUI(self):
        # Main Window
        self.setGeometry(100, 100, 1100, 700)
        self.setWindowTitle(self.title)
        windowSplit = QSplitter(Qt.Horizontal) 
        
        # Left side for Options
        leftPane = QWidget()
        leftPane.setStyleSheet("background-color: ##FFFDD0;") 
        self.setupControls(leftPane)
        
        # Right side of window for Maap
        rightPaneWidget = QWidget() 
        self.setupMapArea(rightPaneWidget) 

        windowSplit.addWidget(leftPane)
        windowSplit.addWidget(rightPaneWidget)
        windowSplit.setSizes([250, 790]) # L/R size ratio

        self.setCentralWidget(windowSplit)

    def setupControls(self, panel):
        # Sets up the LH control panel (slider && buttons)
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        hBox = QHBoxLayout() 
        self.btnInfo = QPushButton("i")
        self.btnInfo.setFixedSize(30, 35)
        self.btnInfo.setStyleSheet("border-radius: 14px; background-color: #ffcccb; font-weight: bold;") # Light red for lava project theme.
        self.btnInfo.clicked.connect(self.showInfo)
        
        hBox.addWidget(self.btnInfo)
        hBox.addStretch() 
        layout.addLayout(hBox)
        self.addSeparator(layout)

        self.sliderVisc = self.createSlider(layout, self.viscText, 0, 1, 0) # Viscosity toggle
        self.addSeparator(layout)

        self.sliderVent = self.createSlider(layout, self.ventText, 0, 1, 0) # Vent size
        self.addSeparator(layout)

        self.sliderRate = self.createSlider(layout, self.rateText, 0, 100, 50) # Effusion rate
        layout.addStretch()

        self.btnStart = QPushButton("RUN SIMULATION")
        
        # Can update color to better match theme --> sticking with red for now
        self.btnStart.setStyleSheet("background-color: #ffcccb; font-weight: bold; padding: 12px;") 
        self.btnStart.clicked.connect(self.runSimulation)
        
        layout.addWidget(self.btnStart)

    def createSlider(self, layout, labelText, minVal, maxVal, defValue):
        currentLabel = QLabel(labelText)
        currentLabel.setStyleSheet("font-weight: bold; font-size: 16px;") 
        layout.addWidget(currentLabel)
        
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minVal)
        slider.setMaximum(maxVal) 
        slider.setValue(defValue)  
        
        slider.setTickInterval(1)
        slider.valueChanged.connect(self.updateState)
        
        layout.addWidget(slider)
        return slider

    def setupMapArea(self, parentWidget):
        layout = QVBoxLayout()
        parentWidget.setLayout(layout)

        self.infoBubb = QLabel("Status: Idle | Adjust Sliders & Click Run!") 
        self.infoBubb.setStyleSheet("background-color: #FFDBBB; padding: 10px; border-radius: 5px;")
        self.infoBubb.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.infoBubb)

        self.mapTab = QTabWidget()
        self.mapTab.setTabPosition(QTabWidget.South) 
        
        self.viewTopo = QWebEngineView()
        self.renderMap(self.viewTopo, "OpenStreetMap") 
        self.mapTab.addTab(self.viewTopo, "Standard Map") 

        self.viewZone = QWebEngineView()
        self.renderMap(self.viewZone, "CartoDB positron") # CartoDB can be replaced with darker theme if needed
        self.mapTab.addTab(self.viewZone, "Lava Zone Map")
        
        layout.addWidget(self.mapTab)

    def renderMap(self, webView, tileType):
        mapData = create_big_island_map(tileType) 
        webView.setHtml(mapData.getvalue().decode()) 

    def updateState(self):
        self.viscosity = self.sliderVisc.value()
        self.ventSize = self.sliderVent.value()
        self.effRate = self.sliderRate.value()
        self.showInfo()

    def showInfo(self):
        viscStr = "Pahoehoe" if self.viscosity == 0 else "'A'a"
        ventSizeStr = "Medium" if self.ventSize == 0 else "Large"
        rateStr = str(self.effRate)
        statusText = f"Settings -> Viscosity: {viscStr} | Vent: {ventSizeStr} | Rate: {rateStr}"
        
        self.infoBubb.setText(statusText)

    def runSimulation(self):
        print("RUNNING SIMULATION WITH:")
        print("Visc:", self.viscosity, "Vent:", self.ventSize, "Rate:", self.effRate)
        
        self.infoBubb.setText("RUNNING LAVA SIMULATION....") #Not yet implemented

    def addSeparator(self, layout):
        seperator = QFrame()
        seperator.setFrameShape(QFrame.HLine) 
        seperator.setFrameShadow(QFrame.Sunken) 
        layout.addWidget(seperator)