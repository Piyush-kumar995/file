import datetime
import pytz
import numpy as np


class DateUtility:

    def __init__(self):
        self.holidays = {}
        with open('holidays.dat', 'r') as f:
            for line in f:
                tz, date, holiday = line.strip().split(',')
                date = datetime.datetime.strptime(date, '%Y%m%d').date()
                self.holidays.setdefault(tz, []).append((date, holiday))

    def convert_dt(self, from_date, from_tz, to_tz):
        from_tz = pytz.timezone(from_tz)
        to_tz = pytz.timezone(to_tz)
        from_date = from_tz.localize(from_date)
        return from_date.astimezone(to_tz)

    def add_dt(self, from_date, days):
        return from_date + datetime.timedelta(days=days)

    def sub_dt(self, from_date, days):
        return from_date - datetime.timedelta(days=days)

    def get_days(self, from_date, to_date):
        return (to_date - from_date).days

    def get_days_exclude_we(self, from_date, to_date):
        weekdays = 0
        current_date = from_date
        while current_date < to_date:
            if current_date.weekday() < 5:  # Monday through Friday
                weekdays += 1
            current_date += datetime.timedelta(days=1)
        return weekdays

    def get_days_since_epoch(self, from_date):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (from_date - epoch).days

    def get_business_days(self, from_date, to_date):
        business_days = 0
        current_date = from_date
        while current_date < to_date:
            if current_date.weekday() < 5:  # Monday through Friday
                for tz, hols in self.holidays.items():
                    for hol in hols:
                        hol_date, hol_name = hol
                        if current_date == hol_date:
                            break
                    else:
                        continue
                    break
                else:
                    business_days += 1
            current_date += datetime.timedelta(days=1)
        return business_days


def convert_timezone(date_time, from_tz, to_tz):
    from_tz = pytz.timezone(from_tz)
    to_tz = pytz.timezone(to_tz)
    return from_tz.localize(date_time).astimezone(to_tz)


def add_subtract_days(date, days):
    return date + datetime.timedelta(days=days)


def days_between_dates(date1, date2):
    return (date2 - date1).days


def weekdays_between_dates(date1, date2):
    days = np.busday_count(date1, date2)
    return days


def days_since_epoch(date):
    return (date - datetime.datetime(1970, 1, 1)).days


def business_days_between_dates(date1, date2, holidays):
    weekdays = np.busday_count(date1, date2, holidays=['2022-12-25'])
    business_days = weekdays

    return business_days


date_time = datetime.datetime.now()
converted_time = convert_timezone(date_time, "UTC", "US/Eastern")
print("converted time is-", converted_time)

date = datetime.date(2022, 7, 4)
new_date = add_subtract_days(date, 12)
print("new dates are-", new_date)

date1 = datetime.date(2022, 7, 4)
date2 = datetime.date(2022, 7, 15)
days = days_between_dates(date1, date2)
print("No of days between day 1 and day 2 is -", days)

date1 = datetime.date(2022, 7, 4)
date2 = datetime.date(2022, 7, 11)
weekdays = weekdays_between_dates(date1, date2)
print("No of weekday bwtween day 1 and day 2 is-", weekdays)

date = datetime.datetime(2022, 7, 4)
days = days_since_epoch(date)
print("No of days since EPOCH", days)

date1 = datetime.date(2022, 7, 4)
date2 = datetime.date(2022, 7, 14)
holidays = [datetime.date(2022, 12, 25)]
business_days = business_days_between_dates(date1, date2, holidays)
print("No, of business days ae-", business_days)
