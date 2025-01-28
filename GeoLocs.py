import math
import re
import csv
import urllib.request

url = "https://raw.githubusercontent.com/joelacus/world-cities/refs/heads/main/world_cities.csv"

file_name = "world_cities.csv"

# download and save the file
try:
    urllib.request.urlretrieve(url, file_name)
    print(f"CSV file saved as: {file_name}")
except Exception as e:
    print(f"Failed to download file: {e}")

# path to the uploaded CSV file NOTE: WRONG FILE
# file_path = "Major_Cities_GPS.csv" # in the same folder as GeoLocs.py

# function to convert given format to decimal degrees
def convert_to_decimal(coord):
    
    # converts latitude or longitude from directional format (e.g., 40.7128 N)
    # or decimal format (e.g., 51.5074) to a standard decimal degree format

    coord = coord.strip().lower().replace("degrees", "").strip()

    # check for a format with direction (e.g., 40.7128° N)
    match = re.match(r"([\d.]+)\s*°?\s*([NSWE])?", coord, re.IGNORECASE)

    if match:
        value, direction = match.groups()
        value = float(value)

        if direction and direction.upper() in ["S", "W"]:
            return -value
        return value
    
    # assume it is already in decimal format
    try:
        return float(coord)
    except ValueError:
        raise ValueError(f"Invalid Coordinate format: {coord}")
    
# function to calculate the distance using haversine formula
def haversine(lat1, lon1, lat2, lon2):

    # calculate the great-circle distance between two points using the Haversine formula
    R = 6371 # earths radius in kilometers

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2* math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c    # distance in kilometers

# function to load city data from the CSV file
def load_city_database(file_name):
    city_database = {}
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.reader(file) 
        next(reader)    # skip the first (header) row

        for row in reader:
            try:
                country = row[0].strip()
                name = row[1].strip()
                lat = convert_to_decimal(row[2].strip())
                lon = convert_to_decimal(row[3].strip())
                city_database[(round(lat,4), round(lon,4))] = name, country
            except (IndexError, ValueError):
                print(f"Skipping invalid row: {row}")
    
    return city_database
        
# function to find the closest city for a given latitude and longitude
"""def find_closest_city(lat, lon, city_database):

    # if the exact match isn't found, it finds the closest approximate match

    closest_city = None
    min_distance = float('inf')

    for (city_lat, city_lon), city_name in city_database.items():
        dist = haversine(lat, lon, city_lat, city_lon)
        if dist < min_distance:
            min_distance = dist
            closest_city = city_name

    return closest_city, min_distance
"""

# function that validates the ranges of the lat and lon (error checking)
def validate_lat_lon(lat, lon):
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}. Must be between -90 and 90.")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}. Must be between -180 and 180.")


# function to get the input (locations) from the user
def get_user_input(set_name):
    
    locations = []
    print(f"\nEnter {set_name} locations (format: Latitude, Longitude)")
    print("make sure to seperate the latitude and longitude with a comma")
    print("Examples: 40.7128° N, 74.0060° W OR 51.5074, -0.1278")
    print("Type 'done' when finished.")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "done":
            break
        try:
            lat_str, lon_str = map(str.strip, user_input.split(","))
            lat, lon = convert_to_decimal(lat_str), convert_to_decimal(lon_str)
            validate_lat_lon(lat, lon)
            locations.append((lat, lon))
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    
    return locations

# function that matches each point in set 1 to the closest point in set 2 based on geographical distance
def match_closest_points(set1, set2):
    matched_points = []

    for lat1, lon1 in set1:
        closest_point = None
        min_distance = float('inf')

        for lat2, lon2 in set2:
            dist = haversine(lat1, lon1, lat2, lon2)
            if dist < min_distance:
                min_distance = dist
                closest_point = (lat2, lon2)

        matched_points.append((lat1, lon1, closest_point[0], closest_point[1], min_distance))
    return matched_points

# function to get the city name from the database
def get_city_name(lat, lon, city_database):
    return city_database.get((round(lat,4), round(lon, 4)), "Unknown location")

# main program

city_database = load_city_database(file_name)
    
set1 = get_user_input("Set 1")
set2 = get_user_input("Set 2")

# find the closest matches
matched_results = match_closest_points(set1, set2)

# Display results with city names
print("\nClosest Matches:")
print("-" * 55)
for lat1, lon1, lat2, lon2, distance in matched_results:
    city1 = get_city_name(lat1, lon1, city_database)
    city2 = get_city_name(lat2, lon2, city_database)
    print(f"{city1} is the closest to {city2} ({distance:.2f} km)")