import json
from math import floor, ceil
from inflection import ordinal

from database import session, Guild

def apply_defaults(cls):
    """Populate default values based on harptos calendar."""
    with open("data/harptos_calendar.json") as json_file:
        calendar_dict = json.load(json_file)
    for key, value in calendar_dict.items():
        setattr(cls, key, value)
    # calculate leap cycle length
    setattr(cls, "leap_cycle_days", cls.year_len*(cls.leap_year_freq-1)+cls.leap_year_len)
    return cls

@apply_defaults
class Calendar(object):
    """Calendar class - for each guild"""

    def __init__(self, guild_id):
        guild_data = self.get_guild(guild_id)
        self.guild = guild_data.guild
        self.first_day = guild_data.first_day
        self.current_day = guild_data.current_day
        self.leap_year = guild_data.leap_year

    @staticmethod
    def format_days(month_dict, day):
        name = month_dict.get('name')
        alternate_name = month_dict.get('alternate')
        if month_dict.get('days') == 1:
            return f"{name}"
        return f"day {day} of {name}, {alternate_name}"

    def get_date(self, n_days=0, current_adjusted=True):
        """Get day. If current_adjusted=True add current day"""
        leap_year = False
        if current_adjusted:
            n_days += self.current_day
        full_leap_cycles = n_days // self.leap_cycle_days
        remainder = n_days % self.leap_cycle_days
        years_so_far = int(full_leap_cycles*self.leap_year_freq)
        if remainder == 0:
            last_month_year = self.months[-1]
            leap_year = True
            return (last_month_year.get("days"), last_month_year, years_so_far)
        counter = 1
        while remainder > self.year_len:
            if counter == self.leap_year_freq:
                leap_year = True
                break
            remainder -= self.year_len
            years_so_far += 1
            counter += 1
        for month in self.months:
            days_in_month = month.get("days")
            if month.get("leap") and leap_year is False:
                continue
            if remainder > days_in_month:
                remainder -= days_in_month
            else:
                return (remainder, month, years_so_far)

    def current_moons(self, n_days):
        """Get current moon phase."""
        moon_phases = [("Full Moon", "🌕"), ("Waxing Gibbous", "🌔"), ("First Quarter", "🌓"), ("Waxing Crescent", "🌒"), ("New Moon", "🌑"), ("Waning Crescent", "🌘"), ("Third Quarter", "🌗"), ("Waning Gibbous", "🌖")]
        phase_dict = {}
        # convert days to minutes
        n_minutes = floor(n_days)*24*60
        for key, value in self.lunar_cyc.items():
            # the key is the moon and the value is the cycle in minutes
            incomplete_phase = floor(n_minutes) % value
            if incomplete_phase == 0:
                # then 
                phase_dict[key] = {
                    "name": moon_phases[0][0],
                    "emoji": moon_phases[0][1],
                    "next_full": ceil((value-incomplete_phase)/(24*60))
                }
                continue
            phase_length = floor(value/len(moon_phases))
            phase = incomplete_phase // phase_length
            phase = floor(phase)
            if phase == 8:
                phase = 7
            # days until next full moon
            phase_dict[key] = {
                "name": moon_phases[phase][0],
                "emoji": moon_phases[phase][1],
                "next_full": ceil((value-incomplete_phase)/(24*60))
            }
        return phase_dict

    def string_moon(self, phase_dict):
        """Return moon phases as string"""
        formatted_string = ""
        for key, value in phase_dict.items():
            formatted_string += f"* {key} is in the {value['name']} {value['emoji']} phase. It is {value['next_full']} days until the next Full Moon.\n"
        return formatted_string

    def days_since_start(self):
        """Returns how many days have passed since start date."""
        return self.current_day - self.first_day

    def day_as_str(self, n_days=0, current_adjusted=True):
        day, month, year = self.get_date(n_days, current_adjusted)
        if month.get("days") == 1:
            return f"{month.get('name')}, Year {year} DR."
        return f"{day}{ordinal(day)} of {month.get('name')}, {month.get('alternate')}, Year {year} DR"
      
    def add_days(self, n_days, day_type="current_day"):
        day_value = getattr(self, day_type)
        day_value += n_days
        setattr(self, day_type, day_value)
        guild = self.get_guild(self.guild)
        setattr(guild, day_type, day_value)
        session.commit()

    def closest_holiday(self):
        """Get closest upcomming holiday."""
        leap_adjust = 0
        for holiday in self.holidays:
            if holiday.get("name") == "Shieldmeet" and self.leap_year is False:
                leap_adjust = 1
            adjusted_date = holiday.get("date") - leap_adjust
            if self.day_of_year > adjusted_date:
                continue
            else:
                return (adjusted_date - self.day_of_year, holiday)
        if self.leap_year:
            days_in_year = self.leap_year_len
        else:
            days_in_year = self.year_len
        days_left = days_in_year - self.day_of_year + self.holidays[0].get("date")
        return (days_left, self.holidays[0])

    ############### Helper Functions ###############
    @staticmethod
    def get_guild(guild_id):
        """guild_id -> Return Guild DB object."""
        guild = session.query(Guild).filter_by(guild=guild_id).first()
        return guild

