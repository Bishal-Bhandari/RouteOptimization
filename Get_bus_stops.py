import re


def stop_time(transit_data, total_time):
    stops_info_dict = []
    if transit_data['line']['vehicle']['type'] == 'BUS':
        stops_info_dict.append({
            "num_stops": transit_data['num_stops']
        })
    # Use regular expression to find all integers in the string
    numbers = re.findall(r'\d+', total_time)
    # Convert the extracted numbers to integers
    time_in_travel = [int(num) for num in numbers]

    stops_time_info = (stops_info_dict[0].get('num_stops')*30)/60 + time_in_travel[0]
    stops_time_info = format(stops_time_info, ".2f")
    return stops_time_info
