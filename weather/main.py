import routines as weather_routines
import json


def test():
    current_weather = weather_routines.get_weather_by_zip('60614')
    print(json.dumps(current_weather.to_dict(), indent=4))

test()

