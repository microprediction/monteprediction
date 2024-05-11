from monteprediction import SPDR_ETFS
import yfinance as yf
import numpy as np
import scipy.stats as stats
from datetime import datetime, timedelta
import pandas as pd

#  For retrieving implied weekly ATM ETF volatilities and weekly return standard deviations from yfinance
#  See get_weekly_options() in particular

def get_days_until_expiration(expiration_date):
    today = datetime.now().date()  
    delta = expiration_date - today
    weekend_days = sum(1 for i in range(delta.days + 1) if (today + timedelta(days=i)).weekday() > 4)
    return delta.days, weekend_days

def get_current_price(stock):
    # Attempt to retrieve a price in various ways
    try:
        return stock.info['regularMarketPrice']
    except KeyError:
        # Try alternative methods if regularMarketPrice is not available
        try:
            return (stock.info['bid'] + stock.info['ask']) / 2
        except KeyError:
            # Fallback to previous close if no live price is available
            return stock.info.get('previousClose', float('nan'))
          
def adjust_volatility(annual_vol, total_days, weekend_days):
    # Assume weekend days contribute 1/3 of the volatility of a weekday
    effective_days = total_days - weekend_days + (weekend_days * 0.3)
    # Adjust annual volatility to the effective number of days
    return annual_vol * (effective_days / 365)**0.5

def fetch_weekly_options_for_ticker(ticker):
    stock = yf.Ticker(ticker)
    exp_dates = stock.options
    if not exp_dates:
        return None

    today = datetime.now().date()
    valid_expirations = [datetime.strptime(date, '%Y-%m-%d').date() for date in exp_dates if datetime.strptime(date, '%Y-%m-%d').date() >= today]
    if not valid_expirations:
        return None

    closest_expiration = min(valid_expirations)
    days_until_expiration, weekend_days = get_days_until_expiration(closest_expiration)
    try:
        opts = stock.option_chain(closest_expiration.strftime('%Y-%m-%d'))
        current_price = get_current_price(stock)
        calls = opts.calls
        puts = opts.puts

        atm_call = calls.iloc[(calls['strike'] - current_price).abs().argsort()[0]]
        atm_put = puts.iloc[(puts['strike'] - current_price).abs().argsort()[0]]

        adjusted_call_iv = adjust_volatility(atm_call['impliedVolatility'], days_until_expiration, weekend_days)
        adjusted_put_iv = adjust_volatility(atm_put['impliedVolatility'], days_until_expiration, weekend_days)
        
        return {
            'ticker': ticker,
            'retrievalTime': datetime.now(),
            'callStrike': atm_call['strike'],
            'callPrice': atm_call['lastPrice'],
            'originalCallIV': atm_call['impliedVolatility'],
            'adjustedCallIV': adjusted_call_iv,
            'putStrike': atm_put['strike'],
            'putPrice': atm_put['lastPrice'],
            'originalPutIV': atm_put['impliedVolatility'],
            'adjustedPutIV': adjusted_put_iv
        }
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None


def get_weekly_options():
   df_data = [fetch_weekly_options_for_ticker(etf) for etf in SPDR_ETFS if fetch_weekly_options_for_ticker(etf)]
   df = pd.DataFrame(df_data)
   if not df.empty:
        df['impliedStd'] = (df['adjustedCallIV'] + df['adjustedPutIV']) / 2  # Average of adjusted IVs as implied std
   return df 

def get_weekly_implied()->dict:
   df =  get_weekly_options()
   return dict(zip(df['ticker'].values,df['impliedStd'].values))
