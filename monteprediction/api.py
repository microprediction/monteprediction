import requests
import json
import pandas as pd 

API_BASE = 'https://www.monteprediction.com/api/'

def get_implied():
   # Get relative implied vols
   response = requests.get(API_BASE + 'implied')
   data = json.loads(response.json()['data'])
   return pd.DataFrame(data)
