import json
import os
import webbrowser

import requests
import pandas as pd
import folium

# Load the API keys from the JSON file
with open('api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']

# Define the search location and radius
location = '49.898813,10.902763'  # Example: Bamberg, Germany
radius = 1000  # Radius in meters
poi_type = 'restaurant'  # Example: Fetch restaurants


# Step 1: Fetch POIs using Places API
def get_pois(location, radius, poi_type, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,
        'radius': radius,
        'type': poi_type,
        'key': api_key
    }
    response = requests.get(url, params=params)
    return response.json()['results']


# Step 2: Fetch details for each POI
def get_poi_details(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'name,rating,user_ratings_total,geometry,opening_hours,popular_times',
        'key': api_key
    }
    response = requests.get(url, params=params)
    return response.json().get('result', {})


# Step 3: Process and save data
def save_to_ods(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(f"{filename}.ods", index=False, engine="odf")


# Step 4: Display POIs on a map
def display_pois_on_map(pois):
    m = folium.Map(location=[float(location.split(',')[0]), float(location.split(',')[1])], zoom_start=15)
    for poi in pois:
        name = poi.get('name', 'Unknown')
        lat = poi['geometry']['location']['lat']
        lng = poi['geometry']['location']['lng']
        folium.Marker(location=[lat, lng], popup=name).add_to(m)
    return m


# Main workflow
def main():
    # Fetch POIs
    pois = get_pois(location, radius, poi_type, api_key)
    print(pois)
    # Extract details and save to list
    poi_data = []
    for poi in pois:
        details = get_poi_details(poi['place_id'], api_keys)

        # Skip if geometry is missing
        if 'geometry' not in details:
            print(f"Skipping place_id {poi['place_id']} due to missing geometry.")
            continue

        # Collect data
        poi_data.append({
            'Name': details.get('name', 'N/A'),
            'Rating': details.get('rating', 'N/A'),
            'Latitude': details.get('geometry', {}).get('location', {}).get('lat', 'N/A'),
            'Longitude': details.get('geometry', {}).get('location', {}).get('lng', 'N/A'),
            'Popular Times': details.get('popular_times', 'N/A')
        })

    # Save to ODS
    save_to_ods(poi_data, "refineData/poi_data")

    # Display on Folium map
    map_file = display_pois_on_map(pois)
    map_file.save("templates/poi_map.html")
    # Open the map
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")


# Run the program
main()
