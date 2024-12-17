import json
import requests
import geopandas as gpd
import pandas as pd

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']

# API endpoint
url = "https://api.mobilitytwin.brussels/stib/vehicle-position"

# Fetch data from API
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

if response.status_code == 200:
    try:
        # Parse the JSON
        data = response.json()

        # JSON to GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(data["features"])

        # Extract latitude and longitude
        gdf["latitude"] = gdf.geometry.y
        gdf["longitude"] = gdf.geometry.x

        # GeoDataFrame to a DataFrame
        df = gdf.drop(columns="geometry")

        # ODS file path
        output_file = "../refineData/Brussel MT/vehicle_position_data_with_latlong.ods"

        # Load existing ODS file
        try:
            existing_data = pd.read_excel(output_file, engine="odf")
            print("Existing data loaded successfully.")
        except FileNotFoundError:
            print("Existing file not found. Creating a new file.")
            existing_data = pd.DataFrame()

        # Append the new data
        combined_data = pd.concat([existing_data, df], ignore_index=True)

        # Save the updated data
        combined_data.to_excel(output_file, engine='odf', index=False)
        print(f"Data successfully appended and saved to {output_file}")

    except ValueError as e:
        print(f"Error processing the JSON data: {e}")

else:
    # Handle HTTP error responses
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
