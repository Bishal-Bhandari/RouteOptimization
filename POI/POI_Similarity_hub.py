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


# Define color categories based on popularity rank
def rank_to_color(rank):
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'cyan', 'magenta']
    if rank <= 2:
        return colors[0]  # red
    elif rank <= 4:
        return colors[1]  # orange
    elif rank <= 6:
        return colors[2]  # yellow
    elif rank <= 8:
        return colors[3]  # green
    elif rank <= 10:
        return colors[4]  # blue
    elif rank <= 12:
        return colors[5]  # purple
    elif rank <= 14:
        return colors[6]  # pink
    elif rank <= 16:
        return colors[7]  # brown
    elif rank <= 18:
        return colors[8]  # cyan
    else:
        return colors[9]


# Create a Folium map centered on the average coordinates of the POI data
center_lat = poi_data['lat'].mean()
center_lon = poi_data['lon'].mean()
map_folium = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# Add POIs with color-coded dots
for _, poi in poi_data.iterrows():
    folium.CircleMarker(
        location=[poi['lat'], poi['lon']],
        radius=6,  # Dot size
        color=rank_to_color(poi['popularity_rank']),  # Color based on rank
        fill=True,
        fill_color=rank_to_color(poi['popularity_rank']),  # Fill color
        fill_opacity=0.8,
        tooltip=f"POI: {poi.get('name', 'Unnamed POI')}\nRank: {poi['popularity_rank']}"
    ).add_to(map_folium)

# Add bus stops as blue dots
for _, bus_stop in bus_stop_data.iterrows():
    folium.CircleMarker(
        location=[bus_stop['Latitude'], bus_stop['Longitude']],
        radius=4,  # Dot size
        color='blue',  # Border color
        fill=True,
        fill_color='blue',  # Fill color
        fill_opacity=0.8,
        tooltip=f"Bus Stop: {bus_stop.get('name', 'Unnamed Stop')}"
    ).add_to(map_folium)

# Save the map to an HTML file
map_file = "/mnt/data/POI_BusStops_Map.html"
map_folium.save(map_file)

print(f"Map saved to {map_file}")
