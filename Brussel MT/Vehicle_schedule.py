import json

import requests
import geopandas as gpd

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']

url = "https://api.mobilitytwin.brussels/stib/vehicle-schedule"

data = requests.get(url, headers={
    'Authorization': f'Bearer {api_key}'
}).json()

gdf = gpd.GeoDataFrame.from_features(data["features"])
# Plot the GeoDataFrame
gdf.plot()