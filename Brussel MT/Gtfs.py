import json
import requests
import geopandas as gpd
import pandas as pd

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
    print("Response received:", data)

    # Check if "features" exists in data
    if "features" in data:
        gdf = gpd.GeoDataFrame.from_features(data["features"])
        print("GeoDataFrame created:", gdf)

        # Plot the GeoDataFrame
        gdf.plot()

        # Save to ODS file (requires pandas_ods_writer or pyexcel_ods3)
        ods_file = "stib_stops.ods"
        pd.DataFrame(gdf).to_csv("stib_stops.csv", index=False)  # Temporary CSV fallback
        print(f"Saved GeoDataFrame to CSV as {ods_file}")
    else:
        print("The 'features' key is missing in the response.")

except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response.")
except Exception as e:
    print(f"An error occurred: {e}")
