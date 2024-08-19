import requests
import json
import pandas as pd
import numpy as np
from dateutil import parser


def convert_date(date_string):
    try:
        dt = parser.parse(date_string.replace('_', '-'))
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return date_string


API_BASE = 'https://www.monteprediction.com/api/'


def get_weekly():
    # Get weekly scores
    response = requests.get(API_BASE + 'weekly')
    data = json.loads(response.json()['data'])
    return pd.DataFrame(data)


def get_implied():
    # Get (stale) implied vols
    response = requests.get(API_BASE + 'implied')
    data = json.loads(response.json()['data'])
    return pd.DataFrame(data)


def get_truth(expiry: str):
    # Get "official" truth ... weekly returns
    expiry_underscore = convert_date(expiry).replace('-', '_')
    response = requests.get(API_BASE + 'truth/' + expiry_underscore)
    data = json.loads(response.json()['data'])
    return pd.DataFrame(data)


def get_truth_expiries():
   response = requests.get(API_BASE + 'truth')

   if response.status_code == 200:
      data = response.json()['available_dates']
      return data  # Assuming the data is a list of date strings in 'YYYY_MM_DD' format
   else:
      print(f"Failed to fetch available dates: {response.status_code}")
      return []


def get_truths(pivot=True) -> pd.DataFrame:
    """
    Fetches and combines truth data for all available dates.

    """
    available_dates = get_truth_expiries()
    all_data = []

    for expiry in available_dates:
        df = get_truth(expiry)
        if not df.empty:
            df['date'] = expiry  # Add date column for reference
            all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    if pivot:
        pivoted_df = combined_df.pivot(index='date', columns='ticker', values='return')
        return pivoted_df
    else:
        return combined_df


def get_mean(expiry: str):
    # Get historical community mean estimate
    expiry_underscore = convert_date(expiry).replace('-', '_')
    response = requests.get(API_BASE + '/moments/mean/' + expiry_underscore)
    data = json.loads(response.json()['data'])
    return pd.DataFrame(data)


def get_covariance(expiry: str) -> pd.DataFrame:
    # Get historical community covariance estimate
    expiry_underscore = convert_date(expiry).replace('-', '_')
    url = API_BASE + 'moments/covariance/' + expiry_underscore
    response = requests.get(url)
    data = json.loads(response.json()['data'])
    tickers = data['columns']
    data_matrix = pd.DataFrame(data['data'], index=tickers, columns=tickers)
    return data_matrix


def get_std(expiry: str) -> pd.Series:
    # Get historical community standard deviations
    cov = get_covariance(expiry=expiry)
    index = cov.index
    devo = np.sqrt(np.diag(cov.values))
    return pd.Series(devo, index=index)


def get_correlation(expiry: str) -> pd.DataFrame:
    # Get historical community correlations
    cov = get_covariance(expiry=expiry)
    index = cov.index
    columns = cov.columns
    devo = np.sqrt(np.diag(cov.values))
    corr = cov.values / np.outer(devo, devo)
    np.fill_diagonal(corr, 1)
    return pd.DataFrame(corr, index=index, columns=columns)
