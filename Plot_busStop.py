import folium
import pandas as pd
import webbrowser
import os

# Load file
df = pd.read_excel('refineData/final_busStop_density.ods', engine='odf')  # file path

# Fill missing values
df['Stop name'] = df['Stop name'].fillna('NA')
df['Bin'] = df['Bin'].fillna('NA')
df['Bench'] = df['Bench'].fillna('NA')

# Create a base map
center_lat = df['Latitude'].mean()
center_long = df['Longitude'].mean()
map = folium.Map(location=[center_lat, center_long], zoom_start=11)

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

# Create the HTML table content for the right corner
table_html = f"""
<div style="position: fixed; 
            top: 10px; right: 10px; 
            width: 300px; 
            height: auto; 
            padding: 10px; 
            background-color: white; 
            border: 2px solid black; 
            z-index: 9999; 
            overflow-y: auto;">
    <h4>Info</h4>
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <th style="border: 1px solid black; padding: 5px;">Density Level</th>
            <th style="border: 1px solid black; padding: 5px;">Population</th>
        </tr>
"""

for index, row in df.iterrows():
    table_html += f"""
        <tr>
            <td style="border: 1px solid black; padding: 5px;">{row['Stop name']}</td>
            <td style="border: 1px solid black; padding: 5px;">{row['Bin']}</td>
            <td style="border: 1px solid black; padding: 5px;">{row['Bench']}</td>
            <td style="border: 1px solid black; padding: 5px;">{row['Density']}</td>
        </tr>
    """

table_html += "</table></div>"

# Add the HTML overlay to the map
from folium import IFrame

iframe = IFrame(table_html, width=350, height=400)
popup = folium.Popup(iframe, max_width=400)
folium.Marker([center_lat, center_long], icon=folium.DivIcon(html=table_html)).add_to(map)

# Save the map
map_file = "templates/map_busStop.html"
map.save(map_file)

# Open the map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
