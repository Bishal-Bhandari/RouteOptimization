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


def categories(tags):
    # Place types dictionary key: ["POI", "Popularity Rank", "Similarity of POI Rank" ] Popularity Rank = 1 highest
    # and 5 lowest 1: Transportation/Infrastructure 2: Education/Learning 3: Health/Wellness 4: Religious/Spiritual
    # 5: Commerce/Business 6: Entertainment/Leisure 7: Food/Beverages8: Environment/Recreation 9: Public/Government
    # Facilities
    tag_dict = {1: ["library", 3, 2], 2: ["biergarten", 2, 7], 3: ["parking", 1, 1], 4: ["restaurant", 1, 7],
                5: ["fuel", 1, 1], 6: ["fountain", 2, 8], 7: ["place_of_worship", 1, 4], 8: ["school", 1, 2],
                9: ["bank", 1, 5], 10: ["boat_rental", 2, 6], 11: ["fast_food", 1, 7], 12: ["taxi", 1, 1],
                13: ["post_office", 1, 9], 14: ["pharmacy", 1, 3], 15: ["doctors", 1, 3], 16: ["vending_machine", 2, 5],
                17: ["pub", 1, 7], 18: ["telephone", 2, 5], 19: ["community_centre", 2, 9], 20: ["cinema", 2, 6],
                21: ["atm", 1, 5], 22: ["cafe", 1, 7], 23: ["bicycle_parking", 1, 1], 24: ["theatre", 2, 6],
                25: ["toilets", 1, 3], 26: ["hunting_stand", 3, 8], 27: ["fire_station", 1, 3], 28: ["bts", 3, 1],
                29: ["driving_school", 2, 2], 30: ["ice_cream", 2, 7], 31: ["bar", 1, 7], 32: ["drinking_water", 2, 8],
                33: ["waste_disposal", 2, 8], 34: ["parcel_locker", 2, 9], 35: ["ferry_terminal", 2, 1],
                36: ["parking_entrance", 3, 1], 37: ["music_school", 2, 2], 38: ["nightclub", 2, 7],
                39: ["car_sharing", 2, 1], 40: ["university", 1, 2], 41: ["stripclub", 3, 7],
                42: ["kindergarten", 1, 2], 43: ["motorcycle_parking", 2, 1], 44: ["swingerclub", 3, 7],
                45: ["kneipp_water_cure", 3, 3], 46: ["brothel", 3, 7], 47: ["clock", 3, 8], 48: ["water_point", 2, 8],
                49: ["dentist", 1, 3], 50: ["car_wash", 2, 1], 51: ["car_rental", 2, 1], 52: ["bbq", 3, 7],
                53: ["veterinary", 2, 3], 54: ["studio", 2, 6], 55: ["photo_booth", 3, 5],
                56: ["charging_station", 1, 1], 57: ["childcare", 2, 2], 58: ["social_facility", 2, 9],
                59: ["sanitary_dump_station", 3, 8], 60: ["courthouse", 2, 9], 61: ["bicycle_rental", 2, 1],
                62: ["public_bookcase", 3, 2], 63: ["dancing_studio", 3, 2], 64: ["marketplace", 1, 5],
                65: ["reception_desk", 3, 9], 66: ["binoculars", 3, 8], 67: ["hospital", 1, 3],
                68: ["trolley_bay", 3, 1], 69: ["luggage_locker", 3, 1], 70: ["academy", 2, 2],
                71: ["financial_advice", 2, 5], 72: ["dojo", 3, 2], 73: ["gambling", 3, 6], 74: ["fraternity", 3, 9],
                75: ["internet_cafe", 2, 7], 76: ["letter_box", 2, 9], 77: ["locker", 3, 1], 78: ["prep_school", 2, 2],
                79: ["college", 1, 2], 80: ["townhall", 2, 9], 81: ["bicycle_repair_station", 2, 1],
                82: ["monastery", 2, 4], 83: ["clinic", 1, 3], 84: ["hookah_lounge", 3, 7],
                85: ["vehicle_inspection", 2, 1], 86: ["casino", 2, 6], 87: ["lounger", 3, 7], 88: ["shower", 2, 3],
                89: ["loading_dock", 3, 1], 90: ["disused", 3, 9], 91: ["training", 2, 2],
                92: ["language_school", 2, 2], 93: ["dancing_school", 2, 2], 94: ["motorcycle_rental", 2, 1],
                95: ["social_centre", 2, 9], 96: ["fixme", 3, 9], 97: ["compressed_air", 3, 1],
                98: ["vacuum_cleaner", 3, 1], 99: ["smoking_area", 3, 8], 100: ["ticket_validator", 2, 1],
                101: ["give_box", 3, 9], 102: ["bus_station", 1, 1], 103: ["post_depot", 2, 9],
                104: ["arts_centre", 2, 6], 105: ["auditorium", 2, 6], 106: ["archive", 2, 2], 107: ["police", 1, 3],
                108: ["cargo", 2, 1], 109: ["funeral_hall", 2, 9], 110: ["animal_shelter", 2, 3],
                111: ["mortuary", 3, 9], 112: ["public_building", 2, 9], 113: ["dressing_room", 3, 6],
                114: ["weighbridge", 3, 1], 115: ["prison", 3, 9], 116: ["animal_training", 3, 8],
                117: ["events_venue", 2, 6], 118: ["outdoor_seating", 3, 7], 119: ["building_yard", 3, 1],
                120: ["waste_transfer_station", 3, 8], 121: ["clothes_dryer", 3, 5], 122: ["grassland", 3, 8]}


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
        pois = parse_osm_data(osm_data)
        save_and_plot_pois(location[0], location[1], pois)


if __name__ == "__main__":
    main()
