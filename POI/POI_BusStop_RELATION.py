import pandas as pd
from geopy.distance import geodesic

# Load POI and bus stop data
poi_file = "osm_poi_rank_data.ods"  # Replace with your POI file path
bus_stop_file = "final_busStop_density.ods"  # Replace with your bus stop file path

poi_data = pd.read_excel(poi_file, engine='odf')
bus_stop_data = pd.read_excel(bus_stop_file, engine='odf')