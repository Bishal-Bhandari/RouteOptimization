import os
import webbrowser

import requests
import folium
import pandas as pd


# Function to query Overpass API
def get_osm_pois(lat, lon, radius, poi_type):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["{poi_type}"](around:{radius},{lat},{lon})["amenity"!="bench"]["amenity"!="post_box"]
      ["amenity"!="waste_basket"]["amenity"!="waste_bin"]["amenity"!="recycling"]["amenity"!="grit_bin"]
      ["amenity"!="parking_space"];
      way["{poi_type}"](around:{radius},{lat},{lon})["amenity"!="bench"]["amenity"!="post_box"]
      ["amenity"!="waste_basket"]["amenity"!="waste_bin"]["amenity"!="recycling"]["amenity"!="grit_bin"]
      ["amenity"!="parking_space"];
      relation["{poi_type}"](around:{radius},{lat},{lon})["amenity"!="bench"]["amenity"!="post_box"]
      ["amenity"!="waste_basket"]["amenity"!="waste_bin"]["amenity"!="recycling"]["amenity"!="grit_bin"]
      ["amenity"!="parking_space"];
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.get(overpass_url, params={"data": overpass_query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


# Parse and save POIs
def parse_osm_data(osm_data):
    pois = []
    if "elements" in osm_data:
        for element in osm_data["elements"]:
            if "tags" in element:
                pois.append({
                    "name": element["tags"].get("name", "Unknown"),
                    "type": element["tags"].get("amenity", "Unknown"),
                    "lat": element["lat"] if "lat" in element else None,
                    "lon": element["lon"] if "lon" in element else None,
                })
    return pois


# Save POIs to ODS and plot on a map
def save_and_plot_pois(lat, lon, pois):
    # Convert POIs to DataFrame
    pois_df = pd.DataFrame(pois)

    # Save to ODS file
    output_path = "../refineData/osm_poi_rank_data.ods"
    pois_df.to_excel(output_path, engine="odf", index=False)
    print(f"POIs saved to {output_path}")

    # Plot on a map
    m = folium.Map(location=[lat, lon], zoom_start=13)
    for poi in pois:
        if poi["lat"] and poi["lon"]:
            folium.Marker(
                location=[poi["lat"], poi["lon"]],
                popup=f"{poi['name']} ({poi['type']})",
                tooltip=poi["type"]
            ).add_to(m)
    map_file = "../templates/osm_pois_rank_map.html"
    m.save(map_file)
    # Open the map
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")


# Main
def main():
    global osm_data
    location = (49.89517023418082, 10.885055540762723)  # Bamberg
    radius = 10000  # Radius in meters
    poi_type = {
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
    for key, value in poi_type.items():
        # Query OSM
        osm_data = get_osm_pois(location[0], location[1], radius, value[0])

    if osm_data:
        pois = parse_osm_data(osm_data)
        save_and_plot_pois(location[0], location[1], pois)


if __name__ == "__main__":
    main()
