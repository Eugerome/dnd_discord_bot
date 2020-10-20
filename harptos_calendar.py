import json


class Calendar:
    """Calendar class"""

    def __init__(self):
        with open("calendar.json") as json_file:
            calendar_dict = json.load(json_file)
        for key, value in calendar_dict.items():
            setattr(self, key, value)
        self.leap_cycle_days = (self.gap_year_freq - 1) * self.year_len + self.gap_year_len

    @staticmethod
    def format_days(month_dict, day):
        name = month_dict.get('name')
        alternate_name = month_dict.get('alternate')
        if month_dict.get('days') == 1:
            return f"{name}"
        return f"day {day} of {name}, {alternate_name}"

    def current_date(self, n_days):
        """Get current date."""
        full_leap_cycles = n_days // self.leap_cycle_days
        remainder = n_days % self.leap_cycle_days
        years_so_far = int(full_leap_cycles*4)
        if remainder == 0:
            last_month_year = self.months[-1]
            return (years_so_far, Calendar.format_days(last_month_year, last_month_year.get("days")))
        counter = 1
        gap_year = False
        while remainder > self.year_len:
            if counter == self.gap_year_freq:
                gap_year = True
                break
            remainder -= self.year_len
            years_so_far += 1
            counter += 1
        for month in self.months:
            days_in_month = month.get("days")
            if month.get("leap") and gap_year is False:
                continue
            if remainder > days_in_month:
                remainder -= days_in_month
            else:
                return (years_so_far, Calendar.format_days(month, remainder))

    def current_moons(self, n_days):
        """Get current moon phase."""
        moon_phases = [("New Moon", "🌑"), ("Waning Crescent", "🌘"), ("Third Quarter", "🌗"), ("Waning Gibbous", "🌖"), ("Full Moon", "🌕"), ("Waxing Gibbous", "🌔"), ("First Quarter", "🌓"), ("Waxing Crescent", "🌒")]
        phase_list = []
        for key, value in self.lunar_cyc.items():
            incomplete_phase = n_days % value
            if incomplete_phase == 0:
                incomplete_phase = value
            phase_length = int(value/len(moon_phases))
            phase = incomplete_phase // phase_length
            phase = int(phase)
            if phase == 8:
                phase = 7
            phase_list.append((key, incomplete_phase, moon_phases[phase]))
        return phase_list

    def string_moon(self, phase_list):
        """Return moon phases as string"""
        formatted_string = ""
        for moon in phase_list:
            moon_name = moon[0]
            moon_days = moon[1]
            moon_cycle_str = moon[2][0]
            moon_cycle_emo = moon[2][1]
            formatted_string += f"{moon_name}: Day {moon_days} of cycle in the {moon_cycle_emo}  ({moon_cycle_str}) phase\n"
        return formatted_string
            

    def today_as_str(self):
        year, day = self.current_date(self.current_day)
        return f"Today is {day}, Year {self.start_year + year}"

    def add_days(self, n_days):
        self.current_day += n_days
        with open("calendar.json","r+") as json_file:
            data = json.load(json_file)
            data["current_day"] = self.current_day
        with open("calendar.json", 'w') as f:
            json.dump(data, f, indent=4)