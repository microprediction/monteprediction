from monteprediction.calendarutil import back_to_weekday
from datetime import timedelta, datetime
from monteprediction import SPDR_ETFS
import yfinance as yf


def get_most_recent_truth():
    end_date = back_to_weekday(datetime.now() - timedelta(days=1))
    start_date = end_date - timedelta(weeks=3)
    recent_data = yf.download(SPDR_ETFS, start=start_date.date(), end=end_date.date(), interval="1wk")
    recent_weekly_prices = recent_data['Adj Close']
    return recent_weekly_prices.pct_change().dropna().iloc[-1].values
