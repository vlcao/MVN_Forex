'''
Created on Oct 2, 2017

@author: cao.vu.lam
'''
from DataHandler.hardcoded_data import combine_all_files_in_a_folder, \
    FOLDER_DATA_OUTPUT, SYMBOL, FILENAME_ORDER_CLOSED_HISTORY
DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1
TIME_STAMP_FORMAT = '%Y.%m.%d_%H.%M.%S.%f'



# write out other data for reference
combine_all_files_in_a_folder(FOLDER_DATA_OUTPUT + SYMBOL + '/Jan_Nov2016',
                              FOLDER_DATA_OUTPUT + SYMBOL + '/' + 'Jan_Nov2016.csv',
                              '*.csv')

# import os
# import glob
# 
# #===============================================================================
# def convert_backflash2forwardflash(backflash_path):
#     forwardflash_path = ''
#      
#     # replace the back flash with forward flash
#     for i in range(len(backflash_path)):
#         if backflash_path[i] == '\\':
#             forwardflash_path += '/'
#         else:
#             forwardflash_path += backflash_path[i]
#          
#     return forwardflash_path
#  
# #===============================================================================
# # convert the back flash with forward flash (just in case)
# folder_name = convert_backflash2forwardflash('E:\EclipsePreferences-csse120-2011-06\HappyForex\src\DataHandler\data\input\USDJPY\USDJPY_Ticks_May2009_Nov2016_Modified_2')
# allFiles = glob.glob(folder_name + '/*.csv')
# 
# for file_ in allFiles:
#     print(os.path.basename(file_))
# #===============================================================================
# import glob
# import csv
#
# #===============================================================================
# combine_all_files_in_a_folder('E:\EclipsePreferences-csse120-2011-06\Happy Forex\src\DataHandler\data\input\USDJPY\USDJPY_Ticks_May2009_Nov2016_Modified_2',
#                               'E:\EclipsePreferences-csse120-2011-06\Happy Forex\src\DataHandler\data\output\USDJPY\USDJPY_Ticks_May2009_May2010.csv')
# print("Completed!!!")
#
# #===============================================================================
# from datetime import datetime
# import time
# from datetime import date
# from DataHandler.hardcoded_data import convert_string_day2float, \
#     convert_string_millisecond2float, convert_string_datetime2float
# 
# MARKET_TIME_STANDARD = '1970.01.01_00:00:00,000'
# DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S,%f'
#      
# ts, ms = '20.12.2016 09:38:42,76'.split(',')
# dt = datetime.strptime(ts, '%d.%m.%Y %H:%M:%S')
# print(dt)
# print(time.mktime(dt.timetuple()))
#      
# print('%f' % (time.mktime(dt.timetuple()) * 1000 + int(ms) * 10))
# print(convert_string_datetime2float('1970.02.02_01:01:00,000', MARKET_TIME_STANDARD, DATETIME_FORMAT))
# print(convert_string_day2float('1970.01.02_01:30:00,000', MARKET_TIME_STANDARD, DATETIME_FORMAT))
# print(convert_string_millisecond2float('1970.01.25_10:01:00,000', MARKET_TIME_STANDARD, DATETIME_FORMAT))
#      
# print('#===============================================================================')
# hr_min_sec_ms = convert_string_millisecond2float('2009.05.01_04:30:02,624', MARKET_TIME_STANDARD, DATETIME_FORMAT)
# print(hr_min_sec_ms)
#  
# # time = 16202624
# milliseconds = hr_min_sec_ms % 1000
# print("==> milliseconds = %s" % milliseconds)
#  
# hr_min_sec = int(hr_min_sec_ms / 1000) 
# print("==> hr_min_sec = %s" % hr_min_sec)
# 
# hour = int(hr_min_sec / 3600)
# print("==> hour = %s" % hour)
# 
# minute = int(hr_min_sec % 3600 / 60)
# print("==> minute = %s" % minute)
#  
# minutes, seconds = divmod(int(day_hr_min_sec), 60)
# hours, minutes = divmod(int(day_hr_min_sec), 60)
#  
# print "%02d:%02d:%02d" % (hours, minutes, seconds)

# #===============================================================================
# DATEOFFSET = 719163  # total days from '0001.01.01_00:00:00,000' to '1970.01.01_00:00:00,000'
# today = datetime.date.fromordinal(DATEOFFSET + 14365)
# print(today)
# 
# 
# dividend = str(today).split('-')
# year = dividend[0]
# month = dividend[1]
# day = dividend[2]
# print(year)
# print(month)
# print(day)
# 
# ''' (0-Monday,1,2,3,4,5,6) '''
# print(date(int(year), int(month), int(day)).weekday())
# 

# #====================================================================
# raw_input("Press Enter to continue...")       
# 
# #====================================================================
# s = 'Hello, world.'
# 
# print(str(s))
# print(repr(s))
# 
# #====================================================================
# import os
# import glob
# 
# print(os.path.dirname(os.getcwd()))
# print(os.getcwd())
#
# #====================================================================
# print(os.path.isfile('exampleCsv.csv'))
# statinfo = os.stat('exampleCsv.csv')
# print(statinfo)
