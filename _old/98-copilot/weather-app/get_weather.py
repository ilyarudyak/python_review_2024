import requests
import json

api_key = ''

def get_weather(city):
    """
    Get the weather for a city using the OpenWeatherMap API.
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        weather = response.json()
        return weather
    
if __name__ == '__main__':
    city = 'New York'
    weather = get_weather(city)
    if weather:
        print(json.dumps(weather))