import json

import pandas as pd
import requests

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Brussel MT API key
api_key = api_keys['Brussels']['API_key']

# Define the API endpoint and your API key
url = "https://api.mobilitytwin.brussels/stib/speed"

# Fetch data from the API
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Check if data is in a suitable format (list of dictionaries)
        if isinstance(data, list):
            # Convert directly to a pandas DataFrame
            df = pd.DataFrame(data)
        elif "features" in data:  # Handle GeoJSON-like structures
            df = pd.json_normalize(data["features"])
        else:
            raise ValueError("Unexpected data format. Adjust the code as needed.")

        # Define the output ODS file name
        output_file = "speed_data.ods"

        # Save to an ODS file
        df.to_excel(output_file, engine="odf", index=False)

        print(f"Data successfully saved to {output_file}")

    except ValueError as e:
        print(f"Error processing the JSON data: {e}")

else:
    # Handle HTTP error responses
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
