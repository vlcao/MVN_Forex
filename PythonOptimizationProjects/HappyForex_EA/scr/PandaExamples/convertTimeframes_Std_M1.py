'''
Created on Dec 4, 2017

@author: cao.vu.lam
'''

import pandas as pd
import os

# Read in the CSV, parse Date and Time into DateTime, then set this as the index of the returned dataframe 

# Replace back-flash into forward flash 
scrDirName = ''
tempPath = str(os.getcwd()) + '/example_data/'
    
for i in range(len(tempPath)):
    if tempPath[i] == '\\':
        scrDirName += '/'
    else:
        scrDirName += tempPath[i]
file_name = scrDirName + 'AUDUSD1_9ys_header.csv'

df = pd.read_csv(file_name,
            parse_dates={'DateTime': ['Date', 'Time']},
            usecols=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            na_values=['nan']).set_index('DateTime')


# Created a dictionary to tell Pandas how to re-sample, if this isn't in place it will re-sample each column separately 
ohlc_dict = {
    'Open':'first',
    'High':'max',
    'Low':'min',
    'Close':'last',
    'Volume':'sum'
}
# Resample to 15Min (this format is needed) as per ohlc_dict, then remove any line with a NaN
# df = df.resample('15Min', how=ohlc_dict).dropna(how='any') 
df = df.resample('15Min').agg(ohlc_dict).dropna(how='any') 

# Resample mixes the columns so lets re-arrange them 
cols = ['Open', 'High', 'Low', 'Close', 'Volume']  
df = df[cols]

# Write out to CSV
M15FilePath = scrDirName + 'AUDUSD1_9ys_M15.csv'
df.to_csv(M15FilePath)
print('Convert successful!!!')
