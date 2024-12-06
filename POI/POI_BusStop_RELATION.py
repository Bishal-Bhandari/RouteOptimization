import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load POI and bus stop data
poi_file = "../refineData/osm_poi_rank_data.ods"  # Replace with your POI file path
bus_stop_file = "../refineData/final_busStop_density.ods"  # Replace with your bus stop file path

poi_data = pd.read_excel(poi_file, engine='odf')
bus_stop_data = pd.read_excel(bus_stop_file, engine='odf')


# Define a function to calculate bus stops within a 500-meter radius of a given POI
def find_nearby_bus_stops(poi, bus_stops, radius=500):
    poi_location = (poi['lat'], poi['lon'])
    nearby_stops = []

    for _, bus_stop in bus_stops.iterrows():
        bus_stop_location = (bus_stop['Latitude'], bus_stop['Longitude'])
        distance = geodesic(poi_location, bus_stop_location).meters
        if distance <= radius:
            nearby_stops.append((bus_stop['Stop name'], bus_stop['Latitude'], bus_stop['Longitude']))

    return nearby_stops


# Create a graph to plot POIs and bus stops
G = nx.Graph()

# Add POIs to the graph as nodes (red dots)
for _, poi in poi_data.iterrows():
    G.add_node(poi['name'], pos=(poi['lon'], poi['lat']), color='red', type='POI')

# Add bus stops to the graph as nodes (blue dots)
for _, bus_stop in bus_stop_data.iterrows():
    G.add_node(bus_stop['Stop name'], pos=(bus_stop['Longitude'], bus_stop['Latitude']), color='blue', type='Bus Stop')

# Add edges connecting POIs to nearby bus stops (with the same color line)
for _, poi in poi_data.iterrows():
    nearby_stops = find_nearby_bus_stops(poi, bus_stop_data)
    for stop_name, stop_lat, stop_lon in nearby_stops:
        G.add_edge(poi['name'], stop_name)

# Extract positions for plotting
positions = nx.get_node_attributes(G, 'pos')
colors = [G.nodes[node]['color'] for node in G.nodes]

# Draw the graph
plt.figure(figsize=(10, 10))

# Draw POIs as red dots and bus stops as blue dots
nx.draw_networkx_nodes(G, positions, node_size=100, node_color=colors)
nx.draw_networkx_labels(G, positions)

# Draw edges with the same color
nx.draw_networkx_edges(G, positions, width=1, alpha=0.5, edge_color='gray')

# Show the graph
plt.title('POIs and Bus Stops within 500 meters')
plt.axis('off')
plt.show()
