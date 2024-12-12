import json

import pandas as pd
import requests
import geopandas as gpd

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']
# Define the API endpoint and your API key
url = "https://api.mobilitytwin.brussels/stib/vehicle-position"

# Fetch data from the API
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Convert the features to a GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(data["features"])

        # Convert the GeoDataFrame to a pandas DataFrame for saving
        df = pd.DataFrame(gdf)

        # Define the output ODS file name
        output_file = "vehicle_position_data.ods"

        # Save to an ODS file
        df.to_excel(output_file, engine="odf", index=False)

        print(f"Data successfully saved to {output_file}")

    except ValueError as e:
        print(f"Error processing the JSON data: {e}")

else:
    # Handle HTTP error responses
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
