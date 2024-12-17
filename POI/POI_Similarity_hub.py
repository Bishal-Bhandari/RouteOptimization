import os
import webbrowser
from folium import PolyLine
import pandas as pd
import folium

# File paths
poi_file = '../refineData/osm_poi_rank_data.ods'
bus_stop_file = '../refineData/final_busStop_density.ods'

# Load data
poi_data = pd.read_excel(poi_file, engine='odf')
bus_stop_data = pd.read_excel(bus_stop_file, engine='odf')

# Clean data
poi_data = poi_data.dropna(subset=['lat', 'lon', 'popularity_rank'])
bus_stop_data = bus_stop_data.dropna(subset=['Latitude', 'Longitude'])


# Color categories
def rank_to_color(rank):
    colors = ['red', 'orange', 'yellow', 'green', 'black', 'purple', 'pink', 'brown', 'cyan', 'magenta']
    if rank == 1:
        return colors[0]
    elif rank == 2:
        return colors[1]
    elif rank == 3:
        return colors[2]
    elif rank == 4:
        return colors[3]
    elif rank == 5:
        return colors[4]
    elif rank == 6:
        return colors[5]
    elif rank == 7:
        return colors[6]
    elif rank == 8:
        return colors[7]
    elif rank == 9:
        return colors[8]
    else:
        return colors[9]


# Folium map
center_lat = poi_data['lat'].mean()
center_lon = poi_data['lon'].mean()
map_folium = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# Group POIs
rank_groups = {}

# POIs with color
for _, poi in poi_data.iterrows():
    color = rank_to_color(poi['similarity_rank'])
    folium.CircleMarker(
        location=[poi['lat'], poi['lon']],
        radius=6,  # Dot size
        color=color,  # Color based on rank
        fill=True,
        fill_color=color,  # Fill color
        fill_opacity=0.8,
        tooltip=f"POI: {poi.get('name', 'Unnamed POI')}\nRank: {poi['similarity_rank']}"
    ).add_to(map_folium)

    # Group POIs by their rank for connecting lines
    rank_groups.setdefault(poi['similarity_rank'], []).append((poi['lat'], poi['lon']))

# Add lines connecting POIs of the same rank
for rank, locations in rank_groups.items():
    color = rank_to_color(rank)
    if len(locations) > 1:  # Only draw lines if multiple points exist
        PolyLine(locations, color=color, weight=2.5, opacity=0.7).add_to(map_folium)

# Add bus stops as blue dots
for _, bus_stop in bus_stop_data.iterrows():
    folium.CircleMarker(
        location=[bus_stop['Latitude'], bus_stop['Longitude']],
        radius=4,  # Dot size
        color='blue',  # Border color
        fill=True,
        fill_color='blue',  # Fill color
        fill_opacity=0.8,
        tooltip=f"Bus Stop: {bus_stop.get('Stop name', 'Unnamed Stop')}"
    ).add_to(map_folium)

# Save the map to an HTML file
map_file = "../templates/POI_similarity_hub_Map.html"
map_folium.save(map_file)
# Open the map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")

print(f"Map saved to {map_file}")
