import datetime as dt
import requests
import numpy as np


base_url = "https://api.openweathermap.org/data/2.5/weather?"
api_key = "0e00fc2e12f7078bfa2c634a0c063043"
city = "Odense"
url = base_url + "appid=" + api_key + "&q=" + city

def get_info():
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        return response

    else:
        print('Data not available!')

def kelvin_2_celc(kelvin):
    celc = kelvin - 273
    return celc

response = get_info()
if response:
    temp_kelvin = response['main']['temp']
    temp_celc = int(kelvin_2_celc(temp_kelvin))
    print(f"Temperature: {temp_celc}'")

    describ = response['weather'][0]['description']
    print(f"Description: {describ}")