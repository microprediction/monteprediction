from monteprediction.calendarutil import back_to_weekday
from datetime import timedelta, datetime
from monteprediction import SPDR_ETFS
import yfinance as yf

# For the "official" ground truth see https://github.com/microprediction/monteprediction/blob/main/monteprediction/api.py
# Code used to produce those is provided here for transparency (and so you can debug it :)

from datetime import datetime
MONDAY_HOLIDAYS = [
    datetime(2024, 1, 1),   # New Year's Day (observed)
    datetime(2024, 1, 15),  # Martin Luther King Jr. Day
    datetime(2024, 2, 19),  # Presidents' Day
    datetime(2024, 5, 27),  # Memorial Day
    datetime(2024, 9, 2)    # Labor Day
]

def get_previous_monday(date):
    """
    If it is Monday, return date
    Otherwise return the date of the previous Monday
    """
    days_to_subtract = (date.weekday() - 0) % 7
    if days_to_subtract == 0:
        return date
    previous_monday = date - timedelta(days=days_to_subtract)
    return previous_monday



def get_previous_tuesday(date):
    """
    If it is Tuesday, return date
    Otherwise return the date of the previous Tuesday
    """
    days_to_subtract = (date.weekday() - 1) % 7
    if days_to_subtract == 0:
        return date
    previous_tuesday = date - timedelta(days=days_to_subtract)
    return previous_tuesday


def get_truth(expiry):
    """
        Get the weekly change Monday close to Monday close
    """
    if expiry in MONDAY_HOLIDAYS:
        print('Its a long weekend!')
        end_date = get_previous_tuesday(expiry + timedelta(days=1))
    else:
        end_date = get_previous_monday(expiry)
    start_date = end_date - timedelta(weeks=3)
    recent_data = yf.download(SPDR_ETFS, start=start_date, end=end_date, interval="1wk")
    recent_weekly_prices = recent_data['Adj Close']
    truth = recent_weekly_prices.pct_change().dropna().iloc[-1]
    return truth
