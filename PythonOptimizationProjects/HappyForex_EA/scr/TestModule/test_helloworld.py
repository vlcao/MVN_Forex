'''
Created on Oct 2, 2017

@author: cao.vu.lam
'''
DEFAULT_NUMBER_INT = 0
DEFAULT_SECOND_NUMBER_INT = 1
DEFAULT_NUMBER_FLOAT = 0.00
DEFAULT_SECOND_NUMBER_FLOAT = 1.00
SECONDS_OF_ADAY = 86400

TIME_STAMP_FORMAT = '%Y.%m.%d_%H.%M.%S'

import os
import csv
import glob
from datetime import datetime

import numpy as np

import sys
BID_COL_INDEX = 3


#===============================================================================
def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
     
    return a
 
# #===============================================================================
# def iTrueRange(date, close, high, low, open, yesterday_close):
#      
#     count = high - low  # today close
#     y = abs(high - yesterday_close)
#     z = abs(low - yesterday_close)
#      
#     if (y <= count >= z):
#         iTrueRange = count
#     elif (count <= y >= z):
#         iTrueRange = y
#     elif (count <= z >= y):
#         iTrueRange = z
#          
#     return date, iTrueRange    
#  
#      
# #===============================================================================
# sampleData = open(os.path.dirname(os.getcwd()) + '/DataHandler/data/input/sampleData.txt', 'r').read()
# splitData = sampleData.split('\n')
#  
# date, closep, highp, lowp, openp, volumn = np.loadtxt(splitData, delimiter=',', unpack=True)
#  
# count = DEFAULT_SECOND_NUMBER_INT
# TRDates = []
# TrueRanges = []
#  
# while count < len(date):
#     #                       iTrueRange(self, d, c, h, l, o, yc)
#     TRDate, TrueRange = iTrueRange(date[count], closep[count], highp[count], lowp[count], openp[count], closep[count - DEFAULT_SECOND_NUMBER_INT])
#     
#     print TrueRange
#     
#     TRDates.append(TRDate)
#     TrueRanges.append(TrueRange)
#      
#     count += DEFAULT_SECOND_NUMBER_INT
# 
# print TrueRanges
# 
# ATR = ExpMovingAverage(TrueRanges, 14)
# print ATR
#   
# ATR_list = np.array(ATR).tolist()
# print ATR_list


#===============================================================================
def iTrueRange(open, high, low, close, yesterday_close):
    
    count = high - low  # today close
    y = abs(high - yesterday_close)
    z = abs(low - yesterday_close)
    
    if (y <= count >= z):
        iTrueRange = count
    elif (count <= y >= z):
        iTrueRange = y
    elif (count <= z >= y):
        iTrueRange = z
        
    return iTrueRange    


#===============================================================================
def ATRPips(atr, size, point):
    
    data_col = len(atr[DEFAULT_NUMBER_INT]) 
    data_row = len(atr)
    atr_pips = [[DEFAULT_NUMBER_FLOAT for x in range(data_col)] for y in range(data_row)] 
    
    for row_count in range(size):
        for col_count in range(len(atr[row_count])):
            atr_pips[row_count][col_count] = int(float(atr[row_count][col_count]) / point)
    
    return atr_pips


#===============================================================================
def ohlc_resample(timeframe_tickdata):
    ''' Convert the Bid price from Tick data into Open, High, Low, Close price '''
    
    # get open and close bid price
    openp = timeframe_tickdata[DEFAULT_NUMBER_INT][BID_COL_INDEX]
    closep = timeframe_tickdata[len(timeframe_tickdata) - DEFAULT_SECOND_NUMBER_INT][BID_COL_INDEX]
    
    # get high, low of the bid price in this time_frame data
    highp = sys.maxint * -1
    lowp = sys.maxint
    for tick in timeframe_tickdata:
        bid_price = tick[BID_COL_INDEX]
        
        # get high and low price
        if (bid_price >= highp):
            highp = bid_price
        if (bid_price < lowp):
            lowp = bid_price
            
    return [openp, highp, lowp, closep]


#===============================================================================
def iATR(period, shift):
    ''' ATR function '''
    
    yesterday_close = 107.544
    TIMEFRAME_OHLC_DATA = [[107.544, 107.546, 107.535, 107.535],
                           [107.544, 107.546, 107.535, 107.535],
                           [107.544, 107.546, 107.535, 107.535],
                           [107.544, 107.546, 107.535, 107.535],
                           [107.544, 107.546, 107.535, 107.535],
                           [107.544, 107.546, 107.535, 107.535],
                           [107.544, 107.546, 107.535, 107.535]]
    TIMEFRAME_TICK_DATA = [[1413133217.0, 16355.0, 61217, 107.534, 107.554],
                           [1413133218.0, 16355.0, 61218, 107.546, 107.566],
                           [1413133218.0, 16355.0, 61218, 107.553, 107.573],
                           [1413133218.0, 16355.0, 61218, 107.564, 107.584],
                           [1413133220.0, 16355.0, 61220, 107.565, 107.585],
                           [1413133220.0, 16355.0, 61220, 107.557, 107.577],
                           [1413133220.0, 16355.0, 61220, 107.559, 107.579],
                           [1413133221.0, 16355.0, 61221, 107.558, 107.578],
                           [1413133222.0, 16355.0, 61222, 107.554, 107.574],
                           [1413133223.0, 16355.0, 61223, 107.553, 107.573]]
    
    if len(TIMEFRAME_OHLC_DATA >= period):
    
        # calculate open, high, low, close of the bid price following the TIME FRAME 
        TIMEFRAME_OHLC_DATA.append(ohlc_resample(TIMEFRAME_TICK_DATA))
        print("TIMEFRAME_OHLC_DATA")
        print TIMEFRAME_OHLC_DATA
        
        # calculate the True Range and ATR
        TrueRanges = []
        open_inx_col = 0
        high_inx_col = 1
        low_inx_col = 2
        close_inx_col = 3
        
        for rate in TIMEFRAME_OHLC_DATA:
            openp = float(str(rate[open_inx_col]))
            highp = float(str(rate[high_inx_col]))
            lowp = float(str(rate[low_inx_col]))
            closep = float(str(rate[close_inx_col]))
            
            TrueRange = iTrueRange(openp, highp, lowp, closep, yesterday_close)
    
            # save TrueRange into an array for ATR calculation            
            TrueRanges.append(TrueRange)
         
        ATR = ExpMovingAverage(TrueRanges, period)
        ATR_list = np.array(ATR).tolist()
        
        print("ATR_list:")
        print ATR_list
    else:
        ATR_list = []
        
    return ATR_list


#===============================================================================
atr = [DEFAULT_NUMBER_FLOAT for i in range(12)]
 
# calculate the ATR
for i in range(12):
    # iATR(): Calculates the Average True Range indicator and returns its value.
    atr[i] = iATR(7, i)
   
# calculate the ATR_PIP
atr_pips = ATRPips(atr, 12, 0.01)
print("atr_pips:")
print atr_pips

# 
# 
# # #===============================================================================
# # ''' suppress scientific notation '''
# # a = 1.515324132e+12
# # print('%f' % a)
# # print('%.2f' % a)
# # 
# #===============================================================================
# def convert_backflash2forwardflash_change_output_folder(backflash_path):
#     ''' convert back flash to forward flash and change the path name from 
#     "input" folder into "output" folder '''
#      
#     forwardflash_path = ''
#      
#     # replace the back flash with forward flash
#     i = DEFAULT_NUMBER_INT
#     while (i < len(backflash_path)):
#         if backflash_path[i] == '\\':
#             forwardflash_path += '/'
#         elif (backflash_path[i] == 'i' 
#               and backflash_path[i + 1] == 'n' 
#               and backflash_path[i + 2] == 'p' 
#               and backflash_path[i + 3] == 'u' 
#               and backflash_path[i + 4] == 't'):
#              
#             forwardflash_path += 'o'
#             forwardflash_path += 'u'
#             forwardflash_path += 't'
#             forwardflash_path += 'p'
#             forwardflash_path += 'u'
#             forwardflash_path += 't'
#              
#             i = i + 4
#              
#         else:
#             forwardflash_path += backflash_path[i]
#              
#         i += DEFAULT_SECOND_NUMBER_INT
#                  
#     return forwardflash_path
# 
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
#    
# #===============================================================================
# def convert_string_datetime2float_no_ms(convert_datetime, std_datetime, sformat):
#     ''' Convert a string of date and time with its standard time and format into seconds in float type '''
#      
#     # parse the time format using strptime.
#     convert_datetime = datetime.strptime(convert_datetime, sformat)  
#     std_date = datetime.strptime(std_datetime, sformat)  # standard date
#         
#     # calculate difference between convert_datetime and std_date by milliseconds
#     diff_time = convert_datetime - std_date
#      
#     # convert the different milliseconds into float
#     diff_time_seconds = float(diff_time.days * SECONDS_OF_ADAY + diff_time.seconds)
#      
#     return diff_time_seconds  
# 
#  
# #===============================================================================
# def convert_string_day2float(convert_datetime, std_datetime, sformat):
#     ''' Convert a string of date and time with its standard time and format into float 
#     of total days only '''
#  
#     convert_datetime = datetime.strptime(convert_datetime, sformat)  
#     std_date = datetime.strptime(std_datetime, sformat)  # standard date
#      
#     # calculate difference between convert_datetime and std_date
#     diff_time = convert_datetime - std_date
#      
#     # convert the different days into total float
#     return float(diff_time.days)    
# 
#  
# #===============================================================================
# def convert_string_second2float(convert_datetime, std_datetime, sformat):
#     ''' Convert a string of date and time with its standard time and format into float 
#     which is sum of total seconds '''
# 
#     # parse the time format using strptime.
#     convert_datetime = datetime.strptime(convert_datetime, sformat)  
#     std_date = datetime.strptime(std_datetime, sformat)  # standard date
#     
#     # calculate difference between convert_datetime and std_date
#     diff_time = convert_datetime - std_date
#     
#     return diff_time.seconds   
# 
#  
# #===============================================================================
# def create_a_new_row_forexfactory_format(row):
#     ''' For FOREXFACTORY Calendar Data Format. 
#     ==> Analyze the string separated by Space to get [Date Time, Symbol, Impact Level] and then create a new version 
#     of that row as [Date_Time, Date, Time, Symbol, Impact Level]
#     Ex: [2009-05-01 00:00:00, ALL, 2] 
#         ==> [1241136000296.0, 14365.0, 000.0, ALL, 2] '''
#     
#     # GAIN Capital tick data from 2007 to 2014
#     datetime_col_index = 0
#     symbol_col_index = 1
#     impact_col_index = 2
#     
#     if (row[datetime_col_index] != '0'):
#         # --> get the part BEFORE (Date) and AFTER (Time) the Space
#         split_space = row[datetime_col_index].split(' ')
#          
#         date_part = split_space[DEFAULT_NUMBER_INT]
#         time_second_part = split_space[DEFAULT_SECOND_NUMBER_INT]
#          
#         # --> format the date time as expected WITHOUT millisecond
#         date_modified_part = ('' + date_part.replace('-', '.') + '_' + time_second_part.split('.')[DEFAULT_NUMBER_INT])
#         
#         fdatetime_modified_part = convert_string_datetime2float_no_ms(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
#         fday_modified_part = convert_string_day2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
#         ftime_modified_part = convert_string_second2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
#         
#         # --> create a new row for Tick data
#         new_row = ['%.1f' % fdatetime_modified_part, fday_modified_part, ftime_modified_part, row[symbol_col_index], float(row[impact_col_index])]
#     else:
#         # --> create a new row for Tick data
#         new_row = row
#     
#     return new_row
# 
#  
# #===============================================================================
# def create_multiple_calendar_data_from_wholefolder_forexfactory_format(folder_name):
#     ''' For FOREXFACTORY Calendar Data Format. 
#     ==> Read each row of all Original Tick data file [Date Time, Symbol, Impact Level], 
#     create a new version of that row, and then
#     combine them by writing each new version row into 1 new CSV file 
#     Ex: [2009-05-01 00:00:00, ALL, 2] 
#         ==> [1241136000296.000000, 14365.0, 000.0, ALL, 2] '''
#      
#     # convert the back flash with forward flash (just in case)
#     folder_name = convert_backflash2forwardflash(folder_name)
#     allFiles = glob.glob(folder_name + '/*.csv')
#      
#     file_index = DEFAULT_SECOND_NUMBER_INT
#     for file_ in allFiles:
#         time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#         file_basename = os.path.basename(file_)
#         print("{0} ==> processing file {1}: {2} ...".format(time_stamp, file_index, file_basename))
#          
#         file_name = convert_backflash2forwardflash_change_output_folder(file_)
#           
#         if (file_index % 10 == DEFAULT_NUMBER_INT):
#             perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
#             time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#             print("{0} ... ==> processing {1}% of the data...".format(time_stamp, perc))
#            
#         # write an array to a CSV file
#         csv_new_row_write = open(file_name, "w")  # "w" indicates that you're writing strings to the file
#                
#         # open the CSV file
#         ifile = open(file_, "rU")
#         reader = csv.reader(ifile, delimiter=",")
#         
#         # create a new version of row with (GAIN Capital Tick Data Format)
#         for row in reader:
#         
#             new_row = (','. join([str(j) for j in create_a_new_row_forexfactory_format(row)])
#                        + "\n")
#             
#             # write to CSV the new row: [Date_Time, Date, Time, Symbol, Impact Level]
#             csv_new_row_write.write(new_row)
#              
#         ifile.close()
#        
#         file_index += DEFAULT_SECOND_NUMBER_INT
#            
#     time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#     print("{0} ==> Completed {1} files!!!".format(time_stamp, file_index - DEFAULT_SECOND_NUMBER_INT))
#  
# #===============================================================================
# 
# 
# # --> format the date time as expected WITHOUT millisecond
# MARKET_TIME_STANDARD = '1970.01.01_00:00:00'
# DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S'
# create_multiple_calendar_data_from_wholefolder_forexfactory_format(os.path.dirname(os.getcwd()) 
#                                                               + '/DataHandler/data/input/economic_calendar_01Jan2007_18Apr2014_original')

# import os
# import glob
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
#     convert_string_millisecond2float, convert_string_datetime2float_no_ms
# 
# ts, ms = '20.12.2016 09:38:42,76'.split(',')
# dt = datetime.strptime(ts, '%d.%m.%Y %H:%M:%S')
# print(dt)
# print(time.mktime(dt.timetuple()))
#      
# print('%f' % (time.mktime(dt.timetuple()) * 1000 + int(ms) * 10))
# print(convert_string_datetime2float_no_ms('1970.02.02_01:01:00,000', MARKET_TIME_STANDARD, DATETIME_FORMAT))
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
