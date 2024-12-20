import os
import webbrowser

import pandas as pd
import folium
from geopy.distance import geodesic

# Load POI and bus stop data
poi_file = "../refineData/osm_poi_rank_data.ods"  # Replace with your POI file path
bus_stop_file = "../refineData/final_busStop_density.ods"  # Replace with your bus stop file path

poi_data = pd.read_excel(poi_file, engine='odf')
bus_stop_data = pd.read_excel(bus_stop_file, engine='odf')

# Clean data
poi_data = poi_data.dropna(subset=['lat', 'lon'])
bus_stop_data = bus_stop_data.dropna(subset=['Latitude', 'Longitude'])


# Find nearby bus stops within a radius
def find_nearby_bus_stops(poi, bus_stops, radius=200):
    poi_location = (poi['lat'], poi['lon'])
    nearby_stops = []

    for _, bus_stop in bus_stops.iterrows():
        bus_stop_location = (bus_stop['Latitude'], bus_stop['Longitude'])
        distance = geodesic(poi_location, bus_stop_location).meters
        if distance <= radius:
            stop_name = bus_stop.get('Stop name', f"Bus Stop {_}")
            nearby_stops.append((bus_stop['Latitude'], bus_stop['Longitude'], stop_name))
    return nearby_stops


# Folium map
center_lat = poi_data['lat'].mean()
center_lon = poi_data['lon'].mean()
map_folium = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# For the ODS file
results = []

# Add POI marker
for _, poi in poi_data.iterrows():
    poi_name = poi.get('name', "Unnamed POI")
    poi_location = (poi['lat'], poi['lon'])

    # Find nearby bus stops
    nearby_stops = find_nearby_bus_stops(poi, bus_stop_data)
    # Add POI dot to the map
    folium.CircleMarker(
        location=[poi['lat'], poi['lon']],
        radius=3,  # Dot size
        color='red',  # Border color
        fill=True,
        fill_color='red',  # Fill color
        fill_opacity=0.8,
        tooltip=f"POI: {poi_name}"  # Show name on hover
    ).add_to(map_folium)

    # Edges and bus stop
    for stop_lat, stop_lon, stop_name in nearby_stops:
        # Line connecting POI to bus stop
        folium.PolyLine(
            locations=[poi_location, (stop_lat, stop_lon)],
            color='blue',
            weight=3,
            opacity=0.5
        ).add_to(map_folium)

        # Add bus stop dot
        folium.CircleMarker(
            location=[stop_lat, stop_lon],
            radius=3,  # Dot size
            color='green',  # Border color
            fill=True,
            fill_color='blue',  # Fill color
            fill_opacity=0.8,
            tooltip=f"Bus Stop: {stop_name}"  # Show name on hover
        ).add_to(map_folium)

    # Save results to a list
    results.append({
        'POI Name': poi_name,
        'Bus Stop Locations': ', '.join(
            f"{stop_name} ({stop_lat}, {stop_lon})" for stop_lat, stop_lon, stop_name in nearby_stops),
        'Bus Stop Count': len(nearby_stops),
        'Popularity Rank': poi.get('popularity_rank', None)
    })

# Into a DataFrame
results_df = pd.DataFrame(results)

# Save the results to an ODS file
output_file = "../refineData/POI_BusStops_Proximity_with_Rank1.ods"  # Replace with your desired output file path
results_df.to_excel(output_file, index=False, engine='odf')

# Save the map to an HTML file
map_file = "../templates/POI_BusStops_Map.html"  # Replace with your desired map file path
map_folium.save(map_file)
# Open the map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")

print(f"Data saved to {output_file} and map saved to {map_file}.")
