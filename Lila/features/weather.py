import requests
from Lila import config


def fetch_weather(city):
    """
    Get the weather in the city
    :param city: (string) city
    :return: (string) weather
    """
    api_key = config.weather_api_key
    units_format = "&units=imperial"

    weather_data = get_data(city, api_key, units_format)

    if weather_data["cod"] == "404":
        city = config.local_city
        weather_data = get_data(city, api_key, units_format)

    if weather_data["cod"] != "404":
        main_data = weather_data["main"]
        weather_description_data = weather_data["weather"][0]
        weather_description = weather_description_data["description"]
        current_temperature = main_data["temp"]
        current_pressure = main_data["pressure"]
        current_humidity = main_data["humidity"]
        wind_data = weather_data["wind"]
        wind_speed = wind_data["speed"]

        final_response = f"""
                The weather in {city} is currently {weather_description} 
                with a temperature of {current_temperature} degrees fahrenheit
        """
        if not config.skip:
            final_response += f"""
                atmospheric pressure of {current_pressure} a m use, 
                humidity of {current_humidity} percent 
                and wind speed reaching {wind_speed} miles per hour"""

        return final_response

    return "Sorry Sir, I couldn't find the city in my database. Please try again"


def get_data(city, api_key, units_format):
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    complete_url = base_url + city + "&appid=" + api_key + units_format

    response = requests.get(complete_url)
    weather_data = response.json()

    return weather_data