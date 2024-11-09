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

# Find the shortest path between the nodes
route = nx.shortest_path(G, orig_node, dest_node, weight='length')

# Convert node coordinates in the route to a list of lat-lng pairs
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

# Create a Folium map centered at the midpoint of the route
midpoint = ((start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2)
m = folium.Map(location=midpoint, zoom_start=14)

# Add the route as a PolyLine to the map
folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.8).add_to(m)

# Add markers for the start and end points
folium.Marker(location=start_point, tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(location=end_point, tooltip="End", icon=folium.Icon(color="red")).add_to(m)

# Display the map
m.save("route_map.html")
m