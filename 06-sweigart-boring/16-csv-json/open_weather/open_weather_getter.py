import requests
import json
import pprint

class OpenWeathergetter:
    """
    Overall, the program does the following:
        1. Reads the requested location from the command line
        2. Downloads JSON weather data from OpenWeatherMap.org
        3. Converts the string of JSON data to a Python data structure
        4. Prints the weather for today and the next two days

    So the code will need to do the following:
        1. Join strings in sys.argv to get the location.
        2. Call requests.get() to download the weather data.
        3. Call json.loads() to convert the JSON data to a Python data structure.
        4. Print the weather forecast.
    """
    
    def __init__(self,
                 api_key='', 
                 city_name='New York', state_code='NY', country_code='US'):
        self._api_key = api_key
        self._lat_long_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={api_key}'
        self._get_lat_long()
        self._weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={self._lat}&lon={self._lon}&appid={api_key}'
        self._weather_data = None

    def _get_lat_long(self):
        # Download the JSON data from OpenWeatherMap.org's API.
        response = requests.get(self._lat_long_url)
        response.raise_for_status()
        # Load JSON data into a Python variable.
        self._lat_long_data = json.loads(response.text)
        self._lat = self._lat_long_data[0]['lat']
        self._lon = self._lat_long_data[0]['lon']

    def get_weather(self):
        """
        Get the 'current weather data' from OpenWeatherMap.org's API:
        https://openweathermap.org/current
        """
        # Download the JSON data from OpenWeatherMap.org's API.
        response = requests.get(self._weather_url)
        response.raise_for_status()
        # Load JSON data into a Python variable.
        self._weather_data = json.loads(response.text)

    def print_weather(self):
        """
        Print the current weather:
        1. Location.
        2. Temperature.
        3. Weather description.
        """ 
        location = self._weather_data['name']
        temperature = self._weather_data['main']['temp']
        temperature = self._convert_kelvin_to_celsius(temperature)
        weather_description = self._weather_data['weather'][0]['description']
        print(f'Location: {location}')
        print(f'Temperature: {temperature}')
        print(f'Weather: {weather_description}')

    def _convert_kelvin_to_celsius(self, kelvin):
        return int(kelvin - 273.15)


if __name__ == '__main__':
    weather = OpenWeathergetter()
    # Print latitude and longitude
    weather.get_weather()
    weather.print_weather()