import pandas as pd
import plotly.express as px

# Load your CSV file (update the path if needed)
df = pd.read_excel('/path/to/your_file.ods', engine='odf')

# Group by 'Bus_Stop' and count the unique bus lines for each stop
bus_stop_groups_detailed = df.groupby('Bus_Stop').agg({
    'Bus_Line': lambda x: list(x.unique())  # List of unique bus lines for each stop
}).reset_index()

# Count the number of lines each bus stop serves
bus_stop_groups_detailed['Line_Count'] = bus_stop_groups_detailed['Bus_Line'].apply(len)


# Define clusters based on the range of bus lines served
def assign_cluster(line_count):
    if line_count == 1:
        return '1 Line'
    elif line_count == 2:
        return '2 Lines'
    else:
        return '3+ Lines'


bus_stop_groups_detailed['Cluster'] = bus_stop_groups_detailed['Line_Count'].apply(assign_cluster)

# Prepare data for plotting with clusters
bus_stop_groups_detailed['Bus_Lines'] = bus_stop_groups_detailed['Bus_Line'].apply(lambda x: ', '.join(map(str, x)))

# Create an interactive scatter plot
fig = px.scatter(
    bus_stop_groups_detailed,
    x='Line_Count',
    y='Bus_Stop',
    color='Cluster',
    hover_data={'Bus_Stop': True, 'Bus_Lines': True, 'Line_Count': True},
    title='Interactive Clustering of Bus Stops by Number of Bus Lines'
)

# Customize plot appearance
fig.update_layout(
    xaxis_title='Number of Bus Lines Served',
    yaxis_title='Bus Stop',
    yaxis={'categoryorder': 'total ascending'},  # Arrange bus stops based on clustering
    title_x=0.5
)

# Show the interactive plot
fig.show()
