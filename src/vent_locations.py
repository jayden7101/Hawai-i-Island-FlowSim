"""
VENT LOCATION FILE:
currently, the island has been broken down into 4 quadrants based on longitude; while the current
implementation does not need this due to the number of vents, this can hopefully help improve
efficiency if enough vents are added that speed could be impacted.
to add a vent:
    "ventname/id": { "json": "jsonfilename.json", "coords": [latitude, longitude]}

the min/max latitude is the same for all quadrants and should encompass the entire latitude range
that was set in map_creation.py. 
in the event that there's a rogue click or something happens outside of the quadrants, there is
a method to handle that that will loop through all vents in the vents_util.py script.

the search through quadrants/vents is handled in such a way that you should be able to add new quadrants
as needed without needing to touch the vent_utils.py script. 
"""


QUADRANTS = [
     { # QUADRANT 1
        "bounds": {"lat_min": 18.8431, "lat_max": 20.4565, "lon_min": -156.073, "lon_max": -155.623},
        "vents": {
            "mlv12":  {"json": "mlv12.json",  "coords": [19.1681, -155.7365]},
            "mlv68": {"json": "mlv68.json", "coords": [19.1267, -155.7367]},
            "mlv2": {"json": "mlv2.json", "coords": [19.0862, -155.7292]},
            "mlv17": {"json": "mlv17.json", "coords": [19.1784, -155.7295]},
            "mlv5014": {"json": "mlv5014.json", "coords": [19.2061, -155.7449]},
            "mlv5012": {"json": "mlv5012.json", "coords": [19.1867, -155.7427]},
            "mlv5011": {"json": "mlv5011.json", "coords": [19.2255, -155.7453]},
            "mlv5013": {"json": "mlv5013.json", "coords": [19.2603, -155.7431]},
            "mlv14": {"json": "mlv14.json", "coords": [19.23748, -155.74508]},
            "mlv5025": {"json": "mlv5025.json", "coords": [19.2799, -155.7339]},
            "mlv5024": {"json": "mlv5024.json", "coords": [19.2931, -155.7267]}
            }
        },
    { # QUADRANT 2
        "bounds": {"lat_min": 18.8431, "lat_max": 20.4565, "lon_min": -155.723, "lon_max": -155.273},
        "vents": {
            "mlv9":  {"json": "mlv9.json",  "coords": [19.0541, -155.6781]},
            "mlv21": {"json": "mlv21.json", "coords": [19.3213, -155.709]},
            "mlv27": {"json": "mlv27.json", "coords": [19.3408, -155.6947]},
            "mlv10": {"json": "mlv10.json", "coords": [19.0798, -155.6923]},
            "mlv5018": {"json": "mlv5018.json", "coords": [19.3551, -155.6779]},
            "mlv5015": {"json": "mlv5015.json", "coords": [19.3110, -155.7167]},
            "mlv5020": {"json": "mlv5020.json", "coords": [19.0896, -155.6979]},
            "mlv5021": {"json": "mlv5021.json", "coords": [19.0734, -155.6813]},
            "mlv65": {"json": "mlv65.json", "coords": [19.522, -155.4338]},
            "mlv5026": {"json": "mlv5026.json", "coords": [19.3127, -155.7173]}
            }
        },
    { # QUADRANT 3
        "bounds": {"lat_min": 18.8431, "lat_max": 20.4565, "lon_min": -155.373, "lon_max": -154.923},
        "vents": {
            "mlv59":  {"json": "mlv59.json",  "coords": [19.5591, -155.2292]},
            "mlv60": {"json": "mlv60.json", "coords": [19.5248, -155.2274]},
            "mlv1000": {"json": "mlv1000.json", "coords": [19.534, -155.2064]},
            "mlv1001": {"json": "mlv1001.json", "coords": [19.5432, -155.2193]},
            "mlv1002": {"json": "mlv1002.json", "coords": [19.5202, -155.2110]},
            "mlv1003": {"json": "mlv1003.json", "coords": [19.5156, -155.2358]},
            "mlv5028": {"json": "mlv5028.json", "coords": [19.5586, -155.3256]}
            }
        },
     { # QUADRANT 4
        "bounds": {"lat_min": 18.8431, "lat_max": 20.4565, "lon_min": -155.023, "lon_max": -154.999},
        "vents": {}
        }       
    ]

