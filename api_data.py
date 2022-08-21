import os
from dotenv import load_dotenv
import requests
import pandas as pd

nasdaq_set_up_account = 'https://data.nasdaq.com/account/profile'
detailed_nasdaq_api_info = "https://docs.data.nasdaq.com/docs/in-depth-usage"
company_of_interest = 'https://www.zeiss.com/meditec/int/home.html'

load_dotenv()
KEY = os.getenv('KEY')


def diff(high,low):
	return high - low


def median(a_list):
	if len(a_list) % 2 != 0:
		return a_list[int((len(a_list) + 1) / 2)]
	the_length = len(a_list)
	return a_list[the_length + 1] + a_list[the_length -1] /2


################################################################################
# 1. Collect data from the Franfurt Stock Exchange, for the ticker AFX_X,
# for the whole year 2017 (keep in mind that the date format is YYYY-MM-DD).
url = 'https://data.nasdaq.com/api/v3/' \
      'datasets/FSE/AFX_X.json' \
      '?collapse=Date' \
      '&start_date=2017-01-01' \
      '&end_date=2017-12-31' \
      '&api_key=sahUUE2GjnUSHDYGayzp'

################################################################################
# 2. Convert the returned JSON object into a Python dictionary.
r = requests.get(url)
json_data = r.json()

###### Some Preparation ########################################################
k_info = json_data['dataset']
afx_df = pd.DataFrame(k_info['data'],columns=k_info['column_names'])
afx_df.drop(axis=1,inplace=True,columns=['Last Price of the Day',
                                         'Daily Traded Units','Daily Turnover'])

################################################################################
# 3. Calculate what the highest and lowest opening prices were for the stock in
# this period.
high = afx_df.iloc[afx_df['Open'].idxmax()]['Open']
low = afx_df.iloc[afx_df['Open'].idxmin()]["Open"]

###### DETOUR FOR SOME WRANGLING ###############################################
# will not drop this row because the needed information to calculate value was
# present, namely the 'Change'
change_locale = afx_df[afx_df['Change'].notnull()].index.tolist()
fix_one_with_change_value = afx_df.at[change_locale[0],'Open'] = \
	afx_df.loc[169,'Change'] + afx_df.loc[169,'Close']

# will drop the remaining two null rows because losing 2 values in a over 200
# with change values less than 1 will not make a large difference
open_locale = afx_df[afx_df['Open'].isnull()].index.tolist()
afx_df.drop(open_locale,inplace=True)

################################################################################
# 4. What was the largest change in any one day (based on High and Low price)?
afx_df['Change'] = afx_df['Open'] - afx_df['Close']
hi_lo = afx_df[['High','Low']]
hi_lo['Diff'] = hi_lo[['High','Low']]. \
	apply(lambda hi_lo: diff(hi_lo['High'],hi_lo['Low']),axis=1)
top = hi_lo.iloc[hi_lo.idxmax()['Diff']]
largest_difference = afx_df[(afx_df['High'] == top["High"]) & (afx_df['Low'] ==
                                                               top["Low"])]
################################################################################
# 5. What was the largest change between any two days (based on Closing Price)?
largest_day_close_diff = afx_df.iloc[afx_df['Close'].diff().idxmax()]
l = afx_df['Close'].diff().max()

################################################################################
# 6. What was the average daily trading volume during this year?
avg_volume = afx_df['Traded Volume'].mean()

################################################################################
# 7. (Optional) What was the median trading volume during this year. (Note: you
# may need to implement your own function for calculating the median.)
listin_vols = sorted(list(afx_df['Traded Volume']))
middle_val_is = median(listin_vols)

print(f'3. The highest and lowest opening prices for the stock in this period '
      f'were:\n {high}(high) and {low}(low)\n\n'
      f'4. The largest change in any one day (based on High and Low price) '
      f'was on {largest_difference.iat[0, 0]} and the change was: '
      f'{round(top["Diff"], 2)}\n\n'
      f'5. The largest change between any two days (based on Closing Price) '
      f'occurred after close on {afx_df.iloc[99, 0]} and the change at opening'
      f' was {round(l, 2)}\n\n'
      f'6. The average daily traing volume was:\n{avg_volume}\n\n'
      f'7. The median trading volume during 2017 was: \n{middle_val_is}')
