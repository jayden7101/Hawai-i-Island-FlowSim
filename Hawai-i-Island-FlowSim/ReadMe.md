# Lava Flow UI

This repository contains the user interface for the lava flow simulation project.

## Current State
- PyQt UI with control panel and map display
- Sliders for viscosity, vent size, and effusion rate
- Interactive map using OpenStreetMap and CartoDB
- Status and settings feedback in the UI

The UI currently relies on web map tiles and is not connected to the backend simulation logic.

## Next Steps for UI
- Replace web tiles with offline map data
- Export QGIS data to GeoJSON or similar format
- Connect UI controls to backend lava flow simulations
- Trigger animations based on selected vent locations