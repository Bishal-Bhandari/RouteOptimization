import folium
import json
import requests
import pandas as pd

# Load the API keys
with open('../api_keys.json') as json_file:
    api_keys = json.load(json_file)

# Google Maps API key
api_key = api_keys['Google_API']['API_key']

# Bamberg coordinates and radius
latitude = 49.8925
longitude = 10.8871
radius = 5000  # Radius in meters

# Place types dictionary
place_type = {
    1: "Train Stations", 2: "Shopping Centers", 3: "Bus Stops", 4: "Airports", 5: "Schools", 6: "Universities",
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
def get_nearby_places(lat, lng, radius, place_keyword):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
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

# Loop through place types
for key, value in place_type.items():
    places_data = get_nearby_places(latitude, longitude, radius, value)
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
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Add POIs to the map
for _, row in poi_df.iterrows():
    folium.Marker(
        location=[row["POI Latitude"], row["POI Longitude"]],
        popup=f"{row['POI Name']} ({row['POI Type']})",
        tooltip=row['POI Name']
    ).add_to(m)

# Save the map as an HTML file
map_output_path = '../refineData/bamberg_poi_map.html'
m.save(map_output_path)
print(f"Map saved to {map_output_path}")
