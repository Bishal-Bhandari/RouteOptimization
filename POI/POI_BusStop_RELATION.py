import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load POI and bus stop data
poi_file = "../refineData/osm_poi_rank_data.ods"  # Replace with your POI file path
bus_stop_file = "../refineData/final_busStop_density.ods"  # Replace with your bus stop file path

poi_data = pd.read_excel(poi_file, engine='odf')
bus_stop_data = pd.read_excel(bus_stop_file, engine='odf')

# Clean data
poi_data = poi_data.dropna(subset=['lat', 'lon'])
bus_stop_data = bus_stop_data.dropna(subset=['Latitude', 'Longitude'])


# Calculate bus stops within a 100-meter radius of a given POI
def find_nearby_bus_stops(poi, bus_stops, radius=200):
    poi_location = (poi['lat'], poi['lon'])
    nearby_stops = []

    for _, bus_stop in bus_stops.iterrows():
        bus_stop_location = (bus_stop['Latitude'], bus_stop['Longitude'])
        distance = geodesic(poi_location, bus_stop_location).meters
        if distance <= radius:
            nearby_stops.append((bus_stop['Latitude'], bus_stop['Longitude']))  # Use lat/lon tuple

    return nearby_stops


# List to store the results
results = []
# Plot POIs and bus stops
G = nx.Graph()

# Add POIs (red dots) with names
for _, poi in poi_data.iterrows():
    poi_label = poi['name']
    G.add_node(
        (poi['lat'], poi['lon']),
        pos=(poi['lon'], poi['lat']),
        color='red',
        label=poi_label,
        type='POI'
    )

# Add bus stops (blue dots) with identifiers
for idx, bus_stop in bus_stop_data.iterrows():
    stop_label = f"BusStop {'Stop name'}"
    G.add_node(
        (bus_stop['Latitude'], bus_stop['Longitude']),
        pos=(bus_stop['Longitude'], bus_stop['Latitude']),
        color='blue',
        label=stop_label,
        type='Bus Stop'
    )

# Edges connecting POIs to nearby bus stops
for _, poi in poi_data.iterrows():
    nearby_stops = find_nearby_bus_stops(poi, bus_stop_data)
    if nearby_stops:
        for stop_location in nearby_stops:
            G.add_edge((poi['lat'], poi['lon']), stop_location)

        # Save the results to generate the POI data file
        results.append({
            'POI Name': poi['name'],
            'Bus Stop Locations': ', '.join(str(stop) for stop in nearby_stops) if nearby_stops else None,
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
