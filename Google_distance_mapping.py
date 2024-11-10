import requests
import folium
import webbrowser
import os
import polyline
import json

from Calculate_time import *

# Load the API keys from the JSON file
with open('api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']

# Start and destination coordinates
start_point = "49.893738936899936,10.891734692962915"  # Start point (latitude, longitude)
End_point = "49.90029382224009,10.857069593929015"  # End point (latitude, longitude)

# Request URL with alternatives enabled
req_url = (f"https://maps.googleapis.com/maps/api/directions/json?origin={start_point}&destination={End_point}"
           f"&mode=transit&alternatives=true&key={api_key}")

# API call
API_response = requests.get(req_url)

# Parse the response
if API_response.status_code == 200:
    data = API_response.json()

    # Check if routes are available
    if data['routes']:
        # Center the map on the midpoint of the first route
        first_route = data['routes'][0]
        decoded_coords_first = polyline.decode(first_route['overview_polyline']['points'])
        midpoint = [(decoded_coords_first[0][0] + decoded_coords_first[-1][0]) / 2,
                    (decoded_coords_first[0][1] + decoded_coords_first[-1][1]) / 2]
        m = folium.Map(location=midpoint, zoom_start=13)

        all_routes_data = []  # List to save data for all routes

        # Loop through each route
        for route_index, route in enumerate(data['routes']):
            legs = route['legs'][0]
            distance = legs['distance']['text']
            duration = legs['duration']['text']
            steps = legs['steps']

            bus_info = []
            for step in steps:
                if step['travel_mode'] == 'TRANSIT':
                    transit_details = step['transit_details']
                    bus_info.append({
                        "bus_name": transit_details['line']['short_name'],
                        "departure_stop": transit_details['departure_stop']['name'],
                        "arrival_stop": transit_details['arrival_stop']['name']
                    })

            # Decode the polyline for this route
            polyline_data = route['overview_polyline']['points']
            decoded_coords = polyline.decode(polyline_data)

            # Save coordinates and bus line info for this route
            route_data = {"route_index": route_index, "distance": distance, "duration": duration, "coordinates": []}
            for i, coord in enumerate(decoded_coords):
                coord_data = {"coordinates": coord}
                if i < len(bus_info):  # Only add bus line info for relevant points
                    coord_data["bus_name"] = bus_info[i]["bus_name"]
                route_data["coordinates"].append(coord_data)
            all_routes_data.append(route_data)

            # Add the route's polyline to the map
            folium.PolyLine(decoded_coords, color="blue", weight=5, tooltip=f"Route {route_index + 1}: {distance}, {duration}").add_to(m)

            # Add markers for the start and end points
            folium.Marker(
                location=(decoded_coords[0][0], decoded_coords[0][1]),
                popup=f"Start Point - Route {route_index + 1}<br>Distance: {distance}<br>Duration: {duration}",
                icon=folium.Icon(color='green')
            ).add_to(m)

            folium.Marker(
                location=(decoded_coords[-1][0], decoded_coords[-1][1]),
                popup=f"End Point - Route {route_index + 1}<br>Distance: {distance}<br>Duration: {duration}",
                icon=folium.Icon(color='red')
            ).add_to(m)

            # Add bus ride details as markers along the route
            for i, info in enumerate(bus_info):
                folium.Marker(
                    location=(decoded_coords[i + 1][0], decoded_coords[i + 1][1]),
                    popup=f"Bus: {info['bus_name']}<br>Departure: {info['departure_stop']}<br>Arrival: {info['arrival_stop']}",
                    icon=folium.Icon(color='blue')
                ).add_to(m)

        # Save all route data to a JSON file
        with open('refineData/all_routes_data.json', 'w') as outfile:
            json.dump(all_routes_data, outfile, indent=4)

        # Save and display the map
        map_file = "templates/all_routes_map.html"
        m.save(map_file)

        # Open the saved map
        file_path = os.path.abspath(map_file)
        webbrowser.open(f"file://{file_path}")

    else:
        print("No routes found.")
else:
    print(f"Error in Google Directions API request: {API_response.status_code}")
