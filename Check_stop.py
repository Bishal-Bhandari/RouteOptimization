import json
import pandas as pd

# Load and parse the JSON file
json_file_path = 'refineData/places_of_interest.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Extract latitude and longitude from JSON data
print("Coordinates from places_of_interest.json:")
json_coordinates = [(entry['latitude'], entry['longitude']) for entry in json_data]
for lat, lon in json_coordinates:
    print(f"Latitude: {lat}, Longitude: {lon}")

# Load and parse the ODS file
ods_file_path = 'refineData/final_busStop_density.ods'
ods_data = pd.read_excel(ods_file_path, engine='odf')

# Extract latitude and longitude from ODS data
print("\nCoordinates from final_busStop_density.ods:")
ods_coordinates = ods_data[['Latitude', 'Longitude']].dropna().values.tolist()
for lat, lon in ods_coordinates:
    print(f"Latitude: {lat}, Longitude: {lon}")
