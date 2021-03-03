import json


class Calendar:
    """Calendar class"""

    def __init__(self):
        with open("harptos_calendar.json") as json_file:
            calendar_dict = json.load(json_file)
        for key, value in calendar_dict.items():
            setattr(self, key, value)
        self.leap_cycle_days = (self.leap_year_freq - 1) * self.year_len + self.leap_year_len
        self.day_of_year = None 
        self.leap_year = None
        self.current_month = None
        # run current_date
        self.today = self.current_date(self.current_day)

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
            self.leap_year = True
            self.day_of_year =  remainder
            return (years_so_far, Calendar.format_days(last_month_year, last_month_year.get("days")))
        counter = 1
        while remainder > self.year_len:
            if counter == self.leap_year_freq:
                self.leap_year = True
                break
            remainder -= self.year_len
            years_so_far += 1
            counter += 1
        self.day_of_year = remainder
        for month in self.months:
            days_in_month = month.get("days")
            if month.get("leap") and self.leap_year is False:
                continue
            if remainder > days_in_month:
                remainder -= days_in_month
            else:
                self.current_month = month
                return (years_so_far, Calendar.format_days(month, remainder))

    def get_date(self, n_days):
        """Get day (combine with current date)"""
        leap_year = False
        full_leap_cycles = n_days // self.leap_cycle_days
        remainder = n_days % self.leap_cycle_days
        years_so_far = int(full_leap_cycles*4)
        if remainder == 0:
            last_month_year = self.months[-1]
            leap_year = True
            return (years_so_far, Calendar.format_days(last_month_year, last_month_year.get("days")))
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

    def days_since_start(self):
        """Returns how many days have passed since start date."""
        return self.current_day - self.first_day

    def today_as_str(self):
        year, day = self.today
        return f"Today is {day}, Year {self.start_year + year}"

    def add_days(self, n_days):
        self.current_day += n_days
        with open("harptos_calendar.json","r+") as json_file:
            data = json.load(json_file)
            data["current_day"] = self.current_day
        with open("harptos_calendar.json", 'w') as f:
            json.dump(data, f, indent=4)
        self.today = self.current_date(self.current_day)

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

    def create_custom_event(self, day, name, notes):
        """Creates a custom event."""
        year, date = self.get_date(day)
        event_dict = {
            "day" : day - self.first_day + 1,
            "name": name,
            "notes": notes,
            "date": f"{date.title()}, Year {self.start_year + year}"
        }
        self.events.append(event_dict)
        self.events = sorted(self.events, key = lambda i: i['day'])
        with open("events.json", 'w') as f:
            json.dump(self.events, f, indent=4)
        return event_dict

    def get_custom_events(self, n_events):
        """Returns n recent events."""
        if len(self.events) <= n_events:
            return self.events
        return self.events[-1*n_events]
