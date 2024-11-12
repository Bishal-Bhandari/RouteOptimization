import json

import openrouteservice
import folium
import os
import webbrowser

# API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# ORS API key
api_key = api_keys['ORS_API']['API_key']

# Start and end coordinates
start_coords = (49.8932278185995, 10.891899867894832)  # ZOB
end_coords = (49.90028516297074, 10.857067388124692)  # Hesslergasse

# Initialize an OpenRouteService client
client = openrouteservice.Client(key=api_key)

# Get the route directions
route = client.directions(
    coordinates=[start_coords, end_coords],
    profile='driving-car',
    format='geojson',
    radiuses=[5000, 5000]  # Increase radius to 1000 meters for both points
    )

# Extract route coordinates
route_coords = [(point[1], point[0]) for point in route['features'][0]['geometry']['coordinates']]

# Create a Folium map centered at the midpoint of the route
midpoint = [(start_coords[1] + end_coords[1]) / 2, (start_coords[0] + end_coords[0]) / 2]
route_map = folium.Map(location=midpoint, zoom_start=14)

# Add the route as a PolyLine on the map
folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(route_map)

# Add markers for the start and end points
folium.Marker(location=(start_coords[1], start_coords[0]), tooltip="Start Point",
              icon=folium.Icon(color="green")).add_to(route_map)
folium.Marker(location=(end_coords[1], end_coords[0]), tooltip="End Point", icon=folium.Icon(color="red")).add_to(
    route_map)

# Save the map
map_file = "../templates/route_map.html"
route_map.save(map_file)

# Open map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
