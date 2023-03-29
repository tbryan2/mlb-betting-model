


from pyowm import OWM
from pyowm.weatherapi25.weather import Weather
from pyowm.utils import config
from pyowm.utils import timestamps
import json

import secrets as mysecrets

# ---------- FREE API KEY examples ---------------------

owm = OWM(mysecrets.WEATHER_API_KEY)
mgr = owm.weather_manager()


# Search for current weather in London (Great Britain) and get details
observation = mgr.weather_at_place('London,GB')
w: Weather = observation.weather

w.detailed_status         # 'clouds'
w.wind()                  # {'speed': 4.6, 'deg': 330}
w.humidity                # 87
w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
w.rain                    # {}
w.heat_index              # None
w.clouds                  # 75


print(json.dumps(w.__dict__, indent=4))


