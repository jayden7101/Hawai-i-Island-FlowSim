# CS 460: Hawaii Island Lava Flow Simulation Project - Front End

An interactive application using PyQt5 for simulating lava flows on Hawaii's Big Island. Users can click locations on an interactive map, configure simulation parameters (viscosity, vent size, effusion rate), and view animated simulations.

## Features

- Interactive map interface
- Parameter configuration for viscosity, vent size, and effusion rate
- Video based flow animations
- Real time simulation control (run, pause, reset)

## Requirements

- Python 3.x
- PyQt5

Install dependencies:
```
pip install -r requirements.txt
```

## Running

From the project root:
```
python Hawai-i-Island-FlowSim/src/main_window.py
```

## Post Prototype Goals 

### Most Urgent

1) Support multiple vents via arrays/JSON configuration, ensuring correct video playback for each parameter combination. Consider dynamic implementation if feasible.
2) Offline capabilities for map and video assets.
3) Package as a standalone executable that launches with a double click.

### Important

4) Support multiple map overlays on the base map.
5. Information button displaying flow details, with descriptions stored in animation JSON files.

### Bonus if possible

6) Dynamic array/configuration system for easier addition of new vents and animations.


CREDITS:
HVO: Lava Zone Map overlay layer
HVERI: Hawaii Island DEM
A-Lurker, BrandonXiang, Raruto: Leaflet KMZ Plugin: https://github.com/Raruto/leaflet-kmz
Volodymyr Agafonkin, originally: Leaflet https://leafletjs.com/, https://github.com/Leaflet/Leaflet
Delage, E., & Kelfoun, K. (2020). VolcFlow-C. Observatoire de Physique du Globe de Clermont-Ferrand (OPGC). https://doi.org/10.25519/VOLCFLOW-C
Kelfoun, K. (2023). VolcFlow. LMV, OPGC. https://doi.org/10.25519/VOLCFLOW

DOCUMENTATION:
PyQt5: https://doc.qt.io/archives/qtforpython-5/
PyQt5.QtCore: https://doc.qt.io/archives/qtforpython-5/PySide2/QtCore/index.html#module-PySide2.QtCore
PyQt5.QtWidgets: https://doc.qt.io/archives/qtforpython-5/PySide2/QtWidgets/index.html#module-PySide2.QtWidgets
PyQt5.QtWebChannel: https://doc.qt.io/archives/qtforpython-5/PySide2/QtWebChannel/index.html#module-PySide2.QtWebChannel
PyQt5.WebEngineWidgets: thon-5/PySide2/QtWebEngineWidgets/index.html#module-PySide2.QtWebEngineWidgets
PyQt5.QtGui: https://doc.qt.io/archives/qtforpython-5/PySide2/QtGui/index.html#module-PySide2.QtGui
