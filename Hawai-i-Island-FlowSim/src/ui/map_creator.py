import folium
import io
from vent_locations import vent_locations

def create_big_island_map(tileType="OpenStreetMap"):
    """
    Creates a Folium map of the Big Island with preset center marker,
    restricted zoom and pan to the island bounds.
    Returns: BytesIO object containing HTML map.
    """
    # Approximate bounding box for Big Island (lat/lon)
    bounds = [
        [18.843106754876224, -156.53445457674312],  # SW corner
        [20.456472808815583, -154.5696457697364]    # NE corner
    ]

    # Center coordinates for Big Island
    centerCoords = [19.6, -155.5]

    # Create map
    foliumMap = folium.Map(
        location=centerCoords,
        zoom_start=9,
        min_zoom=9,
        max_zoom=14,
        max_bounds=True,
        tiles=tileType # Arg passed from UI
    )

    # Restrict panning to Big Island
    foliumMap.fit_bounds(bounds)
    foliumMap.options['maxBounds'] = bounds

    # Add a preset marker at the center
    folium.Marker(centerCoords, tooltip="Big Island").add_to(foliumMap)

    # Loop through vent locations
    for currentVent in vent_locations:
        (ventLat, ventLon) = currentVent["coords"]
        ventName = currentVent["name"]

        folium.Marker(
            location=(ventLat, ventLon),
            tooltip=ventName,
            popup=ventName,
            icon=folium.Icon(color='red')
        ).add_to(foliumMap)

    # Save map to bytes
    mapBytes = io.BytesIO()
    foliumMap.save(mapBytes, close_file=False)
    return mapBytes