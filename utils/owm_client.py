import os

from pyowm import OWM

owm = OWM(os.environ["OWM_API_KEY"])
mgr = owm.weather_manager()


def get_weather_at_place(place):
    observation = mgr.weather_at_place(place)
    return observation.weather


def get_5_days_weather_forecast(place):
    return mgr.forecast_at_place(place, '3h').forecast
