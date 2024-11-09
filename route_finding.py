import osmnx as ox
import networkx as nx
import folium

# Define the latitude and longitude for the start and end points
start_point = (49.8919, 10.8907)  # Replace with your starting point coordinates
end_point = (49.8988, 10.9026)    # Replace with your ending point coordinates

# Get a graph of the area around the starting and ending points
G = ox.graph_from_point(start_point, dist=5000, network_type='drive')

# Find the nearest nodes in the graph to the start and end points
orig_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
dest_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])