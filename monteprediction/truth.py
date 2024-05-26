from monteprediction.calendarutil import back_to_weekday
from datetime import timedelta, datetime
from monteprediction import SPDR_ETFS
import yfinance as yf

# For the "official" ground truth see https://github.com/microprediction/monteprediction/blob/main/monteprediction/api.py

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
