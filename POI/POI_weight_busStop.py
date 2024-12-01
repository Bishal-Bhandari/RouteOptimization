import requests
import pandas as pd
import folium

# Comprehensive list of POI types
poi_types = [
    "amenity=bus_station", "amenity=taxi", "amenity=car_rental", "railway=station", "aeroway=terminal",
    "highway=bus_stop",
    "amenity=school", "amenity=university", "amenity=library", "amenity=kindergarten",
    "amenity=hospital", "amenity=clinic", "amenity=pharmacy", "amenity=fire_station", "amenity=police",
    "amenity=place_of_worship", "historic=monument", "historic=castle", "tourism=museum",
    "shop=mall", "shop=supermarket", "shop=convenience", "amenity=marketplace",
    "leisure=cinema", "leisure=theatre", "leisure=sports_centre", "leisure=park",
    "amenity=restaurant", "amenity=cafe", "amenity=bar", "amenity=fast_food", "tourism=hotel",
    "leisure=garden", "leisure=playground", "leisure=dog_park", "amenity=bench",
    "amenity=post_office", "amenity=townhall", "amenity=embassy", "office=government",
    "shop=clothes", "shop=electronics", "shop=hardware", "amenity=bank", "amenity=atm",
    "sport=soccer", "sport=swimming", "leisure=golf_course", "natural=beach",
    "tourism=attraction", "tourism=camp_site", "tourism=theme_park", "historic=archaeological_site"
]


# Function to query Overpass API
def get_osm_pois(lat, lon, radius, poi_type):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node[{poi_type}](around:{radius},{lat},{lon});
      way[{poi_type}](around:{radius},{lat},{lon});
      relation[{poi_type}](around:{radius},{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.get(overpass_url, params={"data": overpass_query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying {poi_type}: {response.status_code}")
        return None


# Parse OSM data
def parse_osm_data(osm_data, poi_type):
    pois = []
    if "elements" in osm_data:
        for element in osm_data["elements"]:
            if "tags" in element:
                pois.append({
                    "name": element["tags"].get("name", "Unknown"),
                    "type": poi_type.split('=')[1],  # Extract type from query
                    "tags": ", ".join([f"{k}: {v}" for k, v in element["tags"].items()]),
                    "lat": element["lat"] if "lat" in element else None,
                    "lon": element["lon"] if "lon" in element else None,
                })
    return pois


# Save POIs to a CSV file
def save_to_csv(pois):
    pois_df = pd.DataFrame(pois)
    pois_df.to_csv("osm_pois_all_types.csv", index=False)
    print("POIs saved to osm_pois_all_types.csv")


# Plot POIs on a map
def plot_pois(lat, lon, pois):
    m = folium.Map(location=[lat, lon], zoom_start=13)
    for poi in pois:
        if poi["lat"] and poi["lon"]:
            folium.Marker(
                location=[poi["lat"], poi["lon"]],
                popup=f"{poi['name']} ({poi['type']})\nTags: {poi['tags']}",
                tooltip=poi["name"]
            ).add_to(m)
    m.save("osm_pois_map.html")
    print("Map saved as osm_pois_map.html")


# Main function
def main():
    # Location (latitude, longitude) and radius in meters
    location = (49.89517023418082, 10.885055540762723)  # Bamberg
    radius = 1000  # Radius in meters

    all_pois = []

    # Query each POI type
    for poi_type in poi_types:
        print(f"Querying {poi_type}...")
        osm_data = get_osm_pois(location[0], location[1], radius, poi_type)
        if osm_data:
            pois = parse_osm_data(osm_data, poi_type)
            all_pois.extend(pois)

    # Save to file
    save_to_csv(all_pois)

    # Plot on map
    plot_pois(location[0], location[1], all_pois)


if __name__ == "__main__":
    main()
