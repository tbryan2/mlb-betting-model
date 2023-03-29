from __future__ import annotations
from pyowm import OWM
from pyowm.weatherapi25.weather import Weather
from pyowm.weatherapi25.weather_manager import WeatherManager
from mlbbetting import configs

def get_weather_by_zip(zipcode: str) -> Weather:
    """Get the current weather by the specified zip code"""
    
    weather_manager = _get_weather_manager()
    observation = weather_manager.weather_at_zip_code(zipcode, 'US')

    return observation.weather


def _get_weather_manager() -> WeatherManager:
    """Get a new weather manager object"""

    config = configs.get_config(True)

    owm = OWM(config.weather_api_key)
    mgr = owm.weather_manager()

    return mgr