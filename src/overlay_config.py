import os
"""
this script is solely to store the paths of the overlay layers. you do
not need to touch the gui script to add overlays.

to add overlays:
paste your kmz file into the overlayers folder.
edit this file with the overlay name you'd like displayed and the path:
("Overlay Display Name", "overlay_path.kmz")
you can insert this entry at the end, or in the middle.

the gui will automatically populate with the new overlay layer.
to remove an overlay, just delete the object from the file and erase its
entry in the OVERLAY_LAYERS list. 
"""

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYERS_DIR_PATH = os.path.join(PROJECT_ROOT, "overlayers")

OVERLAY_LAYERS = [
    ("Steepest Descent, 3m", "hi_steepest_descent_3m.kmz"),
    ("Steepest Descent, 750k", "hi_steepest_descent_750k.kmz"),
    ("Mauna Loa Rift Zone", "ml_rift.kmz"),
    ("Kilauea Rift Zone", "k_rift.kmz"),
    ("Mauna Loa Trisdell Outlines", "ml_trisdell_outline.kmz"),
    ("Lava Flow Hazard Zones", "HVO_LavaFlowHazardZones.kmz")   
]

