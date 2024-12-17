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

# API endpoint and authorization
url = "https://api.mobilitytwin.brussels/stib/shapefile"

# Fetch data from the API
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

# Check if the request was successful
if response.status_code == 200:
    # Convert JSON data to a GeoDataFrame
    data = response.json()
    gdf = gpd.GeoDataFrame.from_features(data["features"])

    # Assign a CRS if missing (default to WGS84)
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)  # WGS84 Lat/Lon CRS

    # Reproject to a projected CRS (Web Mercator or Belgium Lambert 72)
    gdf_projected = gdf.to_crs(epsg=3857)  # Web Mercator projection

    # Calculate centroids in the projected CRS
    centroids = gdf_projected.centroid

    # Reproject centroids back to geographic CRS for plotting
    centroids_geo = centroids.to_crs(epsg=4326)

    # Calculate map center
    center_lat = centroids_geo.y.mean()
    center_lon = centroids_geo.x.mean()

    # Save to ODS file
    output_file = "../refineData/Brussel MT/mobility_data.ods"
    df = pd.DataFrame(gdf.drop(columns='geometry'))  # Drop geometry column for tabular data
    df.to_excel(output_file, engine='odf', index=False)
    print(f"Data saved to {output_file}")

    # Initialize the Folium map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Add GeoJSON data to the Folium map
    GeoJson(gdf, name="Brussels Mobility Data").add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    map_file = "../templates/brussels_mobility_map.html"
    m.save(map_file)
    # Open the map
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")

else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    print(response.text)
