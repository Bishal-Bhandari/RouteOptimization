import requests
import folium

def get_places_of_interest(api_key, location, radius=500, place_type='restaurant'):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,   # Format: "latitude,longitude"
        'radius': radius,       # Radius in meters
        'type': place_type,     # e.g., restaurant, park, cafe, etc.
        'key': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print("Error:", response.status_code)
        return []