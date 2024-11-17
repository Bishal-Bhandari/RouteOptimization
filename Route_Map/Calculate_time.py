import re


class CalcTime:
    def __init__(self, transit_details, duration):
        self.transit_details = transit_details
        self.duration = duration

    def stop_time(self):
        stops_info_dict = []
        if self.transit_details['line']['vehicle']['type'] == 'BUS':
            stops_info_dict.append({
                "num_stops": self.transit_details['num_stops']
            })
        # Use regular expression to find all integers in the string
        numbers = re.findall(r'\d+', self.duration)
        # Convert the extracted numbers to integers
        time_in_travel = [int(num) for num in numbers]
        print(time_in_travel)
        stops_time_info = (stops_info_dict[0].get('num_stops') * 30) / 60 + time_in_travel[0]

        stops_time_info = format(stops_time_info, ".2f")
        return stops_time_info
