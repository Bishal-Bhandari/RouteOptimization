import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load POI and bus stop data
poi_file = "../refineData/osm_poi_rank_data.ods"  # Replace with your POI file path
bus_stop_file = "../refineData/final_busStop_density.ods"  # Replace with your bus stop file path

poi_data = pd.read_excel(poi_file, engine='odf')
bus_stop_data = pd.read_excel(bus_stop_file, engine='odf')

# Clean data: Remove rows where latitude or longitude are NaN
poi_data = poi_data.dropna(subset=['lat', 'lon'])
bus_stop_data = bus_stop_data.dropna(subset=['Latitude', 'Longitude'])


# Define a function to calculate bus stops within a 500-meter radius of a given POI
def find_nearby_bus_stops(poi, bus_stops, radius=200):
    poi_location = (poi['lat'], poi['lon'])
    nearby_stops = []

    for _, bus_stop in bus_stops.iterrows():
        bus_stop_location = (bus_stop['Latitude'], bus_stop['Longitude'])
        distance = geodesic(poi_location, bus_stop_location).meters
        if distance <= radius:
            nearby_stops.append(bus_stop['Stop name'])

    return nearby_stops


# Initialize a list to store the results
results = []
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
    if nearby_stops:
        for stop_name in nearby_stops:
            G.add_edge(poi['name'], stop_name)  # Add edge only if within 500 meters

        # Save the results to generate the POI data file
        results.append({
            'POI Name': poi['name'],
            'Bus Stop Names': ', '.join(str(stop) for stop in nearby_stops) if nearby_stops else None,
            'Bus Stop Count': len(nearby_stops),
            'Popularity Rank': poi['popularity_rank']
        })

# Convert results into a DataFrame
results_df = pd.DataFrame(results)

# Save the results to an ODS file
output_file = "../refineData/POI_BusStops_Proximity_with_Rank.ods"  # Replace with your desired output file path
results_df.to_excel(output_file, index=False, engine='odf')

# Extract positions for plotting
positions = nx.get_node_attributes(G, 'pos')
colors = [G.nodes[node]['color'] for node in G.nodes]

# Draw the graph
plt.figure(figsize=(12, 12))

# Draw POIs as red dots and bus stops as blue dots
nx.draw_networkx_nodes(G, positions, node_size=100, node_color=colors)
nx.draw_networkx_labels(G, positions)

# Draw edges with the same color
nx.draw_networkx_edges(G, positions, width=1, alpha=0.5, edge_color='gray')

# Show the graph
plt.show()
print(f"Results saved to {output_file}")
