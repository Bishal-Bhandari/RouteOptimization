import requests
import json
import folium
import os
import webbrowser
import polyline

# Google Maps API key
api_key = 'YOUR_GOOGLE_API_KEY'

# Start point (latitude, longitude)
start_point = "49.893738936899936,10.891734692962915"

# List of destination coordinates in Bamberg (latitude, longitude)
destinations = [
    (49.8988, 10.9009),  # Bamberg University
    (49.8932, 10.8984),  # Altenburg Castle
    (49.8972, 10.8757),  # Brose Arena
    (49.8999, 10.8918),  # City Hall
    (49.8916, 10.8866)   # Bamberg Cathedral
]

# Initialize a list to store route data
all_routes_data = []

# Loop through each destination
for idx, destination in enumerate(destinations):
    end_point = f"{destination[0]},{destination[1]}"

    # Build request URL for driving directions
    req_url = (f"https://maps.googleapis.com/maps/api/directions/json"
               f"?origin={start_point}&destination={end_point}&mode=driving&key={api_key}")

    # Send request to the Google Directions API
    response = requests.get(req_url)

    # Parse the response
    if response.status_code == 200:
        route_data = response.json()
        if route_data['routes']:
            route = route_data['routes'][0]
            legs = route['legs'][0]

            # Extract route details
            distance = legs['distance']['text']
            duration = legs['duration']['text']
            polyline_data = route['overview_polyline']['points']
            decoded_coords = polyline.decode(polyline_data)

            # Append route info to list
            route_info = {
                "route_index": idx,
                "distance": distance,
                "duration": duration,
                "coordinates": [{"latitude": lat, "longitude": lon} for lat, lon in decoded_coords]
            }
            all_routes_data.append(route_info)
    else:
        print(f"Failed to fetch route to {end_point}: {response.status_code}")

# Save all route data to JSON file
output_file = "refineData/bamberg_all_routes_from_start.json"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(all_routes_data, f, indent=4)

# Plotting all routes on a Folium map
start_location = [49.893738936899936, 10.891734692962915]
map = folium.Map(location=start_location, zoom_start=13)
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']

# Plot each route
for route in all_routes_data:
    coordinates = [(point['latitude'], point['longitude']) for point in route['coordinates']]
    route_index = route['route_index']

    # Draw polyline for each route
    folium.PolyLine(
        coordinates,
        color=colors[route_index % len(colors)],
        weight=5,
        opacity=0.7,
        tooltip=f"Route {route_index + 1}: Distance {route['distance']}, Duration {route['duration']}"
    ).add_to(map)

    # Add marker at destination
    folium.Marker(
        location=coordinates[-1],
        popup=f"Destination {route_index + 1}",
        icon=folium.Icon(color="red")
    ).add_to(map)

# Add start marker
folium.Marker(
    location=start_location,
    popup="Start Point",
    icon=folium.Icon(color="green")
).add_to(map)

# Save the map to an HTML file and open it
map_file = "templates/bamberg_all_routes_map.html"
map.save(map_file)
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
