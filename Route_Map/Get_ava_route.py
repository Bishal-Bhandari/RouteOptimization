import requests
import json
import folium
import os
import webbrowser
import polyline

# API keys from the JSON file
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']

# Start point
start_point = "49.893738936899936,10.891734692962915"  # ZOB

# List of destination coordinates
destinations = [
    (49.90454893430373, 10.851693436193193),  # Gaustadt Ziegelei
    # (49.9237529380112, 10.893679811566336),  # Hallstadt Ost
    # (49.8786226434617, 10.929225395216823),  # Strullendorfer Straße
    # (49.87255962112503, 10.874977083590274),  # Bamberg König-Konrad-Str.
    # (49.86451606207455, 10.910425276172134)   # Bug Schloßstr.
]

# List to store route data
all_routes_data = []

# Loop through each destination
for idx, destination in enumerate(destinations):
    end_point = f"{destination[0]},{destination[1]}"

    # Request for cars
    req_url_driving = (f"https://maps.googleapis.com/maps/api/directions/json"
                       f"?origin={start_point}&destination={end_point}&mode=driving&alternatives=true&key={api_key}")

    # Request for bus
    req_url_transit = (f"https://maps.googleapis.com/maps/api/directions/json"
                       f"?origin={start_point}&destination={end_point}&mode=transit&alternatives=true&key={api_key}")

    # Request for cars routes
    response_driving = requests.get(req_url_driving)
    # Request for bus routes
    response_transit = requests.get(req_url_transit)

    # Parse for cars routes
    if response_driving.status_code == 200:
        route_data = response_driving.json()
        if route_data['routes']:
            # Loop through all available cars routes
            for route_idx, route in enumerate(route_data['routes']):
                legs = route['legs'][0]

                # Get route details
                distance = legs['distance']['text']
                duration = legs['duration']['text']
                polyline_data = route['overview_polyline']['points']
                # Polyline to coordinates
                try:
                    decoded_coords = polyline.decode(polyline_data)

                    # Append route info to list
                    route_info = {
                        "route_index": f"{idx}-{route_idx}-driving",  # To distinguish between modes and alternatives
                        "mode": "driving",
                        "distance": distance,
                        "duration": duration,
                        "coordinates": [{"latitude": lat, "longitude": lon} for lat, lon in decoded_coords]
                    }
                    all_routes_data.append(route_info)
                except Exception as e:
                    print(f"Error decoding polyline for driving route {idx + 1}, alternative {route_idx + 1}: {e}")

    # Parse for bus routes
    if response_transit.status_code == 200:
        route_data = response_transit.json()
        if route_data['routes']:
            # Loop through all available bus routes
            for route_idx, route in enumerate(route_data['routes']):
                legs = route['legs'][0]

                # Get route details
                distance = legs['distance']['text']
                duration = legs['duration']['text']
                polyline_data = route['overview_polyline']['points']
                # Polyline to coordinates
                try:
                    decoded_coords = polyline.decode(polyline_data)

                    # Append route info to list
                    route_info = {
                        "route_index": f"{idx}-{route_idx}-bus",  # To distinguish between modes and alternatives
                        "mode": "bus",
                        "distance": distance,
                        "duration": duration,
                        "coordinates": [{"latitude": lat, "longitude": lon} for lat, lon in decoded_coords]
                    }
                    all_routes_data.append(route_info)
                except Exception as e:
                    print(f"Error decoding polyline for bus route {idx + 1}, alternative {route_idx + 1}: {e}")

    else:
        print(f"Failed to fetch routes to {end_point}: {response_driving.status_code} (driving), {response_transit.status_code} (bus)")

# Save route to JSON
output_file = "../refineData/bamberg_all_routes_from_start.json"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(all_routes_data, f, indent=4)

# Plotting all routes on a map
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
    mode = route['mode']

    # Draw line for each route
    folium.PolyLine(
        coordinates,
        color=colors[int(route_index.split('-')[1]) % len(colors)],  # Different color for each alternative route
        weight=5,
        opacity=0.7,
        tooltip=f"{mode.capitalize()} Route {route_index}: Distance {route['distance']}, Duration {route['duration']}"
    ).add_to(map)

    # Destination maker
    folium.Marker(
        location=coordinates[-1],
        popup=f"Destination {route_index} ({mode.capitalize()})",
        icon=folium.Icon(color="red")
    ).add_to(map)

# Start marker
folium.Marker(
    location=start_location,
    popup="Start Point",
    icon=folium.Icon(color="green")
).add_to(map)

# Save map to HTML file and open it
map_file = "../templates/bamberg_all_routes_map.html"
map.save(map_file)
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
