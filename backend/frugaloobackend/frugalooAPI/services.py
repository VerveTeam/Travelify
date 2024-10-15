import json
import math
import requests
from itertools import combinations
from math import radians, cos, sin, sqrt, atan2

def extract_lat_long(data):
    """
    Extracts latitude and longitude values from the provided data.

    Parameters:
    - data: Dictionary containing trip details with places and their lat/long

    Returns:
    - List of dictionaries containing day index, place name, and lat/long
    """
    lat_long_values = []

    for day_index, day in data.items():
        for group in day:  # Loop through the list of lists
            for place in group:  # Loop through each place in the group
                lat_long_values.append(
                    {
                        "day_index": day_index,
                        "place_name": place["place_name"],
                        "lat_long": place["lat_long"],
                    }
                )
    return lat_long_values


def fetch_nearby_restaurants(lat_long_values, budget, grouped_attractions):
    """
    Fetches nearby restaurants for given latitude and longitude values, and updates grouped attractions.

    Parameters:
    - lat_long_values: List of dictionaries containing lat/long values for each place.
    - budget: Budget type for filtering restaurants (1: frugal, 2: moderate, 3: expensive).
    - grouped_attractions: Dictionary containing the grouped attractions for each day.

    Returns:
    - Updated grouped_attractions with separate objects for places and restaurants.
    """
    api_key = ""  # Your API key here
    radius = 1500
    budget_mapping = {
        1: {0, 1},  # Frugal: price_level 0 or 1
        2: {2, 3},  # Moderate: price_level 2 or 3
        3: {4},     # Expensive: price_level 4
    }

    # Debug: Print lat_long_values to check its structure
    print("Lat/Long Values:", lat_long_values)

    # Iterate over lat_long_values to process each place
    for place in lat_long_values:
        day_index = place.get("day_index")  # Use .get() to prevent KeyError
        place_name = place.get("place_name")  # Use .get() to prevent KeyError
        lat_long = place.get("lat_long")  # Use .get() to prevent KeyError

        # Debug: Print each place's details
        print("Processing Place:", {"day_index": day_index, "place_name": place_name, "lat_long": lat_long})

        if not place_name or not lat_long:
            print("Error: Missing 'place_name' or 'lat_long' in place:", place)
            continue  # Skip this iteration if data is missing

        lat, lng = lat_long.split(",")

        # Prepare the API request (commented out for testing)
        '''url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=restaurant&key={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            restaurants = [
                {
                    "name": result["name"],
                    "latitude": result["geometry"]["location"]["lat"],
                    "longitude": result["geometry"]["location"]["lng"],
                    "rating": result.get("rating", "N/A"),
                    "price_level": result.get("price_level", "N/A"),
                }
                for result in data["results"]
                if "price_level" in result and result["price_level"] in budget_mapping[budget]
            ]

            if not restaurants:
                restaurants = [
                    {
                        "name": result["name"],
                        "latitude": result["geometry"]["location"]["lat"],
                        "longitude": result["geometry"]["location"]["lng"],
                        "rating": result.get("rating", "N/A"),
                        "price_level": result.get("price_level", "N/A"),
                    }
                    for result in data["results"]
                    if result.get("price_level") is None
                ]'''
        
    # Hardcoded restaurant data for testing
    restaurants = [{'name': 'Delhi Darbar', 'latitude': 18.9238178, 'longitude': 72.8317462, 'rating': 4, 'price_level': 2}, {'name': 'Flavors Cafe at The Ambassador', 'latitude': 18.9338036, 'longitude': 72.82486999999999, 'rating': 4.1, 'price_level': 3}, {'name': 'Bademiya', 'latitude': 18.9232359, 'longitude': 72.83252259999999, 'rating': 3.7, 'price_level': 2}, {'name': 'Woodside Inn', 'latitude': 18.9248583, 'longitude': 72.8318556, 'rating': 4.5, 'price_level': 2}, {'name': '5 Spice', 'latitude': 18.9334885, 'longitude': 72.8357669, 'rating': 3.8, 'price_level': 2}, {'name': 'Subway', 'latitude': 18.938368, 'longitude': 72.8330572, 'rating': 4, 'price_level': 2}, {'name': 'Royal China', 'latitude': 18.9384896, 'longitude': 72.8328156, 'rating': 4.4, 'price_level': 3}, {'name': 'Amrapali Bar and Restaurant & Bar', 'latitude': 18.9302832, 'longitude': 72.831695, 'rating': 3.9, 'price_level': 2}, {'name': 'The J', 'latitude': 18.930182, 'longitude': 72.82675979999999, 'rating': 4.2, 'price_level': 2}, {'name': 'Hotel Fountain Plaza', 'latitude': 18.9354321, 'longitude': 72.8347235, 'rating': 4.1, 'price_level': 2}, {'name': 'Leopold Cafe', 'latitude': 18.9226402, 'longitude': 72.8316401, 'rating': 4.2, 'price_level': 3}]
    return restaurants

def merge_restaurants_places(grouped_attractions, restaurants):
    # Track assigned restaurants to avoid duplicates
    assigned_restaurants = set()

    for group_key, places_list in grouped_attractions.items():
        # Flatten the list of places if it's nested within another list
        places = places_list[0] if isinstance(places_list[0], list) else places_list
        
        for i, place in enumerate(places):
            if 'place_name' in place:
                place_lat, place_lon = map(float, place['lat_long'].split(", "))
                closest_restaurant = None
                min_distance = float('inf')

                # Find the closest available restaurant
                for restaurant in restaurants:
                    if restaurant['name'] not in assigned_restaurants:
                        rest_lat, rest_lon = restaurant['latitude'], restaurant['longitude']
                        distance = haversine(place_lat, place_lon, rest_lat, rest_lon)
                        
                        if distance < min_distance:
                            min_distance = distance
                            closest_restaurant = restaurant

                # If a restaurant is found, insert it after the place
                if closest_restaurant:
                    assigned_restaurants.add(closest_restaurant['name'])  # Mark restaurant as assigned
                    places.insert(i + 1, {
                        'restaurant_name': closest_restaurant['name'],
                        'lat_long': f"{closest_restaurant['latitude']}, {closest_restaurant['longitude']}"
                    })
    
     # Convert the dictionary to a valid JSON string
    json_result = json.dumps(grouped_attractions, indent=4)
    return json_result



def haversine(lat1, lon1, lat2, lon2):
    """Calculate the distance between two lat/long pairs using the Haversine formula."""
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_closest_groups(attractions, num_days):
    def distance(p1, p2):
        return haversine(p1['latitude'], p1['longitude'], p2['latitude'], p2['longitude'])
    
    # List to hold the final result
    result = {}
    used_places = set()
    
    # Generate all combinations of three places
    all_combinations = list(combinations(attractions, 3))
    
    # Sort combinations by the maximum distance between any two places in the group
    all_combinations.sort(key=lambda x: max(distance(x[i], x[j]) for i in range(3) for j in range(i+1, 3)))
    
    # Initialize day index
    index = 1
    for comb in all_combinations:
        if index > num_days:
            break
        
        # Check if any place in the combination has already been used
        if any(place['name'] in used_places for place in comb):
            continue
        
        if index not in result:
            result[index] = []
        
        group = []
        for place in comb:
            group.append({
                "place_name": place['name'],
                "lat_long": f"{place['latitude']}, {place['longitude']}"
            })
            used_places.add(place['name'])
        
        result[index].append(group)
        index += 1
    
    # Ensure the result structure conforms to the requirement (nested arrays)
    formatted_result = {str(i): result.get(i, []) for i in range(1, num_days + 1)}
    # Convert the dictionary to a valid JSON string
    return formatted_result

def extract_places_and_restaurants(data):

    # If data is a string, convert it to a dictionary
    if isinstance(data, str):
        data = json.loads(data)
    # Lists to store extracted place names and restaurant names
    places = []
    restaurants = []
    # Iterate through each day in the data
    for day, entries in data.items():
        print("Entry", entries)
        for entry_list in entries:
            
            for entry in entry_list:
                
                # Check if the key 'place_name' exists and append it to places list
                if 'place_name' in entry:
                    places.append(entry['place_name'])
                
                # Check if the key 'restaurant_name' exists and append it to restaurants list
                if 'restaurant_name' in entry:
                    restaurants.append(entry['restaurant_name'])
    
    return places, restaurants


import json

def inject_descriptions(input1, input2):
    # First check if input1 and input2 are strings and convert them to JSON objects if needed
    if isinstance(input1, str):
        try:
            input1 = json.loads(input1)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format for input1")

    if isinstance(input2, str):
        try:
            input2 = json.loads(input2)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format for input2")

    # Ensure input2 has both 'Places' and 'Restaurants' keys
    if "Places" not in input2 or "Restaurants" not in input2:
        raise KeyError("Input2 must contain 'Places' and 'Restaurants' keys")

    places_descriptions = input2["Places"]
    restaurant_descriptions = input2["Restaurants"]

    place_idx = 0
    restaurant_idx = 0

    # Iterate through each day in input1
    for day, locations in input1.items():
        for location_list in locations:
            for loc in location_list:
                # If it's a place, inject the place description using place_idx
                if "place_name" in loc:
                    if place_idx < len(places_descriptions):
                        loc["description"] = places_descriptions[place_idx]
                        place_idx += 1  # Move to the next place description
                    else:
                        raise IndexError("Not enough place descriptions for the number of places")

                # If it's a restaurant, inject the restaurant description using restaurant_idx
                elif "restaurant_name" in loc:
                    if restaurant_idx < len(restaurant_descriptions):
                        loc["description"] = restaurant_descriptions[restaurant_idx]
                        restaurant_idx += 1  # Move to the next restaurant description
                    else:
                        raise IndexError("Not enough restaurant descriptions for the number of restaurants")

    json_result = json.dumps(input1, indent=4)
    return json_result
