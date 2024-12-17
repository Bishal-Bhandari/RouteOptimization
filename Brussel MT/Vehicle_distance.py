import requests
import json
import pandas as pd
import pyexcel as p

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']

url = "https://api.mobilitytwin.brussels/stib/vehicle-distance"

try:
    # Fetch data from API
    response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})
    print(f"Status Code: {response.status_code}")

    # Parse JSON response
    data = response.json()

    # Output ODS file
    ods_file = "../refineData/Brussel MT/vehicle_distance.ods"

    # Load existing ODS file
    try:
        existing_data = p.get_records(file_name=ods_file)
        existing_df = pd.DataFrame(existing_data)
        print("Existing data loaded successfully.")
    except FileNotFoundError:
        print("Existing file not found. Creating a new file.")
        existing_df = pd.DataFrame()

    # To DataFrame
    new_df = pd.DataFrame(data)

    # Append new data
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Save the updated data
    p.save_as(records=combined_df.to_dict(orient='records'), dest_file_name=ods_file)
    print(f"Data successfully appended and saved to {ods_file}")

except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON response.")
except Exception as e:
    print(f"An error occurred: {e}")
