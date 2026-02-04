from math import radians, sin, cos, sqrt, atan2
from vent_locations import vent_lat_lon, vent_jsons

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
    closest_coord = None
    closest_index = None 
    min_distance = float('inf')

    for idx, vent_coord in enumerate(vent_lat_lon):
        dist = haversine_distance(user_coord, vent_coord)
        if dist < min_distance:
            min_distance = dist
            closest_coord = vent_coord
            closest_index = idx

            vent_file = vent_jsons[closest_index] if closest_index is not None else None

    return closest_coord, round(min_distance, 2), closest_index, vent_file
