import json
import os
import webbrowser
from math import radians, cos, sin, sqrt, atan2

import pandas as pd
import folium


# Calculate haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of Earth in meters
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# JSON file
json_file_path = '../refineData/places_of_interest.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# ODS file
file_path = '../refineData/final_busStop_density.ods'
ods_data = pd.read_excel(file_path, engine='odf')

# List to store POI results
poi_results = []

# Initialize the map
m = folium.Map(location=[49.8917, 10.8871], zoom_start=13)

# Plot bus stop
for _, row in ods_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        tooltip=f"Bus Stop: {row['Stop name']}"
    ).add_to(m)

# Check distance of POIs from bus stops
for entry in json_data:
    poi_lat, poi_lon = entry['latitude'], entry['longitude']
    nearest_bus_stop = None
    nearest_distance = float('inf')

    # Check if any bus stop is within 500 meters
    for _, row in ods_data.iterrows():
        bus_stop_lat, bus_stop_lon = row['Latitude'], row['Longitude']
        distance = haversine(poi_lat, poi_lon, bus_stop_lat, bus_stop_lon)
        if distance <= nearest_distance:  # POI is within 500m
            nearest_distance = distance
            nearest_bus_stop = row['Stop name']

    # Determine POI color based on distance to the nearest bus stop
    poi_color = 'blue' if nearest_distance <= 500 else 'black'

    # Create a popup with nearest bus stop and distance information
    popup_text = f"POI: {entry['name']}<br>"
    if nearest_distance <= 500:
        popup_text += f"Nearest Bus Stop: {nearest_bus_stop}<br>Distance: {nearest_distance:.2f} meters"
        poi_results.append({
            "POI": entry['name'],
            "Latitude": poi_lat,
            "Longitude": poi_lon,
            "Nearest Bus Stop": nearest_bus_stop,
            "Distance (m)": round(nearest_distance, 2)
        })
    else:
        popup_text += "No bus stop within 500 meters"
        poi_results.append({
            "POI": entry['name'],
            "Latitude": poi_lat,
            "Longitude": poi_lon,
            "Nearest Bus Stop": "NA",
            "Distance (m)": "NA"
        })

    # Plot the POI
    folium.CircleMarker(
        location=[poi_lat, poi_lon],
        radius=5,
        color=poi_color,
        fill=True,
        fill_color=poi_color,
        fill_opacity=0.6,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=entry['name']
    ).add_to(m)

# Save the map to an HTML file and display it
map_file = '../templates/coordinates_map.html'
m.save(map_file)
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")

# To a DataFrame
poi_df = pd.DataFrame(poi_results)
# Save the DataFrame
output_path = '../refineData/poi_bus_stop_proximity.ods'
poi_df.to_excel(output_path, engine='odf', index=False)