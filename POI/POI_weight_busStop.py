import json

import requests
import pandas as pd
import time

# ODS file
file_path = '../refineData/final_busStop_density.ods'
bus_stops = pd.read_excel(file_path, engine='odf')

# Load the API keys
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']

# Radius
radius = 500

# Type of places
place_type = {
    1: "Train Stations", 2: "Shopping Centers", 3: "Bus Stops", 4: "Airports", 5: "Schools", 6: "Universities",
    7: "Hospitals", 8: "Residential Areas", 9: "Tourist Attractions", 10: "Restaurants", 11: "Office Complexes",
    12: "Parks", 13: "Museums", 14: "Cinemas", 15: "Markets", 16: "Nightclubs", 17: "Sports Arenas", 18: "Hotels",
    19: "Temples", 20: "Churches", 21: "City Halls", 22: "Playgrounds", 23: "Cafes", 24: "Libraries",
    25: "Bus Depots", 26: "Parking Lots", 27: "Historical Sites", 28: "Monuments", 29: "Zoos", 30: "Art Galleries",
    31: "Convention Centers", 32: "Beaches", 33: "Harbors", 34: "Cemeteries", 35: "Casinos", 36: "Gyms",
    37: "Government Offices", 38: "Fire Stations", 39: "Police Stations", 40: "Prisons", 41: "Post Offices",
    42: "Stadiums", 43: "Amusement Parks", 44: "Bridges", 45: "Campgrounds", 46: "Embassies", 47: "Warehouses",
    48: "Theaters", 49: "Golf Courses",
}

# Store the results
poi_results = []

# Set to track saved POIs
processed_pois = set()


# Search POI
def get_nearby_places(lat, lng, radius, place_type):
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    )
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": list(place_type.values()),
        "key": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


# Loop eacj bus stop
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

            # Skip POI if existed
            if poi_key in processed_pois:
                continue

            # Add POI
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

    # API rate limits
    # time.sleep(1)  # Adjust based on your API usage limits

# Results into a DataFrame
poi_df = pd.DataFrame(poi_results)

# Save the DataFrame to an ODS file
output_path = '../refineData/bus_stop_nearby_pois.ods'
poi_df.to_excel(output_path, engine='odf', index=False)

print(f"Data saved to {output_path}")
