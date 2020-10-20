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
        return f"Day {day} of {name}, {alternate_name}"

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
        moon_phases = [("New Moon", 0), ("Waning Crescent", 1), ("Third Quarter", 2), ("Waning Gibbous", 3), ("Full Moon", 4), ("Waxing Gibbous", 5), ("First Quarter", 6), ("Waxing Crescent", 7)]
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

    def add_days(self, n_days):
        self.current_day += n_days
        with open("calendar.json","r+") as json_file:
            data = json.load(json_file)
            data["current_day"] = self.current_day
        with open("calendar.json", 'w') as f:
            json.dump(data, f, indent=4)