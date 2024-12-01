import os
import folium
import pandas as pd
import requests

# Place types dictionary
place_type = {
    1: ["Train Stations", 1, 1], 2: ["Shopping Centers", 1, 5], 4: ["Airports", 1, 1], 5: ["Schools", 1, 2],
    6: ["Universities", 1, 2], 7: ["Hospitals", 1, 3], 8: ["Residential Areas", 1, 8], 9: ["Tourist Attractions", 1, 6],
    10: ["Restaurants", 1, 7],
    11: ["Office Complexes", 2, 5], 12: ["Parks", 2, 8], 13: ["Museums", 2, 2], 14: ["Cinemas", 2, 6],
    15: ["Markets", 2, 5],
    16: ["Nightclubs", 2, 6], 17: ["Sports Arenas", 2, 6], 18: ["Hotels", 2, 7], 19: ["Temples", 2, 4],
    20: ["Churches", 2, 4],
    21: ["City Halls", 3, 9], 22: ["Playgrounds", 3, 8], 23: ["Cafes", 3, 7], 24: ["Libraries", 3, 2],
    25: ["Bus Depots", 3, 1],
    26: ["Parking Lots", 3, 1], 27: ["Historical Sites", 3, 4], 28: ["Monuments", 3, 4], 29: ["Zoos", 3, 8],
    30: ["Art Galleries", 3, 2],
    31: ["Convention Centers", 4, 5], 32: ["Beaches", 4, 8], 33: ["Harbors", 4, 1], 34: ["Cemeteries", 4, 4],
    35: ["Casinos", 4, 5],
    36: ["Gyms", 4, 6], 37: ["Government Offices", 4, 9], 38: ["Fire Stations", 4, 3], 39: ["Police Stations", 4, 3],
    40: ["Prisons", 5, 9],
    41: ["Post Offices", 5, 9], 42: ["Stadiums", 5, 6], 43: ["Amusement Parks", 5, 6], 44: ["Bridges", 5, 1],
    45: ["Campgrounds", 5, 8],
    46: ["Embassies", 5, 9], 47: ["Warehouses", 5, 5], 48: ["Theaters", 5, 6], 49: ["Golf Courses", 5, 6]
}

# Store the results
poi_results = []

# Overpass API URL
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"


def get_osm_data(lat, lon, radius, poi_tag):
    """
    Query Overpass API for a specific POI type.
    """
    query = f"""
    [out:json];
    (
      node["{poi_tag}"](around:{radius},{lat},{lon});
      way["{poi_tag}"](around:{radius},{lat},{lon});
      relation["{poi_tag}"](around:{radius},{lat},{lon});
    );
    out center;
    """
    response = requests.get(OVERPASS_API_URL, params={"data": query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying Overpass API: {response.status_code}")
        return None


def process_osm_data(osm_data, poi_info):
    """
    Process OSM data to extract relevant POI details.
    """
    for element in osm_data.get("elements", []):
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")
        if lat and lon:
            poi_results.append({
                "POI Name": element.get("tags", {}).get("name", "Unknown"),
                "POI Type": poi_info[0],
                "POI Popularity": poi_info[1],
                "POI Similarity": poi_info[2],
                "Latitude": lat,
                "Longitude": lon,
            })


def plot_and_save(location, radius=5000):
    """
    Plot POIs on a map and save data to an ODS file.
    """
    lat, lon = map(float, location.split(','))
    for key, value in place_type.items():
        poi_tag = value[0].lower().replace(" ", "_")  # Convert to OSM-compatible tag
        print(f"Fetching data for {value[0]}...")
        osm_data = get_osm_data(lat, lon, radius, poi_tag)
        if osm_data:
            process_osm_data(osm_data, value)

    # Create a DataFrame
    poi_df = pd.DataFrame(poi_results)

    # Save the DataFrame to an ODS file
    output_path = '../refineData/osm_poi_rank_data.ods'
    poi_df.to_excel(output_path, engine='odf', index=False)
    print(f"Data saved to {output_path}")

    # Create a Folium map
    m = folium.Map(location=[lat, lon], zoom_start=13)

    # Add POIs to the map
    for _, row in poi_df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['POI Name']} ({row['POI Type']})",
            tooltip=row['POI Name']
        ).add_to(m)

    # Save the map as an HTML file
    map_output_path = '../templates/osm_poi_map.html'
    m.save(map_output_path)
    file_path = os.path.abspath(map_output_path)
    print(f"Map saved to {map_output_path}")


def main():
    location = "49.89517023418082, 10.885055540762723"  # Bamberg
    plot_and_save(location)


if __name__ == "__main__":
    main()
