import json
import os
import webbrowser
import requests
import folium


# Get place of interest
def get_places_of_interest(api_key, location, radius=15000, place_types=None, keywords=None):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    all_results = []

    if place_types is None:
        place_types = ['tourist_attraction', 'museum', 'school', 'university', 'point_of_interest', 'atm', 'bank',
                       'train_station', 'supermarket', 'shopping_mall', 'pharmacy', 'library', 'department_store',
                       'church', 'airport', 'Markets', 'Hospitals', 'Clinics', 'Historical_monuments', 'Castles']
    if keywords is None:
        keywords = ['historical', 'landmark', 'monument', 'tourist']

    # Get results
    for place_type in place_types:
        params = {
            'location': location,
            'radius': radius,
            'type': place_type,
            'language': 'en',
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


def save_places_to_json(places, filename="refineData/places_of_interest.json"):
    places_data = []

    for place in places:
        place_name = place.get('name')
        place_location = place.get('geometry', {}).get('location', {})
        place_lat = place_location.get('lat')
        place_lon = place_location.get('lng')
        place_types = place.get('types', [])  # List of types associated with the place

        # Add to the data list if latitude and longitude exist
        if place_lat and place_lon:
            places_data.append({
                "name": place_name,
                "latitude": place_lat,
                "longitude": place_lon,
                "types": place_types
            })

    # Save the data to a JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(places_data, file, ensure_ascii=False, indent=4)


def plot_on_osm_map(api_key, location, radius=15000):
    # Parse location
    lat, lon = map(float, location.split(','))

    # Initialize map
    folium_map = folium.Map(location=[lat, lon], zoom_start=14)

    # Get POI
    places = get_places_of_interest(api_key, location, radius)

    # Add a marker
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
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(folium_map)

    # Save map to an HTML file
    map_file = "templates/places_of_interest_map.html"
    folium_map.save(map_file)

    # Open the map
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")

    # Save data to JSON
    save_places_to_json(places)


def main():
    # Load the API keys from the JSON file
    with open('api_keys.json') as json_file:
        api_keys = json.load(json_file)

    # Google Maps API key
    api_key = api_keys['Google_API']['API_key']
    location = "49.89517023418082, 10.885055540762723"  # Bamberg
    plot_on_osm_map(api_key, location)


if __name__ == "__main__":
    main()
