import requests

def get_cities_coordinates(query):
    # custom User-Agent used to fit Nominatim's Usage Policy
    # https://operations.osmfoundation.org/policies/nominatim/
    headers = {
        "User-Agent": "Yandex Weather Parser by I2oony (ppalamar28@gmail.com)",
        "Accept-Language": "ru-RU"
    }

    url = "https://nominatim.openstreetmap.org/search"
    query_params = {
        "city": query,
        "format": "json",
        "limit": 5
    }

    response = requests.get(url, headers=headers, params=query_params)
    results = response.json()

    list_of_results = list()
    for item in results:
        list_of_results.append(City(item["name"], 
                                    item["display_name"], 
                                    item["lat"], 
                                    item["lon"]))

    return list_of_results

class City:
    def __init__(self, name, display_name, lat, lon):
        self.name = name
        self.display_name = display_name
        self.lat = lat
        self.lon = lon
