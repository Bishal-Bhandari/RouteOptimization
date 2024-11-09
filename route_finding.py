import folium
import os
import webbrowser
import networkx as nx
import osmnx as ox

# Define the coordinates for the start and end points
start_point = (49.8919, 10.8907)  # Replace with your starting point coordinates
end_point = (49.8988, 10.9026)    # Replace with your ending point coordinates

# Generate the road network graph for routing
G = ox.graph_from_point(start_point, dist=5000, network_type='drive')

# Find the nearest nodes to the start and end points in the graph
orig_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
dest_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

# Find the shortest path between these nodes
route = nx.shortest_path(G, orig_node, dest_node, weight='length')

# Convert the route to latitude-longitude coordinates
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

# Create a Folium map centered around the midpoint of the route
midpoint = ((start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2)
route_map = folium.Map(location=midpoint, zoom_start=14)

# Add the route as a PolyLine on the map
folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(route_map)

# Add markers for the start and end points
folium.Marker(location=start_point, tooltip="Start Point", icon=folium.Icon(color="green")).add_to(route_map)
folium.Marker(location=end_point, tooltip="End Point", icon=folium.Icon(color="red")).add_to(route_map)

# Save the map as an HTML file and open it in a browser
map_file = "route_map.html"
route_map.save(map_file)
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
