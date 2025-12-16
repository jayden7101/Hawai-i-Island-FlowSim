# CS 460: Hawaii Island Lava Flow Simulation Project

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

## TODO: 
1) Review the README and add on to the Post Prototype goals
2) Backend update the README as needed --> mainly focuses on the front end 