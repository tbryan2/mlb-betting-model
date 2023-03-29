
from pyowm import OWM
from pyowm.weatherapi25.weather import Weather
import secrets as mysecrets


def get_weather_by_zip(zipcode: str) -> Weather:
    """
    Get the current weather by the specified zip code
    """
    owm = OWM(mysecrets.WEATHER_API_KEY)
    mgr = owm.weather_manager()

    observation = mgr.weather_at_zip_code(zipcode)

    return observation.weather