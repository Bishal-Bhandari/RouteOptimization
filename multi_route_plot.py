import json
import os
import webbrowser
import folium

# Load the JSON data
with open("refineData/all_routes_data.json", "r") as f:
    data = json.load(f)

# Initialize the map centered at an average location (start point)
start_location = [49.8936, 10.89168]
map = folium.Map(location=start_location, zoom_start=13)

# Define colors for each route
colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown']

# Loop through each route in the data
for route in data:
    route_index = route['route_index']
    route_distance = route['distance']
    route_duration = route['duration']

    # Extract coordinates for plotting
    coordinates = [(point['latitude'], point['longitude']) for point in route['coordinates']]

    # Add the polyline for the route to the map
    folium.PolyLine(
        coordinates,
        color=colors[route_index % len(colors)],
        weight=5,
        opacity=0.7,
        tooltip=f"Route {route_index + 1}: Distance {route_distance}, Duration {route_duration}"
    ).add_to(map)

    # Add markers at the start and end of the route
    folium.Marker(
        location=coordinates[0],
        popup=f"Start of Route {route_index + 1}",
        icon=folium.Icon(color="green")
    ).add_to(map)
    folium.Marker(
        location=coordinates[-1],
        popup=f"End of Route {route_index + 1}",
        icon=folium.Icon(color="red")
    ).add_to(map)

    # Add markers for each bus stop, if available
    for bus_stop in route.get('bus_info', []):
        stop_coords = coordinates[0]  # Assume first coordinate for start
        folium.Marker(
            location=stop_coords,
            popup=f"Bus: {bus_stop['bus_name']}<br>Departure: {bus_stop['departure_stop']}<br>Arrival: {bus_stop['arrival_stop']}",
            icon=folium.Icon(color="blue")
        ).add_to(map)

# Save the map to an HTML file
map_file = "templates/map_multi_route.html"
map.save(map_file)

# Open the map in a web browser
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
