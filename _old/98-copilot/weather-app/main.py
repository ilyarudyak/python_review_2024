from get_weather import get_weather

# Ask user for their desired location to get the weather
location = input("Enter the location: ")

# Get the weather for the location using the get_weather function
weather = get_weather(location)

# Define a function to convert Kelvin to Fahrenheit
def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

# Print the high and low temperatures for the location
if weather:
    temp_min = kelvin_to_fahrenheit(weather['main']['temp_min'])
    temp_max = kelvin_to_fahrenheit(weather['main']['temp_max'])
    print(f"The high temperature is {temp_max:.1f}°F and the low temperature is {temp_min:.1f}°F.")