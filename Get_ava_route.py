import requests
import json
import folium
import os
import webbrowser
import polyline

# Load the API keys from the JSON file
with open('api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']

# Start point (latitude, longitude)
start_point = "49.893738936899936,10.891734692962915"  # ZOB

# List of destination coordinates in Bamberg (latitude, longitude)
destinations = [
    (49.90454893430373, 10.851693436193193),  # Gaustadt Ziegelei
    (49.9237529380112, 10.893679811566336),  # Hallstadt Ost
    (49.8786226434617, 10.929225395216823),  # Strullendorfer Straße
    (49.87255962112503, 10.874977083590274),  # Bamberg König-Konrad-Str.
    (49.86451606207455, 10.910425276172134)   # Bug Schloßstr.
]

# Initialize a list to store route data
all_routes_data = []

# Loop through each destination
for idx, destination in enumerate(destinations):
    end_point = f"{destination[0]},{destination[1]}"

    # Build request URL for driving directions with alternatives enabled
    req_url = (f"https://maps.googleapis.com/maps/api/directions/json"
               f"?origin={start_point}&destination={end_point}&mode=driving&alternatives=true&key={api_key}")

    # Send request to the Google Directions API
    response = requests.get(req_url)

    # Parse the response
    if response.status_code == 200:
        route_data = response.json()
        if route_data['routes']:
            # Loop through all available routes
            for route_idx, route in enumerate(route_data['routes']):
                legs = route['legs'][0]

                # Extract route details
                distance = legs['distance']['text']
                duration = legs['duration']['text']
                polyline_data = route['overview_polyline']['points']
                # Decode the polyline to coordinates
                try:
                    decoded_coords = polyline.decode(polyline_data)

                    # Append route info to list if decoding is successful
                    route_info = {
                        "route_index": f"{idx}-{route_idx}",  # To distinguish multiple routes to the same destination
                        "distance": distance,
                        "duration": duration,
                        "coordinates": [{"latitude": lat, "longitude": lon} for lat, lon in decoded_coords]
                    }
                    all_routes_data.append(route_info)
                except Exception as e:
                    print(f"Error decoding polyline for route {idx + 1}, alternative {route_idx + 1}: {e}")
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
colors = ['blue', 'red', 'black', 'green', 'cyan',
          'magenta', 'yellow', 'olive', 'gray', 'brown',
          'purple', 'pink', 'teal', 'navy', 'tan',
          'maroon', 'steelblue', 'orchid', 'orange', 'tomato',
          'chocolate', 'forestgreen', 'slategrey', 'crimson']

# Plot each route
for route in all_routes_data:
    coordinates = [(point['latitude'], point['longitude']) for point in route['coordinates']]
    route_index = route['route_index']

    # Draw polyline for each route
    folium.PolyLine(
        coordinates,
        color=colors[int(route_index.split('-')[1]) % len(colors)],  # Different color for each alternative route
        weight=5,
        opacity=0.7,
        tooltip=f"Route {route_index}: Distance {route['distance']}, Duration {route['duration']}"
    ).add_to(map)

    # Add marker at destination
    folium.Marker(
        location=coordinates[-1],
        popup=f"Destination {route_index}",
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
