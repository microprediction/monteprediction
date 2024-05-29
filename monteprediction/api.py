import requests
import json
import pandas as pd 
import numpy as np 
from dateutil import parser

def convert_date(date_string):
    try:
        dt = parser.parse(date_string)
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return "Invalid date format"

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

def get_truth(expiry:str):
   # Get "official" truth ... weekly returns
   expiry_underscore = convert_date(expiry).replace('-','_')
   response = requests.get(API_BASE + 'truth/' + expiry_underscore)
   data = json.loads(response.json()['data'])
   return pd.DataFrame(data)

def get_mean(expiry:str):
   # Get historical community mean estimate
   expiry_underscore = convert_date(expiry).replace('-','_')
   response = requests.get(API_BASE + '/moments/mean/' + expiry_underscore)
   data = json.loads(response.json()['data'])
   return pd.DataFrame(data)

def get_covariance(expiry:str)->pd.Dataframe:
   # Get historical community covariance estimate
   expiry_underscore = convert_date(expiry).replace('-','_')
   url = API_BASE + 'moments/covariance/' + expiry_underscore
   response = requests.get(url)
   data = json.loads(response.json()['data'])
   tickers = data['columns']
   data_matrix = pd.DataFrame(data['data'], index=tickers, columns=tickers)
   return data_matrix

def get_std(expiry:str)->pd.Series:
    cov = get_covariance(expiry=expiry)
    index = cov.index
    devo = np.sqrt(np.diag(cov.values))
    return pd.Series(devo, index=index)

def get_correlation(expiry:str)->pd.Dataframe:
    cov = get_covariance(expiry=expiry)
    index = cov.index
    devo = np.sqrt(np.diag(cov.values))
    outer_std_devs = np.outer(std_devs, std_devs)
    corr_matrix = cov_matrix / outer_std_devs
    np.fill_diagonal(corr_matrix, 1)
    corr_matrix_df = pd.DataFrame(corr_matrix, index=index, columns=columns)
    return corr_matrix_df
    
    
    
    
