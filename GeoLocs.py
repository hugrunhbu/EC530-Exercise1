import math
import re

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
    print(matched_points)
    return matched_points

# main program
    
set1 = get_user_input("Set 1")
set2 = get_user_input("Set 2")

# find the closest matches
matched_results = match_closest_points(set1, set2)

# Display results
print("\nClosest Matches:")
print("-" * 55)
print(f"{'Lat1':<12}{'Lon1':<12}  ->  {'Closest Lat':<12}{'Closest Lon':<12}  {'Distance (km)':<10}")
print("-" * 55)
for match in matched_results:
    lat1, lon1, lat2, lon2, distance = match
    print(f"{lat1:<12.4f}{lon1:<12.4f}  ->  {lat2:<12.4f}{lon2:<12.4f}  {distance:<10.2f}")