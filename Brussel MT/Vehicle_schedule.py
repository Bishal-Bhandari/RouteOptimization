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

url = "https://api.mobilitytwin.brussels/stib/vehicle-schedule"

try:
    # Fetch data from API
    response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})
    print(f"Status Code: {response.status_code}")

    # Parse JSON response
    data = response.json()

    # Save GeoDataFrame to ODS format
    ods_file = "../refineData/Brussel MT/Vehicle_schedule.ods"
    p.save_as(records=data, dest_file_name=ods_file)

except Exception as e:
    print(f"An error occurred: {e}")
