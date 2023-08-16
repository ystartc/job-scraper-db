import requests
import os
load_dotenv()


def get_lat_long(location):
    API_KEY = os.environ.get('LOCATIONIQ_API_KEY')
    url = f'https://us1.locationiq.com/v1/search?key={API_KEY}&q={location}&format=json'
    response = requests.get(url)
    data = response.json()
    if data:
        first_result = data[0]
        lat = first_result['lat']
        lon = first_result['lon']
        print(f"Latitude: {lat}, Longitude: {lon}")
        return lat, lon
    
def get_all_within_radius(location, radius=None):
    base_url = "http://api.geonames.org/findNearbyPlaceNameJSON"

    # Geonames username
    username = os.environ.get('GEONAMES_USERNAME')

    lat, long = get_lat_long(location)
    if not radius:
        radius = 50 * 1.60934
    else:
        radius *= 1.60934
    
    # Radius in kilometers

    # Make the API request
    response = requests.get(base_url, params={
        "lat": lat,
        "lng": long,
        "radius": radius,
        "username": username
    })

    # Parse and print the response
    data = response.json()
    cities = set()
    for city in data['geonames']:
        if city not in cities:
            print(city['name'], city['adminName1'])
            cities.add(city['name'])
        
    return cities