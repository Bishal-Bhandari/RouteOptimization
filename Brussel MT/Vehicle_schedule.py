import json

import requests
import geopandas as gpd
import pandas as pd
import pyexcel as p

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']

# Data from the API
url = "https://api.mobilitytwin.brussels/stib/vehicle-schedule"
headers = {'Authorization': 'Bearer [api_key]'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        gdf = gpd.GeoDataFrame.from_features(data["features"])

        # Convert GeoDataFrame to DataFrame
        df = pd.DataFrame(gdf)

        # Save to ODS file
        output_file = "vehicle_schedule_data.ods"
        df.to_excel(output_file, engine="odf", index=False)

        print(f"Data successfully saved to {output_file}")
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
