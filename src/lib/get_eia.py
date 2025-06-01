import requests
import os

def get_eia_api_key():
    return os.environ['eia_api_key']

def test_get_eia_data():
    
    api_key = get_eia_api_key()
    url = "https://api.eia.gov/v2/electricity/rto/region-sub-ba-data/data/"
    params = {
        "frequency": "daily",
        "data[0]": "value",
        "start": "2019-01-01T00",
        "end": "2025-05-31T00",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 5000,
        "api_key": api_key
    }
    r = requests.get(url, params=params)
    grid_data = r.json()
    return grid_data


print("hello")
data = test_get_eia_data()
print("hey")