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
response = requests.get(url, headers={
    'Authorization': 'Bearer [api_key]'
})
data = response.json()

# To GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(data["features"])

# Convert GeoDataFrame to DataFrame for saving to ODS
df = pd.DataFrame(gdf)

# Save to ODS file
output_file = "vehicle_schedule_data.ods"
df.to_excel(output_file, engine="odf", index=False)

print(f"Data successfully saved to {output_file}")
