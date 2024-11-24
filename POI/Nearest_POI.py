import json

import requests
import pandas as pd
import time

# Load bus stop locations from your ODS file
file_path = '../refineData/final_busStop_density.ods'
bus_stops = pd.read_excel(file_path, engine='odf')

# Load the API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']

# Define the search radius (500 meters)
radius = 500

# Define the type of places you want to search for (e.g., 'point_of_interest', 'restaurant', etc.)
place_type = "point_of_interest"

# Initialize a list to store the results
poi_results = []

# Set to track already saved POIs (use latitude and longitude as unique identifiers)
processed_pois = set()

# Function to search nearby places using Google Maps API
def get_nearby_places(lat, lng, radius, place_type):
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    )
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type,
        "key": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


# Iterate over each bus stop
for _, row in bus_stops.iterrows():
    bus_stop_name = row['Stop name']
    latitude = row['Latitude']
    longitude = row['Longitude']

    # Get nearby POIs
    places_data = get_nearby_places(latitude, longitude, radius, place_type)

    if places_data and "results" in places_data:
        for place in places_data["results"]:
            poi_lat = place["geometry"]["location"]["lat"]
            poi_lon = place["geometry"]["location"]["lng"]
            poi_key = (poi_lat, poi_lon)  # Unique identifier for the POI

            # Skip if POI is already processed
            if poi_key in processed_pois:
                continue

            # Add POI to the results
            poi_results.append({
                "Bus Stop": bus_stop_name,
                "Bus Stop Latitude": latitude,
                "Bus Stop Longitude": longitude,
                "POI Name": place.get("name", "Unknown"),
                "POI Latitude": poi_lat,
                "POI Longitude": poi_lon,
                "POI Address": place.get("vicinity", "Unknown")
            })

            # Mark this POI as processed
            processed_pois.add(poi_key)

    # Pause to respect API rate limits
    # time.sleep(1)  # Adjust based on your API usage limits

# Convert the results into a DataFrame
poi_df = pd.DataFrame(poi_results)

# Save the DataFrame to an ODS file
output_path = '../refineData/bus_stop_nearby_pois.ods'
poi_df.to_excel(output_path, engine='odf', index=False)

print(f"Data saved to {output_path}")
