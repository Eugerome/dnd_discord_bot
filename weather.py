"""Randomise weather"""
import json
import random

with open("weather.json") as json_file:
    weather_dict = json.load(json_file)

class DailyForecast:
    """Create a forecast for the day."""

    def __init__(self, day_of_year):
        self.season = self.get_season(day_of_year)
        self.season_patterns = weather_dict.get("season_patterns").get(self.season)
        self.avg_temp = self.generate_temperature(self.season_patterns.get("temperature"))
        self.forecast_string = ""
        self.get_string()
        

    def get_season(self, day_of_year):
        """Return the current season based on day of year."""
        for season, last_day in weather_dict.get("seasons").items():
            if day_of_year <= last_day:
                return season

    def generate_temperature(self, temp_range):
        return random.randrange(temp_range[0], temp_range[-1])

    def get_string(self):
        for time_of_day, temperature_mod in weather_dict.get("day_time").items():
            forecast = Forecast(time_of_day, self.avg_temp, temperature_mod, self.season_patterns)
            self.forecast_string += f"{forecast.get_string()}\n"

    def save_temp():
        pass

class Forecast():

    def __init__(self, time_of_day, avg_temp, temp_mod, season_patterns):
        self.time_of_day = time_of_day
        self.temperature = int(avg_temp + temp_mod)
        self.wind = self.get_wind(season_patterns.get("wind"))
        self.sky = self.get_wind(season_patterns.get("clouds"))
        self.precipitation = self.get_precipitation(self.sky, season_patterns.get("rain"))
        # adjust temperature if clear sky:
        if self.sky == "clear sky":
            self.temperature += int(season_patterns.get("clear sky_mod"))
        # adjust precipitation if negative temp
        if self.temperature <= 0:
            self.precipitation = self.precipitation.replace("rain", "snow")

    @staticmethod
    def get_sky(sky_pattern):
        result = random.randrange(1, 100)
        adjusted = 0
        for key, value in sky_pattern.items():
            adjusted += int(value * 100)
            if result <= adjusted:
                return key

    @staticmethod
    def get_wind(wind_pattern):
        result = random.randrange(1, 100)
        adjusted = 0
        for key, value in wind_pattern.items():
            adjusted += int(value * 100)
            if result <= adjusted:
                return key

    @staticmethod
    def get_precipitation(sky_status, rain_patterns):
        # return no rain if clear sky
        if sky_status == "clear sky":
            return "no rain"
        # process other possibilities
        adjusted_value = 0
        rain_status = {}
        for rain_type, value in rain_patterns.items():
            if rain_type == "no rain":
                adjusted_value += int(value*100)
            else:
                adjusted_value += int(value*100*weather_dict.get("rain_mod").get(sky_status))
            rain_status[rain_type] = adjusted_value
        result = random.randrange(0, adjusted_value)
        for key, value in rain_status.items():
            if result <= value:
                return key

    def get_string(self):
        """Returns formatted string."""
        return f"{self.time_of_day.title()}: {self.temperature}°C, {self.sky.title()}, {self.precipitation.title()}, {self.wind.title()}"

day = DailyForecast(1)
import pdb; pdb.set_trace()
