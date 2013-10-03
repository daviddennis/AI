from datetime import datetime


class TimeManager():

    def __init__(self):
        self.time_terms = 'MILLISECOND SECOND MINUTE HOUR DAY WEEKEND WEEKDAY'.split(' ')
        self.time_terms += 'WEEK MONTH YEAR DECADE CENTURY MILLENIUM ERA BC AD B.C. A.D. B.C.E. BCE'.split(' ')
        self.time_terms += [x + 'S' for x in self.time_terms]
        self.time_terms = set(self.time_terms)

    def recognize_time(self, string):
        tokens = string.split(' ')
        for token in tokens:
            if token in self.time_terms:
                return True
        return False

    def get_date_range(self):
        pass
