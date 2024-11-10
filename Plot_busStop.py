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
map = folium.Map(location=[center_lat, center_long], zoom_start=11.5)
# Add points
for index, row in df.iterrows():
    # Create a popup with information from the file
    popup_content = f"""
    <div style="width: 150px;">  <!-- Adjust width as desired -->
        <b>Stop Name:</b> {row['Stop name']}<br>
        <b>Available Bin:</b> {row['Bin']}<br>
        <b>Bench:</b> {row['Bench']}<br>
        <b>Population Density:</b> {row['Density']}<br>
    </div>
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

# To display information section
table_html = f"""
<div style="position: fixed; 
            top: 0px; right: 10px; 
            width: 240px; 
            height: auto; 
            padding: 10px; 
            background-color: white; 
            border: 2px solid black; 
            z-index: 9999; 
            overflow-y: auto;">
    <h4>Information</h4>
    <h5>Population is based on 1km X 1km grid provided by <a href="https://experience.arcgis.com/experience/2ce4e1cccb244421a281fa813c7523fc">Statistische Ämter des Bundes und der Länder</a></h5>
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <th style="border: 1px solid black; padding: 5px;">Density Level</th>
            <th style="border: 1px solid black; padding: 5px;">Population</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">5</td>
            <td style="border: 1px solid black; padding: 5px;">5770 to 8800</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">4</td>
            <td style="border: 1px solid black; padding: 5px;">3850 to 5770</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">3</td>
            <td style="border: 1px solid black; padding: 5px;">2480 to 3850</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">2</td>
            <td style="border: 1px solid black; padding: 5px;">1440 to 2480</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">1</td>
            <td style="border: 1px solid black; padding: 5px;">Under 1140</td>
        </tr>
    </table><br>
    <h5>49°54'03.8"N 10°53'28.4"E is the mean point for map displaying 12 km of its nearest bus stop.</h5>
</div>
"""

table_html += "</table></div>"

# Add HTML table into the map's HTML
map.get_root().html.add_child(folium.Element(table_html))

# Save the map
map_file = "templates/map_busStop.html"
map.save(map_file)

# Open the map
file_path = os.path.abspath(map_file)
webbrowser.open(f"file://{file_path}")
