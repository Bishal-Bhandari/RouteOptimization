import pandas as pd
import plotly.express as px

# File upload
df = pd.read_excel('refineData/BusLine_And_Stops.ods', engine='odf')

# Group by 'Bus_Stop' and count the unique bus lines for each stop
bus_stop_groups_detailed = df.groupby('Bus_Stop').agg({
    'Bus_Line': lambda x: list(x.unique())  # List of unique bus lines for each stop
}).reset_index()

# Counting the bus line based on stop
bus_stop_groups_detailed['Line_Count'] = bus_stop_groups_detailed['Bus_Line'].apply(len)


# For cluster based on the bus line
def assign_cluster(line_count):
    if line_count == 1:
        return '1 Line'
    elif line_count == 2:
        return '2 Lines'
    elif line_count == 3:
        return '3 Lines'
    elif line_count == 4:
        return '4 Lines'
    elif line_count == 5:
        return '5 Lines'
    elif line_count == 6:
        return '6 Lines'
    elif line_count == 7:
        return '7 Lines'
    elif line_count == 8:
        return '8 Lines'
    elif line_count == 9:
        return '9 Lines'
    else:
        return '10+ Lines'


bus_stop_groups_detailed['Cluster'] = bus_stop_groups_detailed['Line_Count'].apply(assign_cluster)

# Plotting for cluster
bus_stop_groups_detailed['Bus_Lines'] = bus_stop_groups_detailed['Bus_Line'].apply(lambda x: ', '.join(map(str, x)))
output_data = bus_stop_groups_detailed[['Bus_Stop', 'Cluster', 'Bus_Lines']]

# Save output
output_data.to_csv("refineData/bus_stop_clusters.csv", index=False)


# For scatter plot
fig = px.scatter(
    bus_stop_groups_detailed,
    x='Line_Count',
    y='Bus_Stop',
    color='Cluster',
    hover_data={'Bus_Stop': True, 'Bus_Lines': True, 'Line_Count': True},
    title='Bus Stops by Number of Bus Lines'
)

# Plot label
fig.update_layout(
    xaxis_title='Number of Bus Lines',
    yaxis_title='Bus Stop',
    yaxis={'categoryorder': 'total ascending'},  # Arrange bus stops based on clustering
    title_x=0.5
)

# Show plot
fig.show()
