import os
import webbrowser

import folium
import json
import requests
import pandas as pd

# Place types dictionary
# key: ["POI", "Popularity Rank", "Similarity of POI Rank" ]
place_type = {
    1: "Train Stations", 2: "Shopping Centers", 4: "Airports", 5: "Schools", 6: "Universities",
    7: "Hospitals", 8: "Residential Areas", 9: "Tourist Attractions", 10: "Restaurants", 11: "Office Complexes",
    12: "Parks", 13: "Museums", 14: "Cinemas", 15: "Markets", 16: "Nightclubs", 17: "Sports Arenas", 18: "Hotels",
    19: "Temples", 20: "Churches", 21: "City Halls", 22: "Playgrounds", 23: "Cafes", 24: "Libraries",
    25: "Bus Depots", 26: "Parking Lots", 27: "Historical Sites", 28: "Monuments", 29: "Zoos", 30: "Art Galleries",
    31: "Convention Centers", 32: "Beaches", 33: "Harbors", 34: "Cemeteries", 35: "Casinos", 36: "Gyms",
    37: "Government Offices", 38: "Fire Stations", 39: "Police Stations", 40: "Prisons", 41: "Post Offices",
    42: "Stadiums", 43: "Amusement Parks", 44: "Bridges", 45: "Campgrounds", 46: "Embassies", 47: "Warehouses",
    48: "Theaters", 49: "Golf Courses",
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
        places_data = get_nearby_places(lat, lon, radius, value, api_key)
        if places_data and "results" in places_data:
            for place in places_data["results"]:
                poi_results.append({
                    "POI Name": place.get("name", "Unknown"),
                    "POI Type": value,
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
