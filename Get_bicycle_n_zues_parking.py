import os
import webbrowser

import requests
import pandas as pd
import folium
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell


# Save data to file
def save_to_ods(data, filename):
    ods = OpenDocumentSpreadsheet()
    table = Table(name="Bicycle Parking")

    # Add header
    headers = list(data.columns)
    header_row = TableRow()
    for header in headers:
        header_row.addElement(TableCell(valuetype="string", value=str(header)))
    table.addElement(header_row)

    # Add rows
    for _, row in data.iterrows():
        table_row = TableRow()
        for cell in row:
            table_row.addElement(TableCell(valuetype="string", value=str(cell)))
        table.addElement(table_row)

    ods.spreadsheet.addElement(table)
    ods.save(filename)


# Overpass API query
def get_osm_bike_parking():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
     [out:json];
    (
      node["amenity"="bicycle_parking"](around:10000,49.8916,10.8989);
      way["amenity"="bicycle_parking"](around:10000,49.8916,10.8989);
      relation["amenity"="bicycle_parking"](around:10000,49.8916,10.8989);
    );
    out body;
    """

    # Request to the Overpass API
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Extract bicycle locations
    bike_parking_data = []
    for element in data['elements']:
        if element['type'] == 'node':
            bike_parking_data.append({
                'osmid': element['id'],
                'latitude': element['lat'],
                'longitude': element['lon']
            })
        elif element['type'] in ['way', 'relation']:
            pass

    # List to a DataFrame
    df = pd.DataFrame(bike_parking_data)
    return df


# Plot data on map
def plot_bike_parking_folium(data, output_file="templates/bicycle_parking_map.html"):
    # Initialize map
    m = folium.Map(location=[49.8916, 10.8989], zoom_start=13)

    # Add parking locations
    for _, row in data.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"OSM ID: {row['osmid']}",
            icon=folium.Icon(color="blue", icon="bicycle", prefix="fa"),
        ).add_to(m)

    # Save map
    m.save(output_file)

    # Open the map
    file_path = os.path.abspath(output_file)
    webbrowser.open(f"file://{file_path}")


# Main workflow
def main():
    # Fetch OSM bicycle data
    osm_data = get_osm_bike_parking()

    # Save to ODS
    ods_filename = "refineData/osm_bike_parking.ods"
    save_to_ods(osm_data[["osmid", "latitude", "longitude"]], ods_filename)

    # Plot data on map
    plot_bike_parking_folium(osm_data)


if __name__ == "__main__":
    main()
