import json
import os
import webbrowser
import folium

# Load the JSON data
with open("refineData/all_routes_data.json", "r") as f:
    data = json.load(f)

# Initialize the map centered at an average location
start_location = [49.8936, 10.89168]
map = folium.Map(location=start_location, zoom_start=15)

# Define colors for each route
colors = ['blue', 'red', 'black', 'yellow', 'green', 'brown']

# Loop through each route in the data
for route in data:
    coordinates = [point['coordinates'] for point in route['coordinates']]
    route_index = route['route_index']
    route_distance = route['distance']
    route_duration = route['duration']
    bus_name = route['coordinates'][0].get('bus_name', 'Unknown')

    # Add route line to the map
    folium.PolyLine(
        coordinates,
        color=colors[route_index % len(colors)],
        weight=5,
        opacity=0.7,
        tooltip=f"Route {route_index + 1}: {bus_name}, {route_distance}, {route_duration}"
    ).add_to(map)

    # Add markers at the start and end of the route
    folium.Marker(
        location=coordinates[0],
        popup=f"Start of Route {route_index + 1}",
        icon=folium.Icon(color="green" if route_index == 0 else "blue")
    ).add_to(map)
    folium.Marker(
        location=coordinates[-1],
        popup=f"End of Route {route_index + 1}",
        icon=folium.Icon(color="red")
    ).add_to(map)

# Save the map to an HTML file
# Save the map
map_file = "templates/map_multi_route.html"
map.save(map_file)

# Open the map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
