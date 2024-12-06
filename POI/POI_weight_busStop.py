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
            # Place types ["POI", "Popularity Rank", "Similarity of POI Rank" ] Popularity Rank = 1 highest and 3 lowest
            # 1: Transportation/Infrastructure 2: Education/Learning 3: Health/Wellness 4: Religious/Spiritual
            # 5: Commerce/Business 6: Entertainment/Leisure 7: Food/Beverages 8: Environment/Recreation 9:
            # Public/Government Facilities
            ["library", 3, 2], ["biergarten", 2, 7], ["parking", 1, 1], ["restaurant", 1, 7],
            ["fuel", 1, 1], ["fountain", 2, 8], ["place_of_worship", 1, 4], ["school", 1, 2],
            ["bank", 1, 5], ["boat_rental", 2, 6], ["fast_food", 1, 7], ["taxi", 1, 1],
            ["post_office", 1, 9], ["pharmacy", 1, 3], ["doctors", 1, 3], ["vending_machine", 2, 5],
            ["pub", 1, 7], ["telephone", 2, 5], ["community_centre", 2, 9], ["cinema", 2, 6],
            ["atm", 1, 5], ["cafe", 1, 7], ["bicycle_parking", 1, 1], ["theatre", 2, 6],
            ["toilets", 1, 3], ["hunting_stand", 3, 8], ["fire_station", 1, 3], ["bts", 3, 1],
            ["driving_school", 2, 2], ["ice_cream", 2, 7], ["bar", 1, 7], ["drinking_water", 2, 8],
            ["waste_disposal", 2, 8], ["parcel_locker", 2, 9], ["ferry_terminal", 2, 1],
            ["parking_entrance", 3, 1], ["music_school", 2, 2], ["nightclub", 2, 7],
            ["car_sharing", 2, 1], ["university", 1, 2], ["stripclub", 3, 7],
            ["kindergarten", 1, 2], ["motorcycle_parking", 2, 1], ["swingerclub", 3, 7],
            ["kneipp_water_cure", 3, 3], ["brothel", 3, 7], ["clock", 3, 8], ["water_point", 2, 8],
            ["dentist", 1, 3], ["car_wash", 2, 1], ["car_rental", 2, 1], ["bbq", 3, 7],
            ["veterinary", 2, 3], ["studio", 2, 6], ["photo_booth", 3, 5],
            ["charging_station", 1, 1], ["childcare", 2, 2], ["social_facility", 2, 9],
            ["sanitary_dump_station", 3, 8], ["courthouse", 2, 9], ["bicycle_rental", 2, 1],
            ["public_bookcase", 3, 2], ["dancing_studio", 3, 2], ["marketplace", 1, 5],
            ["reception_desk", 3, 9], ["binoculars", 3, 8], ["hospital", 1, 3],
            ["trolley_bay", 3, 1], ["luggage_locker", 3, 1], ["academy", 2, 2],
            ["financial_advice", 2, 5], ["dojo", 3, 2], ["gambling", 3, 6], ["fraternity", 3, 9],
            ["internet_cafe", 2, 7], ["letter_box", 2, 9], ["locker", 3, 1], ["prep_school", 2, 2],
            ["college", 1, 2], ["townhall", 2, 9], ["bicycle_repair_station", 2, 1],
            ["monastery", 2, 4], ["clinic", 1, 3], ["hookah_lounge", 3, 7],
            ["vehicle_inspection", 2, 1], ["casino", 2, 6], ["lounger", 3, 7], ["shower", 2, 3],
            ["loading_dock", 3, 1], ["disused", 3, 9], ["training", 2, 2],
            ["language_school", 2, 2], ["dancing_school", 2, 2], ["motorcycle_rental", 2, 1],
            ["social_centre", 2, 9], ["fixme", 3, 9], ["compressed_air", 3, 1],
            ["vacuum_cleaner", 3, 1], ["smoking_area", 3, 8], ["ticket_validator", 2, 1],
            ["give_box", 3, 9], ["bus_station", 1, 1], ["post_depot", 2, 9],
            ["arts_centre", 2, 6], ["auditorium", 2, 6], ["archive", 2, 2], ["police", 1, 3],
            ["cargo", 2, 1], ["funeral_hall", 2, 9], ["animal_shelter", 2, 3],
            ["mortuary", 3, 9], ["public_building", 2, 9], ["dressing_room", 3, 6],
            ["weighbridge", 3, 1], ["prison", 3, 9], ["animal_training", 3, 8],
            ["events_venue", 2, 6], ["outdoor_seating", 3, 7], ["building_yard", 3, 1],
            ["waste_transfer_station", 3, 8], ["clothes_dryer", 3, 5], ["grassland", 3, 8]

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
