from math import radians, sin, cos, sqrt, atan2
from vent_locations import vent_locations

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
    """Return the closest vent (dict) to the given [lat, lon]."""
    closest = None
    min_distance = float('inf')

    for vent_coord in vent_locations:
        dist = haversine_distance(user_coord, vent_coord)
        if dist < min_distance:
            min_distance = dist
            closest = vent_coord

    return closest, round(min_distance, 2)
