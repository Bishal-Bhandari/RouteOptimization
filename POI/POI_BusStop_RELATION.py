import pandas as pd
from geopy.distance import geodesic

# Load POI and bus stop data
poi_file = "osm_poi_rank_data.ods"  # Replace with your POI file path
bus_stop_file = "final_busStop_density.ods"  # Replace with your bus stop file path

poi_data = pd.read_excel(poi_file, engine='odf')
bus_stop_data = pd.read_excel(bus_stop_file, engine='odf')


# Bus stops within a 500-meter radius of a given POI
def find_nearby_bus_stops(poi, bus_stops, radius=500):
    poi_location = (poi['lat'], poi['lon'])
    nearby_stops = []

    for _, bus_stop in bus_stops.iterrows():
        bus_stop_location = (bus_stop['Latitude'], bus_stop['Longitude'])
        distance = geodesic(poi_location, bus_stop_location).meters
        if distance <= radius:
            nearby_stops.append(bus_stop['name'])

    return nearby_stops
