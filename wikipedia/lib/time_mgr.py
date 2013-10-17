from datetime import datetime
from wikipedia.models import *


class TimeManager():

    def __init__(self):
        self.month_names = "JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER".split(' ')
        self.short_month_names = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(' ')
        self.time_terms = 'MILLISECOND SECOND MINUTE HOUR DAY WEEKEND WEEKDAY YESTERDAY TODAY TOMORROW BEFORE AFTER'.split(' ')
        self.time_terms += 'WEEK MONTH YEAR DECADE CENTURY MILLENIUM ERA BC AD B.C. A.D. B.C.E. BCE'.split(' ')
        self.time_terms += [x + 'S' for x in self.time_terms]
        self.time_terms = set(self.time_terms)

    def recognize_time(self, item):
        string = None
        if isinstance(item, str) or isinstance(item, unicode):
            string = item
        else:
            string = item.name

        tokens = string.split(' ')
        for token in tokens:
            if token in self.time_terms:
                return True
        return False

    def get_date_range(self):
        pass

    def is_day(self, number):
        if isinstance(number, Number):
            if number.number > 0 and number.number <= 31:
                return True
        return False

    def is_month(self, concept):
        if isinstance(concept, Concept):
            if concept.name in self.month_names or concept.name in self.short_month_names:
                return True
        return False

    def is_year(self, number):
        if isinstance(number, Number):
            if number.number >= 0 and number.number < 10000:
                return True
        return False
