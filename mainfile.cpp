#include <iostream>
#include <vector>
#include <cmath>
#include <limits>

using namespace std;

// earth's radius in km
const double EARTH_RADIUS = 6371.0;

// function to convert degrees to radians
// haversine uses radians
double DegToRad(double degree)
{
    return degree * M_PI / 180.0;
}

// Using the Haversine formula to calculate the distance
double haversine(double lat1, double lon1, double lat2, double lon2)
{
    double dLat = DegToRad(lat2 - lat1);
    double dLon = DegToRad(lon2 - lon1);

    lat1 = DegToRad(lat1);
    lat2 = DegToRad(lat2);

    double a = sin(dLat / 2) * sin(dLat / 2) + cos(lat1) * cos(lat2) * sin(dLon / 2) * sin(dLon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));

    return EARTH_RADIUS * c;
}

int main()
{
    // create the two vectors
    // vector 1 American cities
    vector<pair<double, double>> Array1 = {
        {40.7128, -74.0060},  // NY city
        {34.0522, -118.2437}, // LA
        {41.8781, -87.6298},  // Chicago
        {37.7749, -122.4194}, // San Francisco
        {25.7617, -80.1918}   // Miami
    };
    // vector 2 european cities
    vector<pair<double, double>> Array2 = {
        {51.5047, -0.1278}, // London
        {48.8566, 2.3522},  // Paris
        {52.5200, 13.4050}, // Berlin
        {41.9028, 12.4964}, // Rome
        {40.4168, -3.7038}  // Madrid
    };

    // match each american city to the closest european city
    cout << "Closest European cities to each American city: \n";

    for (const auto &americanCity : Array1)
    {
        double minDistance = numeric_limits<double>::max();
        pair<double, double> closestCity;

        for (const auto &europeanCity : Array2)
        {
            double distance = haversine(americanCity.first, americanCity.second, europeanCity.first, europeanCity.second);
            if (distance < minDistance)
            {
                minDistance = distance;
                closestCity = europeanCity;
            }
        }

        // output results
        cout << "American City (" << americanCity.first << ", " << americanCity.second << ")" << " -> closest European City (" << closestCity.first << ", " << closestCity.second << ")" << " [Distance: " << minDistance << " km]\n";
    }

    return 0;
}