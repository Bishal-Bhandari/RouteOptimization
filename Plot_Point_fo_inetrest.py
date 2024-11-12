import requests
import folium


def get_places_of_interest(api_key, location, radius=500, place_type='restaurant'):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,  # Format: "latitude,longitude"
        'radius': radius,  # Radius in meters
        'type': place_type,  # e.g., restaurant, park, cafe, etc.
        'key': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print("Error:", response.status_code)
        return []


def plot_on_osm_map(api_key, location, radius=500, place_type='restaurant'):
    # Parse location into latitude and longitude
    lat, lon = map(float, location.split(','))

    # Initialize map centered on the location
    m = folium.Map(location=[lat, lon], zoom_start=15)

    # Get places of interest
    places = get_places_of_interest(api_key, location, radius, place_type)

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
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    # Save map to an HTML file
    m.save("places_of_interest_map.html")
    print("Map saved as 'places_of_interest_map.html'.")


# Replace with your API key and desired location
api_key = "YOUR_GOOGLE_API_KEY"
location = "48.137154,11.576124"  # Example coordinates (e.g., Munich)
plot_on_osm_map(api_key, location)
