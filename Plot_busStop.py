import folium
import pandas as pd
import webbrowser
import os

# Load file
df = pd.read_excel('refineData/final_busStop_density.ods', engine='odf')  # file path

# Fill missing
df['Stop name'] = df['Stop name'].fillna('NA')
df['Bin'] = df['Bin'].fillna('NA')
df['Bench'] = df['Bench'].fillna('NA')

# Create a base map
center_lat = df['Latitude'].mean()
center_long = df['Longitude'].mean()
map = folium.Map(location=[center_lat, center_long], zoom_start=10)

# Add points
for index, row in df.iterrows():
    # Create a popup with information from the file
    popup_content = f"""
        <b>Stop Name:</b> {row['Stop name']}<br>
        <b>Available Bin:</b> {row['Bin']}<br>
        <b>Bench:</b> {row['Bench']}<br>
        <b>Population Density:</b> {row['Density']}<br>
    """

    # Tooltip
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color=f'#{hex(index)[2:]:0<6}',  # different color for each point
        fill=True,
        fill_color=f'#{hex(index)[2:]:0<6}',
        fill_opacity=0.7,
        tooltip=row['Stop name'],  # Tooltip when hovering
    ).add_to(map).add_child(folium.Popup(popup_content))  # Popup with detailed info

# Save the map
map_file = "templates/map_busStop.html"
map.save(map_file)

# Open the map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
