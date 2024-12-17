import json
import os
import webbrowser

import requests
import geopandas as gpd
import pandas as pd
import folium
from folium import GeoJson

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']

# API endpoint
url = "https://api.mobilitytwin.brussels/stib/shapefile"

# File paths
output_file = "../refineData/Brussel MT/mobility_data_shape_file.ods"
map_file = "../templates/brussels_mobility_map.html"

# Data from the API
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

if response.status_code == 200:
    # JSON data to GeoDataFrame
    data = response.json()
    gdf = gpd.GeoDataFrame.from_features(data["features"])

    # CRS if missing
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)  # WGS84 Lat/Lon CRS

    # Projected CRS
    gdf_projected = gdf.to_crs(epsg=3857)

    centroids = gdf_projected.centroid

    centroids_geo = centroids.to_crs(epsg=4326)

    # Map center
    center_lat = centroids_geo.y.mean()
    center_lon = centroids_geo.x.mean()

    # GeoDataFrame to DataFrame
    new_data = pd.DataFrame(gdf.drop(columns='geometry'))

    # ODS file
    try:
        existing_data = pd.read_excel(output_file, engine='odf')
        print("Existing data loaded successfully.")
    except FileNotFoundError:
        print("Existing file not found. Creating a new file.")
        existing_data = pd.DataFrame()

    # Append new data
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Updated data to ODS file
    combined_data.to_excel(output_file, engine='odf', index=False)
    print(f"Data successfully appended and saved to {output_file}")

    # Create and save map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    GeoJson(gdf, name="Brussels Mobility Data").add_to(m)
    folium.LayerControl().add_to(m)

    # Save the map
    m.save(map_file)

    # Open the map in the browser
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")

else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    print(response.text)
