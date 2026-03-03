import os

# this script is solely for layers so you do not need to edit the gui script
# to add layers

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYERS_DIR_PATH = os.path.join(PROJECT_ROOT, "overlayers")

OVERLAY_LAYERS = [
    ("Steepest Descent, 3m", "hi_steepest_descent_3m.kmz"),
    ("Steepest Descent, 750k", "hi_steepest_descent_750k.kmz"),
    ("Post 2018 County Roads", "hi_county_roads_post2018.kmz"),
    ("Mauna Loa Rift Zone", "ml_rift.kmz"),
    ("Kilauea Rift Zone", "k_rift.kmz"),
    ("Mauna Loa Trisdell Outlines", "ml_trisdell_outline.kmz"),
    ("Mauna Loa Lava Flows", "ml_750yr_lava.kmz")
]

