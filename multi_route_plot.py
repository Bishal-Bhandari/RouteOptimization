import json
import os
import webbrowser
import folium

# Load the JSON
with open("refineData/bamberg_all_routes_from_start.json", "r") as f:
    data = json.load(f)

# Map centered at an average location
start_location = [49.8936, 10.89168]  # start point
map = folium.Map(location=start_location, zoom_start=15)

# Colors for each route
colors = ['blue', 'red', 'black', 'green', 'cyan',
          'magenta', 'yellow', 'olive', 'gray', 'brown',
          'purple', 'pink', 'teal', 'navy', 'tan',
          'maroon', 'steelblue', 'orchid', 'orange', 'tomato',
          'chocolate', 'forestgreen', 'slategrey', 'crimson']

# Loop through each route in file
for route in data:
    route_index = route['route_index']
    mode = route['mode']  # Cars or Bus
    route_distance = route['distance']
    route_duration = route['duration']

    # Get coordinates for plotting
    coordinates = [(point['latitude'], point['longitude']) for point in route['coordinates']]

    # Add the polyline for map
    folium.PolyLine(
        coordinates,
        color=colors[int(route_index.split('-')[1]) % len(colors)],  # Different color for each alternative route
        weight=5,
        opacity=0.7,
        tooltip=f"{mode.capitalize()} Route {route_index}: Distance {route_distance}, Duration {route_duration}"
    ).add_to(map)

    # Start marker
    folium.Marker(
        location=coordinates[0],
        popup=f"Start of {mode.capitalize()} Route {route_index}",
        icon=folium.Icon(color="green")
    ).add_to(map)
    # End marker
    folium.Marker(
        location=coordinates[-1],
        popup=f"End of {mode.capitalize()} Route {route_index}",
        icon=folium.Icon(color="red")
    ).add_to(map)

    # Bus stop markers
    if mode == 'bus' and 'bus_info' in route:
        for bus_stop in route['bus_info']:
            stop_coords = bus_stop.get('coordinates',
                                       coordinates[0])
            folium.Marker(
                location=stop_coords,
                popup=f"Bus Stop: {bus_stop.get('bus_name', 'Unknown')}<br>Departure: "
                      f"{bus_stop.get('departure_stop', 'Unknown')}<br>Arrival: "
                      f"{bus_stop.get('arrival_stop', 'Unknown')}",
                icon=folium.Icon(color="blue")
            ).add_to(map)

# Save the map
map_file = "templates/map_multi_route.html"
map.save(map_file)

# Open the map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
