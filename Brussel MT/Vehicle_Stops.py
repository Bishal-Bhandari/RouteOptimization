import json
import os
import webbrowser

import requests
import geopandas as gpd
import pandas as pd
import folium
import pyexcel as p

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']

url = "https://api.mobilitytwin.brussels/stib/stops"

try:
    # Fetch data from API
    response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})
    print(f"Status Code: {response.status_code}")

    # Parse JSON response
    data = response.json()

    # Check if "features" exists in data
    if "features" in data:
        gdf = gpd.GeoDataFrame.from_features(data["features"])

        # Define ODS file path
        ods_file = "../refineData/Brussel MT/stib_stops.ods"

        # GeoDataFrame to DataFrame
        df = pd.DataFrame(gdf.drop(columns="geometry"))  # Drop geometry for ODS compatibility
        records = df.to_dict(orient='records')

        # Load existing ODS file
        try:
            existing_data = p.get_records(file_name=ods_file)
            existing_df = pd.DataFrame(existing_data)
            print("Existing data loaded successfully.")
        except FileNotFoundError:
            print("Existing file not found. Creating a new file.")
            existing_df = pd.DataFrame()

        # Append new data
        combined_df = pd.concat([existing_df, df], ignore_index=True)

        # Save the updated data
        p.save_as(records=combined_df.to_dict(orient='records'), dest_file_name=ods_file)
        print(f"Data successfully appended and saved to {ods_file}")
        '''
        # Plot data on a Folium map
        m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=12)

        # Add each point to the map
        for _, row in gdf.iterrows():
            if row.geometry.is_empty or not row.geometry.is_valid:
                continue
            coords = row.geometry.centroid
            folium.Marker(
                location=[coords.y, coords.x],
                popup=row.get("stop_name", "Unknown Stop")  # Replace 'name' with the actual stop name field
            ).add_to(m)

        # Save the map to an HTML file
        map_file = "../templates/stib_stops_map.html"
        m.save(map_file)
        # Open the saved map
        file_path = os.path.abspath(map_file)
        webbrowser.open(f"file://{file_path}")
        '''

    else:
        print("The 'features' key is missing in the response.")

except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response.")
except Exception as e:
    print(f"An error occurred: {e}")
