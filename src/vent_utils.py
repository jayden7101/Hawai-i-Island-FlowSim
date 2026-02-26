"""
this script has the haversine formula for finding the closest distances
"""

import os
import json
from math import radians, sin, cos, sqrt, atan2
from vent_locations import vent_lat_lon, vent_jsons

# directory for json files and the path to it
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
JSON_DIR = os.path.join(PROJECT_ROOT, "mlv_json")

"""
HAVERSINE FORMULA
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

"""
FIND CLOSEST VENT:
this function returns the closest vent to the users chosen coordinate
returns:
closest_cord: lat + lon of the closest vent
distance_kim: distance in km
closest_index: index into vent_lat_lon and vent_jsons
ventFile: matching json filename
"""
def find_closest_vent(user_coord):
    """Return the closest vent (dict) to the given [lat, lon]."""
    closest_coord = None
    closest_index = None 
    min_distance = float('inf')

    for idx, vent_coord in enumerate(vent_lat_lon):
        dist = haversine_distance(user_coord, vent_coord)
        if dist < min_distance:
            min_distance = dist
            closest_coord = vent_coord
            closest_index = idx

            ventFile = vent_jsons[closest_index] if closest_index is not None else None

    return closest_coord, round(min_distance, 2), closest_index, ventFile


"""
ANIMATION LOADING:
this opens the json file for any given vent to return the animations directory that
is inside of it. 
"""
def load_vent_animations(ventFile):
    path = os.path.join(JSON_DIR, ventFile)
    print(f"DEBUG: trying to open {path}")        # add this
    print(f"DEBUG: file exists: {os.path.exists(path)}")  # add this
    try:
        with open(path, "r", encoding = "utf-8") as f:
            data = json.load(f)
        return data.get("animations", {})
    except Exception as e:
        print(f"Could not load {path}: {e}")
    return {}


"""
ANIMATION SELECTION
"""

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







    
