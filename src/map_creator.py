# map_creator.py
import folium
import io
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
KMZ_PLUGIN_PATH = os.path.join(PROJECT_ROOT, "js", "leaflet-kmz.js")
MAP_HELPERS_PATH = os.path.join(PROJECT_ROOT, "js", "map_helpers.js")

# def create_big_island_map(kmz_plugin_path):
def create_big_island_map():
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
    center_coords = [19.6, -155.5]

    # Create map
    folium_map = folium.Map(
        location=center_coords,
        zoom_start=9,
        min_zoom=9,
        max_zoom=14,
        max_bounds=True,
        tiles = None
    )

    # Restrict zooming and panning to Big Island
    folium_map.fit_bounds(bounds)
    folium_map.options["maxBounds"] = bounds
    folium_map.options["maxBoundsViscosity"] = 1.0

    # Add a preset marker at the center
    folium.Marker(center_coords, tooltip="Big Island").add_to(folium_map)

    folium.TileLayer(
        tiles = "OpenStreetMap",
        name = "Street Map",
        control = True
    ).add_to(folium_map)
    
    # satellite tile layer ( from Esri World Imagery)
    folium.TileLayer (
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr = "Esri, Maxar, Earthstar Geographics, and the GIS User Community",
        name = "Satellite",
        overlay = False,
        control = True
    ).add_to(folium_map)

    folium.LayerControl(position = "bottomleft", collapsed = False).add_to(folium_map)

    #inject leaflet-kmz plugin for overlay usage (rift zone etc)
    with open(KMZ_PLUGIN_PATH, "r", encoding = "utf-8") as f:
        kmz_plugin_js = f.read()

    folium_map.get_root().html.add_child(folium.Element(
        f'<script>{kmz_plugin_js}</script>'
    ))

    # inject map_helpers plugin for auto-zooming to vent
    with open(MAP_HELPERS_PATH, "r", encoding="utf-8") as f:
        map_helpers_js = f.read()

    folium_map.get_root().html.add_child(folium.Element(
        f"<script>{map_helpers_js}</script>"
    ))

    map_name = folium_map.get_name()

    map_name = folium_map.get_name()

    folium_map.get_root().script.add_child(folium.Element(
        f"""
        setTimeout(function() {{
            window.appMap = {map_name};
            console.log("appMap assigned", !!window.appMap);
        }}, 0);
        """
    ))

    # Save map to bytes
    map_bytes = io.BytesIO()
    folium_map.save(map_bytes, close_file=False)
    return map_bytes




