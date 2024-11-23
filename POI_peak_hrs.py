import requests
import pandas as pd
import folium

# Define search parameters
location = [49.898813, 10.902763]  # Example: Bamberg, Germany
radius = 1000  # Radius in meters
poi_type = "amenity=restaurant"  # Example: Restaurants


# Step 1: Query Overpass API for POIs
def fetch_osm_pois(location, radius, poi_type):
    overpass_url = "https://overpass-api.de/api/interpreter"
    lat, lon = location
    query = f"""
    [out:json];
    (
      node[{poi_type}](around:{radius},{lat},{lon});
      way[{poi_type}](around:{radius},{lat},{lon});
      relation[{poi_type}](around:{radius},{lat},{lon});
    );
    out center;  // Get the center coordinates for ways and relations
    """
    response = requests.get(overpass_url, params={'data': query})
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()


# Step 2: Extract data from the Overpass response
def process_osm_data(data):
    pois = []
    for element in data['elements']:
        lat = element.get('lat') or element.get('center', {}).get('lat')
        lon = element.get('lon') or element.get('center', {}).get('lon')
        name = element.get('tags', {}).get('name', 'Unknown')
        pois.append({'Name': name, 'Latitude': lat, 'Longitude': lon})
    return pois


# Step 3: Save data to ODS format
def save_to_ods(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(f"{filename}.ods", index=False, engine="odf")


# Step 4: Display POIs on a Folium map
def display_pois_on_map(pois, location):
    m = folium.Map(location=location, zoom_start=15)
    for poi in pois:
        name = poi['Name']
        lat = poi['Latitude']
        lon = poi['Longitude']
        folium.Marker(location=[lat, lon], popup=name).add_to(m)
    return m


# Main workflow
def main():
    # Fetch POIs
    osm_data = fetch_osm_pois(location, radius, poi_type)
    pois = process_osm_data(osm_data)

    # Save POIs to an ODS file
    save_to_ods(pois, "osm_poi_data")

    # Display POIs on a Folium map
    map_ = display_pois_on_map(pois, location)
    map_.save("osm_poi_map.html")
    print("POI data saved as 'osm_poi_data.ods' and map saved as 'osm_poi_map.html'.")


if __name__ == "__main__":
    main()
