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


def parse_osm_data(osm_data):
    pois = []
    # Convert tag_dict to make lookup faster
    tag_dict = {
        value[0]: {"popularity_rank": value[1], "similarity_rank": value[2]}
        for value in [
            # Place types ["POI", "Popularity Rank", "Similarity of POI Rank" ] Popularity Rank = 1 highest and 5 lowest
            # 1: Transportation/Infrastructure 2: Education/Learning 3: Health/Wellness 4: Religious/Spiritual
            # 5: Commerce/Business 6: Entertainment/Leisure 7: Food/Beverages 8: Environment/Recreation 9:
            # Public/Government Facilities
            ["library", 3, 2], ["train_station", 1, 1], ["museum", 4, 2], ["biergarten", 2, 7], ["parking", 6, 1],
            ["restaurant", 2, 7],
            ["fuel", 7, 1], ["fountain", 7, 8], ["place_of_worship", 4, 4], ["school", 3, 2],
            ["bank", 5, 5], ["boat_rental", 5, 6], ["fast_food", 2, 7], ["taxi", 7, 1],
            ["post_office", 5, 9], ["pharmacy", 3, 3], ["doctors", 7, 3], ["vending_machine", 7, 5],
            ["pub", 5, 7], ["telephone", 6, 5], ["community_centre", 3, 9], ["cinema", 4, 6],
            ["atm", 5, 5], ["cafe", 2, 7], ["bicycle_parking", 7, 1], ["theatre", 4, 6],
            ["toilets", 7, 3], ["hunting_stand", 5, 8], ["fire_station", 6, 3],
            ["driving_school", 5, 2], ["ice_cream", 5, 7], ["bar", 5, 7], ["drinking_water", 8, 8],
            ["waste_disposal", 9, 8], ["parcel_locker", 8, 9], ["ferry_terminal", 7, 1],
            ["parking_entrance", 6, 1], ["music_school", 4, 2], ["nightclub", 5, 7],
            ["car_sharing", 7, 1], ["university", 3, 2], ["stripclub", 8, 7],
            ["kindergarten", 6, 2], ["motorcycle_parking", 7, 1], ["swingerclub", 10, 7],
            ["kneipp_water_cure", 10, 3], ["clock", 9, 8], ["water_point", 9, 8],
            ["dentist", 7, 3], ["car_wash", 5, 1], ["car_rental", 8, 1], ["bbq", 3, 7],
            ["veterinary", 5, 3], ["studio", 8, 6], ["photo_booth", 10, 5],
            ["charging_station", 5, 1], ["childcare", 6, 2], ["social_facility", 8, 9],
            ["sanitary_dump_station", 9, 8], ["courthouse", 3, 9], ["bicycle_rental", 8, 1],
            ["public_bookcase", 9, 2], ["shopping_mall", 2, 5], ["dancing_studio", 3, 2], ["marketplace", 4, 5],
            ["reception_desk", 3, 9], ["binoculars", 9, 8], ["hospital", 3, 3],
            ["trolley_bay", 8, 1], ["luggage_locker", 3, 1], ["academy", 9, 2],
            ["financial_advice", 9, 5], ["dojo", 9, 2], ["gambling", 3, 6], ["fraternity", 9, 9],
            ["internet_cafe", 9, 7], ["letter_box", 2, 9], ["locker", 8, 1], ["prep_school", 2, 2],
            ["college", 1, 2], ["townhall", 2, 9], ["bicycle_repair_station", 2, 1],
            ["monastery", 2, 4], ["clinic", 1, 3], ["hookah_lounge", 9, 7],
            ["vehicle_inspection", 2, 1], ["casino", 2, 6], ["lounger", 7, 7], ["shower", 2, 3],
            ["loading_dock", 9, 1], ["disused", 9, 9], ["training", 9, 2],
            ["language_school", 2, 2], ["dancing_school", 2, 2], ["motorcycle_rental", 2, 1],
            ["social_centre", 2, 9], ["fixme", 9, 9],
            ["vacuum_cleaner", 10, 1], ["smoking_area", 3, 8], ["ticket_validator", 2, 1],
            ["give_box", 9, 9], ["bus_station", 1, 1], ["post_depot", 2, 9],
            ["arts_centre", 2, 6], ["auditorium", 2, 6], ["archive", 8, 2], ["police", 3, 3],
            ["cargo", 2, 1], ["funeral_hall", 8, 9], ["animal_shelter", 8, 3],
            ["mortuary", 9, 9], ["public_building", 2, 9], ["dressing_room", 8, 6],
            ["weighbridge", 9, 1], ["prison", 3, 9], ["animal_training", 10, 8],
            ["events_venue", 9, 6], ["outdoor_seating", 3, 7], ["building_yard", 9, 1],
            ["waste_transfer_station", 9, 8], ["clothes_dryer", 10, 5], ["grassland", 6, 8]

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
        pois = parse_osm_data(osm_data)
        save_and_plot_pois(location[0], location[1], pois)


if __name__ == "__main__":
    main()
