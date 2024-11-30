import os
import webbrowser

import folium
import json
import requests
import pandas as pd

# Place types dictionary
# key: ["POI", "Popularity Rank", "Similarity of POI Rank" ]
# Popularity Rank = 1 highest and 5 lowest
# Similarity of POI Rank= Transportation and Infrastructure:1, Education and Knowledge:2,
# Healthcare and Emergency Services:3, Religious and Cultural Sites:4, Commercial Centers:5, Entertainment:6,
# Dining and Hospitality:7, Public Spaces:8, Administrative Buildings:9
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


# Search POIs
def get_nearby_places(lat, lon, radius, place_keyword, api_key):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "keyword": place_keyword,
        "key": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def plot_and_save(api_key, location, radius=5000):
    # Parse location
    lat, lon = map(float, location.split(','))
    # Loop through place types
    for key, value in place_type.items():
        places_data = get_nearby_places(lat, lon, radius, value[0], api_key)
        if places_data and "results" in places_data:
            for place in places_data["results"]:
                poi_results.append({
                    "POI Name": place.get("name", "Unknown"),
                    "POI Type": value[0],
                    "POI Popularity": value[1],
                    "POI Similarity": value[2],
                    "POI Rank": key,
                    "POI Latitude": place["geometry"]["location"]["lat"],
                    "POI Longitude": place["geometry"]["location"]["lng"],
                    "POI Address": place.get("vicinity", "Unknown"),
                })

    # Results into a DataFrame
    poi_df = pd.DataFrame(poi_results)

    # Save the DataFrame to an ODS file
    output_path = '../refineData/bamberg_poi_rank_data.ods'
    poi_df.to_excel(output_path, engine='odf', index=False)
    print(f"Data saved to {output_path}")

    # Create a Folium map
    m = folium.Map(location=[lat, lon], zoom_start=13)

    # Add POIs to the map
    for _, row in poi_df.iterrows():
        folium.Marker(
            location=[row["POI Latitude"], row["POI Longitude"]],
            popup=f"{row['POI Name']} ({row['POI Type']})",
            tooltip=row['POI Name']
        ).add_to(m)

    # Save the map as an HTML file
    map_output_path = '../templates/bamberg_poi_map.html'
    m.save(map_output_path)
    file_path = os.path.abspath(map_output_path)
    webbrowser.open(f"file://{file_path}")


def main():
    # Load the API keys from the JSON file
    with open('../api_keys.json') as json_file:
        api_keys = json.load(json_file)

    # Google Maps API key
    api_key = api_keys['Google_API']['API_key']
    location = "49.89517023418082, 10.885055540762723"  # Bamberg
    plot_and_save(api_key, location)


if __name__ == "__main__":
    main()
