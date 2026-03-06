"""
this script has the haversine formula for finding the closest distances
"""

import os
import json
from math import radians, sin, cos, sqrt, atan2
from vent_locations import *

# directory for json files and the path to it
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
JSON_DIR = os.path.join(PROJECT_ROOT, "mlv_json")

"""
VENT SELECTION FUNCTIONS
"""
def haversine_distance(coord1, coord2):
    """Return the distance between two lat/lon pairs in kilometers."""
    R = 6371.0  # Earth radius (km)
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def find_closest_vent(user_coord):
    lat, lon = user_coord

    quadrant_selection = None
    for quadrant in QUADRANTS:
        b = quadrant["bounds"] # b for bounds
        if b["lat_min"] <= lat <= b["lat_max"] and b["lon_min"] <= lon <= b["lon_max"]:
            quadrant_selection = quadrant
            break
        
    # if a location is chosen that falls outside of the defined quadrants,
    # search through all vents
    if quadrant_selection is None: 
        all_vents = { key: vent for q in QUADRANTS for key, vent in q["vents"].items()}
        vent_search = all_vents
    else:
        vent_search = quadrant_selection["vents"]

    # run haversine against vents in found quadrant
    closest_vent = None
    min_dist = float("inf")
    for vname, vdata in vent_search.items():
        dist = haversine_distance(user_coord, vdata["coords"])
        if dist < min_dist:
            min_dist = dist
            closest_vent = vdata

    # this handles if the user clicks a point that is within a quadrant, but that quadrant
    # is empty; this is currently the case for quadrant 4, which is why this is needed.
    if closest_vent is None:
        all_vents = { key: vent for q in QUADRANTS for key, vent in q["vents"].items()}
        for vname, vdata in all_vents.items():
            dist = haversine_distance(user_coord, vdata["coords"])
            if dist < min_dist:
                min_dist = dist
                closest_vent = vdata
    return closest_vent["coords"], round(min_dist, 3), closest_vent["json"]

"""
ANIMATION PLAYING FUNCTIONS:
"""
def load_vent_animations(ventFile):
    path = os.path.join(JSON_DIR, ventFile)
    print(f"DEBUG: trying to open {path}")        # check if can open
    print(f"DEBUG: file exists: {os.path.exists(path)}")  # check if file exists
    try:
        with open(path, "r", encoding = "utf-8") as f:
            data = json.load(f)
        return data.get("animations", {})
    except Exception as e:
        print(f"Could not load {path}: {e}")
    return {}

# maps configurations to their number based on the toggles
# viscosity, vent size, effusion rate
ANIMATION_CONFIG_MAP = {
    ("low", "small", "low"): 1,
    ("low", "large", "low"): 2,
    ("low", "large", "high"): 3,
    ("low", "small", "high"): 4,
    ("high", "small", "low"): 5,
    ("high", "small", "high"): 6,   
    ("high", "large", "low"): 7,
    ("high", "large", "high"): 8,
}

# set a default if there's no configuration for a certain selection
DEFAULT_ANIMATION_CONFIG = 1

"""
build animation key for a vent + config selection
"""
def get_animation_key(ventFile, viscosity, ventSize, effusion):
    base_name = os.path.splitext(ventFile)[0]

    combo = (viscosity, ventSize, effusion)
    anim_num = ANIMATION_CONFIG_MAP.get(combo, DEFAULT_ANIMATION_CONFIG)

    return f"{base_name}_{anim_num}"

def get_animation_data(ventFile, viscosity, ventSize, effusion):
    animations = load_vent_animations(ventFile)
    if not animations:
        return None, None

    key = get_animation_key(ventFile, viscosity, ventSize, effusion)

    if key not in animations:
        print(f"Warning: '{key}' not found in {ventFile}. Using first available.")
        key = next(iter(animations))

    return key, animations[key]
