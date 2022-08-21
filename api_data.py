
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

afx_df.drop(axis=1, inplace=True, columns=['Last Price of the Day', 'Daily Traded Units', 'Daily Turnover'])

info1 = afx_df.info()
desc1 = afx_df.describe()

#high Low
high = afx_df.iloc[afx_df['Open'].idxmax()]['Open']
low = afx_df.iloc[afx_df['Open'].idxmin()]["Open"]

# will not drop this row because the needed information to calculate value was present
change_locale = afx_df[afx_df['Change'].notnull()].index.tolist()
fix_one_with_change_value = afx_df.at[change_locale[0], 'Open'] = afx_df.loc[169, 'Change'] + afx_df.loc[169, 'Close']

# will drop the remaining two null rows because losing 2 values in a over 200 with change values less than 1 will not make a large difference
open_locale = afx_df[afx_df['Open'].isnull()].index.tolist()
afx_df.drop(open_locale, inplace=True)

afx_df['Change'] = afx_df['Open'] - afx_df['Close']







