
import os
from dotenv import load_dotenv
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nasdaq_set_up_account = 'https://data.nasdaq.com/account/profile'
detailed_nasdaq_api_info = "https://docs.data.nasdaq.com/docs/in-depth-usage"
company_of_interest = 'https://www.zeiss.com/meditec/int/home.html'

load_dotenv()
KEY = os.getenv('KEY')


url = 'https://data.nasdaq.com/api/v3/' \
      'datasets/FSE/AFX_X.json' \
      '?collapse=Date' \
      '&start_date=2017-01-01' \
      '&end_date=2017-12-31' \
      '&api_key=sahUUE2GjnUSHDYGayzp'


# Package the request, send the request and catch the response: r
r = requests.get(url)

# Decode the JSON data into a dictionary: json_data
json_data = r.json()

k_info = json_data['dataset']
afx_df = pd.DataFrame(k_info['data'], columns=k_info['column_names'])
info = afx_df.info()
desc = afx_df.describe()

# Goals
"""
These are your tasks for this mini project:

1. Collect data from the Franfurt Stock Exchange, for the ticker AFX_X, for the whole year 2017 (keep in mind that the date format is YYYY-MM-DD).
2. Convert the returned JSON object into a Python dictionary.
3. Calculate what the highest and lowest opening prices were for the stock in this period.
4. What was the largest change in any one day (based on High and Low price)?
5. What was the largest change between any two days (based on Closing Price)?
6. What was the average daily trading volume during this year?
7. (Optional) What was the median trading volume during this year. (Note: you may need to implement your own function for calculating the median.)
"""

#
#
# twenty_17 = "https://data.nasdaq.com/api/v3/datasets/FSE/AFX_X.json?" \
#             "Date=7-01-01&Date=2017-12-31&api_key=sahUUE2GjnUSHDYGayzp"
# # Package the request, send the request and catch the response: r
# r = requests.get(twenty_17)
# textin = r.text
#
# # Decode the JSON data into a dictionary: json_data
# json_data_2017 = r.json()
