import json
import pandas as pd
from math import radians, cos, sin, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  # Distance in meters


# Load and parse the JSON file
json_file_path = 'refineData/places_of_interest.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Extract latitude and longitude from JSON data
json_coordinates = [(entry['latitude'], entry['longitude']) for entry in json_data]

# Load and parse the ODS file
ods_file_path = 'refineData/final_busStop_density.ods'
ods_data = pd.read_excel(ods_file_path, engine='odf')

# Extract latitude and longitude from ODS data
ods_coordinates = ods_data[['Latitude', 'Longitude']].dropna().values.tolist()

# Compare each pair of coordinates
for json_lat, json_lon in json_coordinates:
    found_nearby = False
    for ods_lat, ods_lon in ods_coordinates:
        distance = haversine(json_lat, json_lon, ods_lat, ods_lon)
        print(distance)
        if distance <= 200:
            print("Yes")
            found_nearby = True
            break
        else:
            print("No")
