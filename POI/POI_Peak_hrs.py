def time_peak():
    # Morning Peak (6 AM - 10 AM)
    morning_peak = [
        "bus_station", "train_station", "bicycle_rental", "taxi", "car_rental", "motorcycle_rental",
        "school", "university", "kindergarten", "college", "prep_school", "music_school",
        "language_school", "dancing_school", "academy", "dojo", "post_office",
        "financial_advice", "courthouse", "reception_desk", "cafe", "fuel"
    ]

    # Midday Peak (11 AM - 2 PM)
    midday_peak = [
        "restaurant", "cafe", "fast_food", "biergarten", "ice_cream", "pub", "bbq",
        "shopping_mall", "marketplace", "vending_machine", "post_office", "letter_box",
        "clinic", "pharmacy", "dentist", "hospital", "community_centre", "social_facility"
    ]

    # Afternoon Peak (3 PM - 6 PM)
    afternoon_peak = [
        "school", "university", "dancing_studio", "driving_school", "music_school",
        "bus_station", "parking", "taxi", "bicycle_parking", "car_sharing",
        "cinema", "theatre", "arts_centre", "events_venue", "museum",
        "pharmacy", "post_office"
    ]

    # Evening Peak (6 PM - 9 PM)
    evening_peak = [
        "restaurant", "fast_food", "bbq", "biergarten", "cafe",
        "bar", "pub", "nightclub", "stripclub", "hookah_lounge",
        "swingerclub",
        "cinema", "theatre", "arts_centre", "casino", "auditorium",
        "community_centre", "social_centre", "taxi", "bus_station"
    ]

    # Night Hours (9 PM - 12 AM)
    night_hours = [
        "bar", "nightclub", "stripclub", "swingerclub",
        "bus_station", "taxi", "car_rental", "hospital", "police",
        "fire_station", "vending_machine", "fuel"
    ]

    # Low Activity Hours (12 AM - 6 AM)
    low_activity = [
        "hospital", "police", "fire_station",
        "bus_station", "taxi", "fuel", "parking", "car_sharing"
    ]

    # Flexible Peak Hours (All Day Activity)
    flexible_hours = [
        "hospital", "clinic", "pharmacy", "parking", "bus_station",
        "train_station", "vending_machine", "fuel"
    ]
 time_peak()