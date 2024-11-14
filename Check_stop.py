import json
import os
import webbrowser

import pandas as pd
import folium

# Load and parse the JSON file
json_file_path = 'refineData/places_of_interest.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Load and parse the ODS file
ods_file_path = 'refineData/final_busStop_density.ods'
ods_data = pd.read_excel(ods_file_path, engine='odf')

# Initialize the map centered around Bamberg, assuming that’s the region for these coordinates
m = folium.Map(location=[49.8917, 10.8871], zoom_start=13)

# Plot ODS coordinates as red dots
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

# Plot JSON coordinates as blue dots with names
for entry in json_data:
    folium.CircleMarker(
        location=[entry['latitude'], entry['longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        tooltip=entry['name']
    ).add_to(m)

for entry in json_data:
    folium.CircleMarker(
        location=[entry['latitude'], entry['longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        tooltip=entry['name']
    ).add_to(m)

# Save the map to an HTML file and display it
map_file = 'templates/coordinates_map.html'
m.save(map_file)

# Open the saved map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
