import unittest
from unittest.mock import patch, mock_open
import math
import csv

# Import the functions to be tested
from GeoLocs import convert_to_decimal, haversine, validate_lat_lon, match_closest_points, get_city_name, load_city_database

class TestGeoFunctions(unittest.TestCase):
    
    def test_convert_to_decimal(self):
        self.assertEqual(convert_to_decimal("40.7128 N"), 40.7128)
        self.assertEqual(convert_to_decimal("74.0060 W"), -74.0060)
        self.assertEqual(convert_to_decimal("51.5074"), 51.5074)
        self.assertEqual(convert_to_decimal("-0.1278"), -0.1278)
        with self.assertRaises(ValueError):
            convert_to_decimal("invalid data")
    
    def test_haversine(self):
        distance = haversine(40.7128, -74.0060, 34.0522, -118.2437)  # NYC to LA
        self.assertAlmostEqual(distance, 3935.75, places=2)

    def test_validate_lat_lon(self):
        validate_lat_lon(40.7128, -74.0060)  # Should not raise an error
        with self.assertRaises(ValueError):
            validate_lat_lon(100, -74.0060)  # Invalid latitude
        with self.assertRaises(ValueError):
            validate_lat_lon(40.7128, -200)  # Invalid longitude

    def test_match_closest_points(self):
        set1 = [(40.7128, -74.0060)]  # NYC
        set2 = [(34.0522, -118.2437), (51.5074, -0.1278)]  # LA, London
        matched = match_closest_points(set1, set2)
        self.assertEqual(matched[0][:2], (40.7128, -74.0060))  # NYC
        self.assertEqual(matched[0][2:4], (34.0522, -118.2437))  # Closest should be LA

    def test_get_city_name(self):
        city_database = {
            (40.7128, -74.0060): ("New York", "USA"),
            (34.0522, -118.2437): ("Los Angeles", "USA"),
        }
        self.assertEqual(get_city_name(40.7128, -74.0060, city_database), ("New York", "USA"))
        self.assertEqual(get_city_name(34.0522, -118.2437, city_database), ("Los Angeles", "USA"))
        self.assertEqual(get_city_name(0, 0, city_database), "Unknown location")

    @patch("builtins.open", new_callable=mock_open, read_data="""Country,City,Latitude,Longitude\nUSA,New York,40.7128,-74.0060\nUSA,Los Angeles,34.0522,-118.2437""")
    def test_load_city_database(self, mock_file):
        city_database = load_city_database("mock_file.csv")
        self.assertIn((40.7128, -74.0060), city_database)
        self.assertEqual(city_database[(40.7128, -74.0060)], ("New York", "USA"))
        self.assertIn((34.0522, -118.2437), city_database)
        self.assertEqual(city_database[(34.0522, -118.2437)], ("Los Angeles", "USA"))

if __name__ == "__main__":
    unittest.main()
