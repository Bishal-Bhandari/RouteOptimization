import json
import os
import webbrowser
import requests
import folium


def get_places_of_interest(api_key, location, radius=1000, place_types=None, keywords=None):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    all_results = []

    if place_types is None:
        place_types = ['tourist_attraction', 'museum', 'school', 'university', 'point_of_interest']
    if keywords is None:
        keywords = ['historical', 'landmark', 'monument', 'tourist']

    # Fetch results for each type and keyword
    for place_type in place_types:
        params = {
            'location': location,
            'radius': radius,
            'type': place_type,
            'key': api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            all_results.extend(response.json().get('results', []))

    for keyword in keywords:
        params = {
            'location': location,
            'radius': radius,
            'keyword': keyword,
            'key': api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            all_results.extend(response.json().get('results', []))

    return all_results


def plot_on_osm_map(api_key, location, radius=1000):
    # Parse location into latitude and longitude
    lat, lon = map(float, location.split(','))

    # Initialize map centered on the location
    folium_map = folium.Map(location=[lat, lon], zoom_start=14)

    # Get places of interest
    places = get_places_of_interest(api_key, location, radius)

    # Add a marker for each place of interest
    for place in places:
        place_name = place.get('name')
        place_location = place.get('geometry', {}).get('location', {})
        place_lat = place_location.get('lat')
        place_lon = place_location.get('lng')

        if place_lat and place_lon:
            # Add marker to the map
            folium.Marker(
                location=[place_lat, place_lon],
                popup=place_name,
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(folium_map)

    # Save map to an HTML file
    map_file = "templates/places_of_interest_map.html"
    folium_map.save(map_file)

    # Open the map
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")


# Load the API keys from the JSON file
with open('api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']
location = "49.89517023418082, 10.885055540762723"  # Bamberg
plot_on_osm_map(api_key, location)
