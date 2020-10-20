import json


class Calendar:
    """Calendar class"""

    def __init__(self):
        with open("calendar.json") as json_file:
            calendar_dict = json.load(json_file)
        for key, value in calendar_dict.items():
            setattr(self, key, value)

    def current_date(self, n_days):
        """Get current date."""
        counter = 0
        while n_days > self.year_len:
            n_days -= self.year_len
            counter += 1
        for key, value in self.month_len.items():
            if n_days <= value:
                return self.start_year + counter, key, n_days
            else:
                n_days -= value

    def current_weekday(self, n_days):
        """Get current weekday."""
        weekday = n_days % self.week_len
        return self.weekdays[weekday-1]
    
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
