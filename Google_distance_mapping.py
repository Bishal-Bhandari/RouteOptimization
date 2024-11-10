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

req_url = (f"https://maps.googleapis.com/maps/api/directions/json?origin={start_point}&destination={End_point}"
           f"&mode=transit&key={api_key}")

# API call
API_response = requests.get(req_url)

# Parse the response
if API_response.status_code == 200:
    data = API_response.json()

    # Validation of route data
    if data['routes']:
        route = data['routes'][0]
        legs = route['legs'][0]

        # Extract the data of distance and time
        distance = legs['distance']['text']
        duration = legs['duration']['text']

        # Extract the steps
        steps = legs['steps']

        bus_info = []
        for step in steps:
            if step['travel_mode'] == 'TRANSIT':
                transit_details = step['transit_details']

                # # Get approx. stop time
                # bus_stop_time = CalcTime(transit_details, duration)
                # duration = bus_stop_time
                bus_info.append({
                    "bus_name": transit_details['line']['short_name'],
                    "departure_stop": transit_details['departure_stop']['name'],
                    "arrival_stop": transit_details['arrival_stop']['name']

                })

        # Get route's polyline
        polyline_data = route['overview_polyline']['points']

        # Get a list of lat/lon tuples
        decoded_coords = polyline.decode(polyline_data)

        # Save coordinates and bus line info to a file
        saved_data = []
        for i, coord in enumerate(decoded_coords):
            data_entry = {"coordinates": coord}
            if i < len(bus_info):  # Only add bus line info for relevant points
                data_entry["bus_name"] = bus_info[i]["bus_name"]
            saved_data.append(data_entry)

        # Save to JSON file
        with open('refineData/decoded_coords_with_bus_info.json', 'w') as outfile:
            json.dump(saved_data, outfile, indent=4)

        # Centering the Folium map between the two points
        midpoint = [(decoded_coords[0][0] + decoded_coords[-1][0]) / 2,
                    (decoded_coords[0][1] + decoded_coords[-1][1]) / 2]
        m = folium.Map(location=midpoint, zoom_start=13)

        # Adding the bus route to the map
        folium.PolyLine(decoded_coords, color="blue", weight=5).add_to(m)

        # Adding pin for start and end points with info
        folium.Marker(
            location=(decoded_coords[0][0], decoded_coords[0][1]),
            popup=f"Start Point<br>Distance: {distance}<br>Duration: {duration}",
            icon=folium.Icon(color='green')
        ).add_to(m)

        folium.Marker(
            location=(decoded_coords[-1][0], decoded_coords[-1][1]),
            popup=f"End Point<br>Distance: {distance}<br>Duration: {duration}",
            icon=folium.Icon(color='red')
        ).add_to(m)

        # Adding details for each bus ride
        for i, info in enumerate(bus_info):
            folium.Marker(
                location=(decoded_coords[i + 1][0], decoded_coords[i + 1][1]),
                popup=f"Bus: {info['bus_name']}<br>Departure: {info['departure_stop']}<br>Arrival: {info['arrival_stop']}",
                icon=folium.Icon(color='blue')
            ).add_to(m)

        # Save and display the map
        map_file = "templates/bus_route_map.html"
        m.save(map_file)

        # Open the saved map
        file_path = os.path.abspath(map_file)
        webbrowser.open(f"file://{file_path}")

    else:
        print("No route found.")
else:
    print(f"Error in Google API request: {API_response.status_code}")
