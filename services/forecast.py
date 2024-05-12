from collections import OrderedDict

from utils.owm_client import get_5_days_weather_forecast

weights = {
    'temp': 0.1,
    'cloud': 0.2,
    'wind': 0.3,
    'rain': 0.4,
    'snow': 0.5
}


def forecast_best_day(user_preference) -> str:
    """
        Forecast the recommended best day from 5-day weather forecast based on a user's weather preference.
        Return a weather date string value or None value if no best day found.
    """
    # Get the 5-day forecast data first based on the user's location
    weathers = get_5_days_weather_forecast(user_preference.location)

    # Group the weather data list by weather date into an ordered dictionary
    weathers_grouped_by_date = OrderedDict()
    for weather in weathers:
        weather_date = str(weather.reference_time('date').date())
        weather_list = weathers_grouped_by_date.get(weather_date, [])
        weather_list.append(weather)
        weathers_grouped_by_date[weather_date] = weather_list

    weighted_sum_dict = OrderedDict()

    # For each group of weather list, we will check if the weather list is valid based on the user preference setting.
    # Each weather data in the weather list must be all valid.
    # When a weather list is valid, calculate average data and then calculate weighted sum of the average data.
    # This will produce a dictionary of weather date key and the weighted sum value.
    for date, weathers in weathers_grouped_by_date.items():
        weathers_count = len(weathers)
        valid = True
        total_temp = 0
        total_cloudiness = 0
        total_wind_speed = 0
        total_rain_volume = 0
        total_snow_volume = 0

        for weather in weathers:
            # Validate the weather data against the user preference
            is_temp_pref_passed = temperature_preference_check(weather,
                                                               user_preference.temp_min,
                                                               user_preference.temp_max)
            is_cloud_pref_passed = cloud_preference_check(weather, user_preference.max_cloudiness)
            is_wind_pref_passed = wind_preference_check(weather, user_preference.max_wind_speed)
            is_rain_pref_passed = rain_preference_check(weather, user_preference.max_rain_volume)
            is_snow_pref_passed = rain_preference_check(weather, user_preference.max_snow_volume)

            total_temp += get_temp(weather)
            total_cloudiness += get_cloudiness(weather)
            total_wind_speed += get_wind_speed(weather)
            total_rain_volume += get_rain_volume(weather)
            total_snow_volume += get_snow_volume(weather)

            valid = (is_temp_pref_passed and is_cloud_pref_passed and is_wind_pref_passed and is_rain_pref_passed
                     and is_snow_pref_passed)
            if not valid:
                break

        # If the weather list data is valid, calculate the average data and then calculate the weighted sum
        # and save the weighted sum value into a dictionary
        if valid:
            average_weather_data = {
                "temp": total_temp / weathers_count if weathers_count > 0 else 0,
                "cloud": total_cloudiness / weathers_count if weathers_count > 0 else 0,
                "wind": total_wind_speed / weathers_count if weathers_count > 0 else 0,
                "rain": total_rain_volume / weathers_count if weathers_count > 0 else 0,
                "snow": total_snow_volume / weathers_count if weathers_count > 0 else 0
            }
            weighted_sum_dict[date] = sum(average_weather_data[name] * weights[name] for name in weights)

    the_best_day = None
    smallest_weighted_sum = float('inf')

    # Find the smallest weighted sum value and the linked weather date will be the best day
    for date, weighted_sum in weighted_sum_dict.items():
        if weighted_sum < smallest_weighted_sum:
            the_best_day = date
            smallest_weighted_sum = weighted_sum

    return the_best_day


def temperature_preference_check(weather, temp_min, temp_max) -> bool:
    temp_data = weather.temperature()
    if temp_data and temp_data["temp"]:
        if temp_min is not None and temp_max is None:
            return temp_data["temp"] >= temp_min
        elif temp_min is None and temp_max is not None:
            return temp_data["temp"] <= temp_max
        elif temp_min is not None and temp_max is not None:
            return temp_min <= temp_data["temp"] <= temp_max

    return True


def cloud_preference_check(weather, max_cloudiness) -> bool:
    cloudiness = weather.clouds
    if cloudiness and max_cloudiness:
        return cloudiness <= max_cloudiness

    return True


def wind_preference_check(weather, max_wind_speed) -> bool:
    wind_data = weather.wind()
    if wind_data and wind_data["speed"] and max_wind_speed:
        return wind_data["speed"] <= max_wind_speed

    return True


def rain_preference_check(weather, max_rain_volume) -> bool:
    rain_data = weather.rain
    if rain_data and rain_data["3h"] and max_rain_volume:
        return rain_data["3h"] <= max_rain_volume

    return True


def snow_preference_check(weather, max_snow_volume) -> bool:
    snow_data = weather.snow
    if snow_data and snow_data["3h"] and max_snow_volume:
        return snow_data["3h"] <= max_snow_volume

    return True


def get_temp(weather) -> float:
    temp_data = weather.temperature()
    if temp_data and temp_data["temp"]:
        return temp_data["temp"]

    return 0


def get_cloudiness(weather) -> float:
    cloudiness = weather.clouds
    if cloudiness:
        return cloudiness

    return 0


def get_wind_speed(weather) -> float:
    wind_data = weather.wind()
    if wind_data and wind_data["speed"]:
        return wind_data["speed"]

    return 0


def get_rain_volume(weather) -> float:
    rain_data = weather.rain
    if rain_data and rain_data["3h"]:
        return rain_data["3h"]

    return 0


def get_snow_volume(weather) -> float:
    snow_data = weather.snow
    if snow_data and snow_data["3h"]:
        return snow_data["3h"]

    return 0
