import requests
import json


def api_call():
    # Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Overpass QL query to get traffic light locations
    overpass_query = """
        [out:json][timeout:25];
        // gather results
        node["highway"="traffic_signals"](49.845,10.852,49.912,10.948); 
        out body;
        >;
        out skel qt;
        """

    # Request to the Overpass API
    response = requests.get(overpass_url, params={'data': overpass_query})
    return response


def get_traffic_light():
    response = api_call()
    # Request was successful?
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Coordinates of traffic lights
        for element in data['elements']:
            if element['type'] == 'node':  # Traffic lights are represented as nodes
                lat = element['lat']
                lon = element['lon']
                print(f"Traffic Light at lat: {lat}, lon: {lon}")
    else:
        print(f"Error: {response.status_code}")


class TrafficLight:
    def __init__(self):
        get_traffic_light()

