import requests
import json
import pandas as pd 
from dateutil import parser

def convert_date(date_string):
    try:
        dt = parser.parse(date_string)
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        # Handle cases where the date string is not recognized
        return "Invalid date format"

API_BASE = 'https://www.monteprediction.com/api/'

def get_implied():
   # Get relative implied vols
   response = requests.get(API_BASE + 'implied')
   data = json.loads(response.json()['data'])
   return pd.DataFrame(data)

def get_truth(expiry:str):
   # Get "official" truth ... weekly returns
   expiry_underscore = convert_date(expiry).replace('-','_')
   response = requests.get(API_BASE + 'truth/' + expiry_underscore)
   data = json.loads(response.json()['data'])
   return pd.DataFrame(data)
