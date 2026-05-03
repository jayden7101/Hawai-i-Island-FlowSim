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
JSON_DIR = os.path.join(PROJECT_ROOT, "vent_json")

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

"""
this function is for searching for the closest vent to the point selected by the user.
the map is broken up into 4 quadrants, where each quadrant has a .1 degree overlap in
the event if a user chooses a location in quadrant x, if the nearest vent to that click
is actually in quadrant y, it will be able to find that in the overlap.

if no quadrant is found (if a user clicks outside available quadrants), all vents will be
searched. if the selection falls into an area that has no available vents, all vents will
be be searched. 

while the min/max latitudes currently encompass the entire area covered by the map in the ui,
the function will still look at min/max latitude in the event that more quadrants are added
in the vent_locations.py script (which would be done through editing current quadrants and
adding new ones).

theoretically, you should not need to adjust this code after adding new quadrants. 
"""
def find_closest_vent(user_coord):
    lat, lon = user_coord
    print(f"\nDEBUGGING: find_closest vent function. searching for {lat:.4f}, {lon:.4f}")

    matching_quadrants = [] # to track quadrants a vent is in
    for i, quadrant in enumerate(QUADRANTS):
        b = quadrant["bounds"]
        print(f"DEBUG: check quadrant {i + 1}: lon {b['lon_min']} to {b['lon_max']}")
        if b["lat_min"] <= lat <= b["lat_max"] and b["lon_min"] <= lon <= b["lon_max"]:
            print(f"DEBUG: quadrant{i + 1} is matched")
            matching_quadrants.append(quadrant)
        else:
            print(f"DEBUG: quadrant {i + 1} no match.")

    if matching_quadrants:
        print(f"DEBUG: {len(matching_quadrants)} quadrants matched. continuing search.")
        vent_search = {key: vent for q in matching_quadrants for key, vent in q["vents"].items()}
    else:
        print(f"DEBUG: no quadrants matched, searching all vents")
        vent_search = {key: vent for q in QUADRANTS for key, vent in q["vents"].items()}
    print(f"DEBUG: searching {len(vent_search)} vents: {list(vent_search.keys())}")

    closest_vent = None
    min_dist = float("inf")
    for vname, vdata in vent_search.items():
        dist= haversine_distance(user_coord, vdata["coords"])
        if dist < min_dist:
            min_dist = dist
            closest_vent = vdata

    # if no vents in quadrant(s) are found, search all vents.
    if closest_vent is None:
        print(f"DEBUG: no matched vents; resorting to searching all vents")
        all_vents = {key: vent for q in QUADRANTS for key, vent in q["vents"].items()}
        for vname, vdata in all_vents.items():
            dist = haversine_distance(user_coord, vdata["coords"])
            if dist < min_dist:
                min_dist = dist
                closest_vent = vdata
        print(f"DEBUG: all vent search result: {closest_vent['json']} at {round(min_dist, 3)} km")

    print(f"DEBUG: results are {closest_vent['json']} at {round(min_dist, 3)} km")
    return closest_vent["coords"], round(min_dist, 3), closest_vent["json"]        

"""
ANIMATION PLAYING FUNCTIONS:
load_vent_animations: get all animations for the vent's json file
get_animation_key: build specific key based on vent number and lava configuration
get_animation_data: 
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

"""
build animation key for a vent + config selection
viscosity, ventSize and effusion are passed here, but defined in lava_gui
get_animation_key builds an identifier for a unique vent and configuration.
"""
def get_animation_key(ventFile, viscosity, ventSize, effusion):
    base_name = os.path.splitext(ventFile)[0] # removes the file extension

    combo = (viscosity, ventSize, effusion) # store the value from the config map
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




