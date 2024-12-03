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
      ["amenity"!="parking_space"]["amenity"!="shelter"];
      way["{poi_type}"](around:{radius},{lat},{lon})["amenity"!="bench"]["amenity"!="post_box"]
      ["amenity"!="waste_basket"]["amenity"!="waste_bin"]["amenity"!="recycling"]["amenity"!="grit_bin"]
      ["amenity"!="parking_space"]["amenity"!="shelter"];
      relation["{poi_type}"](around:{radius},{lat},{lon})["amenity"!="bench"]["amenity"!="post_box"]
      ["amenity"!="waste_basket"]["amenity"!="waste_bin"]["amenity"!="recycling"]["amenity"!="grit_bin"]
      ["amenity"!="parking_space"]["amenity"!="shelter"];
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


def classify_place(tags):
    categories = {
        "Education": ["school", "university", "college"],
        "Transport": ["bus_stop", "train_station", "airport"],
        "Healthcare": ["hospital", "clinic", "pharmacy"],
        "Leisure": ["park", "cinema", "stadium"],
        "Shopping": ["mall", "supermarket", "shop"],
        "Food & Drink": ["restaurant", "cafe", "bar"],
        "Tourism": ["museum", "hotel", "attraction"],
        "Residential": ["apartments", "residential"],
    }

    for category, keywords in categories.items():
        for key, value in tags.items():
            if value in keywords or key in keywords:
                return category
    return "Other"


# Example usage:
def parse_and_classify_osm_data(osm_data):
    pois = []
    if "elements" in osm_data:
        for element in osm_data["elements"]:
            if "tags" in element:
                category = classify_place(element["tags"])
                pois.append({
                    "name": element["tags"].get("name", "Unknown"),
                    "type": category,
                    "lat": element.get("lat"),
                    "lon": element.get("lon"),
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
                tooltip=poi["name"]
            ).add_to(m)
    map_file = "../templates/osm_pois_rank_map.html"
    m.save(map_file)
    # Open the map
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")


# Main
def main():
    location = (49.89517023418082, 10.885055540762723)  # Bamberg
    radius = 10000  # Radius in meters
    poi_type = "amenity"  # Search for amenities; customize as needed

    # Query OSM
    osm_data = get_osm_pois(location[0], location[1], radius, poi_type)
    if osm_data:
        pois = parse_and_classify_osm_data(osm_data)
        save_and_plot_pois(location[0], location[1], pois)


if __name__ == "__main__":
    main()
