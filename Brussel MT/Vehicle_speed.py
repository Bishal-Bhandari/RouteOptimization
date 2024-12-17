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

# Fetch data from API
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

if response.status_code == 200:
    try:
        # Parse the JSON
        data = response.json()

        # List of dictionaries
        if isinstance(data, list):
            # Pandas DataFrame
            df = pd.DataFrame(data)
        elif "features" in data:
            df = pd.json_normalize(data["features"])
        else:
            raise ValueError("Unexpected data format. Adjust the code as needed.")

        # Define the output ODS file
        output_file = "../refineData/Brussel MT/speed_data.ods"

        # Load existing ODS file
        try:
            existing_data = pd.read_excel(output_file, engine='odf')
            print("Existing data loaded successfully.")
        except FileNotFoundError:
            print("Existing file not found. Creating a new file.")
            existing_data = pd.DataFrame()

        # Append new data
        combined_data = pd.concat([existing_data, df], ignore_index=True)

        # Save the updated data
        combined_data.to_excel(output_file, engine='odf', index=False)
        print(f"Data successfully appended and saved to {output_file}")

    except ValueError as e:
        print(f"Error processing the JSON data: {e}")

else:
    # Handle HTTP error responses
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
