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
      node["railway"="station"](around:{radius},{lat},{lon});
      way["railway"="station"](around:{radius},{lat},{lon});
      relation["railway"="station"](around:{radius},{lat},{lon});
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


def parse_osm_data(osm_data):
    pois = []
    # Convert tag_dict to make lookup faster
    tag_dict = {
        value[0]: {"popularity_rank": value[1], "similarity_rank": value[2]}
        for value in [
            # ["POI", "Popularity Rank", "Similarity of POI Rank" ] Popularity Rank = 10 highest and 1 lowest
            # 1: Transportation/Infrastructure 2: Education/Learning 3: Health/Wellness 4: Religious/Spiritual
            # 5: Commerce/Business 6: Entertainment/Leisure 7: Food/Beverages 8: Environment/Recreation 9:
            # Public/Government Facilities
            ["library", 8, 2], ["train_station", 10, 1], ["station", 10, 1], ["museum", 7, 2], ["biergarten", 9, 7], ["parking", 5, 1],
            ["restaurant", 9, 7], ["fuel", 4, 1], ["fountain", 4, 8], ["place_of_worship", 7, 4], ["school", 8, 2],
            ["bank", 6, 5], ["boat_rental", 6, 6], ["fast_food", 9, 7], ["taxi", 4, 1],
            ["post_office", 6, 9], ["pharmacy", 8, 3], ["doctors", 4, 3], ["vending_machine", 4, 5],
            ["pub", 6, 7], ["telephone", 5, 5], ["community_centre", 8, 9], ["cinema", 7, 6],
            ["atm", 6, 5], ["cafe", 9, 7], ["bicycle_parking", 4, 1], ["theatre", 7, 6],
            ["toilets", 4, 3], ["hunting_stand", 6, 8], ["fire_station", 5, 3],
            ["driving_school", 6, 2], ["ice_cream", 6, 7], ["bar", 6, 7], ["drinking_water", 3, 8],
            ["waste_disposal", 2, 8], ["parcel_locker", 3, 9], ["ferry_terminal", 4, 1],
            ["parking_entrance", 5, 1], ["music_school", 7, 2], ["nightclub", 6, 7],
            ["car_sharing", 4, 1], ["university", 8, 2], ["stripclub", 3, 7], ["brothel", 3, 6],
            ["kindergarten", 5, 2], ["motorcycle_parking", 4, 1], ["swingerclub", 1, 7],
            ["kneipp_water_cure", 1, 3], ["clock", 2, 8], ["water_point", 2, 8],
            ["dentist", 4, 3], ["car_wash", 6, 1], ["car_rental", 3, 1], ["bbq", 8, 7],
            ["veterinary", 6, 3], ["studio", 3, 6], ["photo_booth", 1, 5],
            ["charging_station", 6, 1], ["childcare", 5, 2], ["social_facility", 3, 9],
            ["sanitary_dump_station", 2, 8], ["courthouse", 8, 9], ["bicycle_rental", 3, 1],
            ["public_bookcase", 2, 2], ["shopping_mall", 9, 5], ["dancing_studio", 8, 2], ["marketplace", 7, 5],
            ["reception_desk", 8, 9], ["binoculars", 2, 8], ["hospital", 8, 3],
            ["trolley_bay", 3, 1], ["luggage_locker", 8, 1], ["academy", 2, 2],
            ["financial_advice", 2, 5], ["dojo", 2, 2], ["gambling", 8, 6], ["fraternity", 2, 9],
            ["internet_cafe", 2, 7], ["letter_box", 9, 9], ["locker", 3, 1], ["prep_school", 9, 2],
            ["college", 10, 2], ["townhall", 9, 9], ["bicycle_repair_station", 9, 1],
            ["monastery", 9, 4], ["clinic", 10, 3], ["hookah_lounge", 2, 7],
            ["vehicle_inspection", 9, 1], ["casino", 9, 6], ["lounger", 4, 7], ["shower", 9, 3],
            ["loading_dock", 2, 1], ["disused", 2, 9], ["training", 2, 2],
            ["language_school", 9, 2], ["dancing_school", 9, 2], ["motorcycle_rental", 9, 1],
            ["social_centre", 9, 9], ["fixme", 2, 9],
            ["vacuum_cleaner", 1, 1], ["smoking_area", 8, 8], ["ticket_validator", 9, 1],
            ["give_box", 2, 9], ["bus_station", 10, 1], ["post_depot", 9, 9],
            ["arts_centre", 9, 6], ["auditorium", 9, 6], ["archive", 3, 2], ["police", 8, 3],
            ["cargo", 9, 1], ["funeral_hall", 3, 9], ["animal_shelter", 3, 3],
            ["mortuary", 2, 9], ["public_building", 9, 9], ["dressing_room", 3, 6],
            ["weighbridge", 2, 1], ["prison", 8, 9], ["animal_training", 1, 8],
            ["events_venue", 2, 6], ["outdoor_seating", 8, 7], ["building_yard", 2, 1],
            ["waste_transfer_station", 2, 8], ["clothes_dryer", 1, 5], ["grassland", 5, 8]
        ]
    }

    if "elements" in osm_data:
        for element in osm_data["elements"]:
            if "tags" in element:
                poi_type = element["tags"].get("amenity", "Unknown")
                rank_data = tag_dict.get(poi_type, {"popularity_rank": "Unknown", "similarity_rank": "Unknown"})
                pois.append({
                    "name": element["tags"].get("name", poi_type),
                    "type": poi_type,
                    "lat": element.get("lat"),
                    "lon": element.get("lon"),
                    "popularity_rank": rank_data["popularity_rank"],
                    "similarity_rank": rank_data["similarity_rank"],
                })
    return pois


# Update the `save_and_plot_pois` function to handle the new columns
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
                popup=f"{poi['name']} ({poi['type']}) - Rank: {poi['popularity_rank']}, Similarity: {poi['similarity_rank']}",
                tooltip=poi["name"] if poi["name"] else poi["type"]
            ).add_to(m)

    # To display information section
    table_html = f"""
    <div style="position: fixed; 
                top: 0px; right: 10px; 
                width: 290px; 
                height: auto; 
                padding: 10px; 
                background-color: white; <
                border: 2px solid black; 
                z-index: 9999; 
                overflow-y: auto;">
        <h4 style="border: 1px solid black; padding: 5px;">Information</h4>
        <table style="width: 100%; border-collapse: collapse;">
        <tr>
                <th style="border: 1px solid black; padding: 5px;">Popularity Rank</th>
                <th style="border: 1px solid black; padding: 5px;">Popularity</th>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">1</td>
                <td style="border: 1px solid black; padding: 5px;">Low</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">10</td>
                <td style="border: 1px solid black; padding: 5px;">High</td>
            </tr>
            <tr>
                <th style="border: 1px solid black; padding: 5px;">Similarity Rank</th>
                <th style="border: 1px solid black; padding: 5px;">Group</th>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">1</td>
                <td style="border: 1px solid black; padding: 5px;">Transportation/Infrastructure</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">2</td>
                <td style="border: 1px solid black; padding: 5px;">Education/Learning</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">3</td>
                <td style="border: 1px solid black; padding: 5px;">Health/Wellness</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">4</td>
                <td style="border: 1px solid black; padding: 5px;">Religious/Spiritual</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">5</td>
                <td style="border: 1px solid black; padding: 5px;">Commerce/Business</td>
            </tr>
                        <tr>
                <td style="border: 1px solid black; padding: 5px;">6</td>
                <td style="border: 1px solid black; padding: 5px;">Entertainment/Leisure</td>
            </tr>
                        <tr>
                <td style="border: 1px solid black; padding: 5px;">7</td>
                <td style="border: 1px solid black; padding: 5px;">Food/Beverages</td>
            </tr>
                        <tr>
                <td style="border: 1px solid black; padding: 5px;">8</td>
                <td style="border: 1px solid black; padding: 5px;">Environment/Recreation</td>
            </tr>
                        <tr>
                <td style="border: 1px solid black; padding: 5px;">9</td>
                <td style="border: 1px solid black; padding: 5px;">Public/Government Facilities</td>
            </tr>
        </table>
    </div>
    """

    # Add the HTML table as a folium.Element
    table_element = folium.Element(table_html)
    m.get_root().html.add_child(table_element)

    map_file = "../templates/osm_pois_rank_map.html"
    m.save(map_file)
    # Open the map
    file_path = os.path.abspath(map_file)
    webbrowser.open(f"file://{file_path}")


# Main
def main():
    location = (49.89517023418082, 10.885055540762723)  # Bamberg
    radius = 5000  # Radius in meters
    poi_type = "amenity"  # Search for amenities; customize as needed

    # Query OSM
    osm_data = get_osm_pois(location[0], location[1], radius, poi_type)
    if osm_data:
        pois = parse_osm_data(osm_data)
        save_and_plot_pois(location[0], location[1], pois)


if __name__ == "__main__":
    main()
