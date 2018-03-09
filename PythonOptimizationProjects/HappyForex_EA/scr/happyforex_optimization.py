'''
Created on Dec 12, 2017

@author: cao.vu.lam
'''
#!/usr/bin/env python

import cProfile
import random
import logging.handlers
import os
import shutil
import sys
import multiprocessing
import csv
import glob
import _strptime

import numpy as np
import pandas as pd

from decimal import Decimal
from math import factorial as f
from astropy.units import day
from multiprocessing.dummy import Pool as ThreadPool
from os import path, remove
from datetime import datetime, date

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

log = logging.getLogger(__name__)

################################################################################
#########################       HARDCODED DATA      ############################
################################################################################
DEFAULT_NUMBER_INT = 0
DEFAULT_SECOND_NUMBER_INT = 1
DEFAULT_NUMBER_FLOAT = 0.00
DEFAULT_SECOND_NUMBER_FLOAT = 1.00

VALUE_COL_INDEX = 1

MONTHS_OF_A_YEAR = 12
DAYS_OF_AYEAR = 360
HOURS_OF_ADAY = 24
MINUTES_OF_ANHOUR = 60
SECONDS_OF_AMINUTE = 60
SECONDS_OF_ADAY = 86400
SECONDS_OF_ANHOUR = 3600
MILLISECONDS_OF_ASECOND = 1000

DATEOFFSET = 719163  # total days from '0001.01.01_00:00:00,000' to '1970.01.01_00:00:00,000' (MARKET_TIME_STANDARD)

OP_BUY = 0.00
OP_SELL = 1.00
OP_BUYLIMIT = 2.00
OP_SELLLIMIT = 3.00
OP_BUYSTOP = 4.00
OP_SELLSTOP = 5.00

DEPOSIT = 100000.00
MAX_FITNESS = 100.00
MAX_LOTS = 0.10
NET_PROFIT = 4167700.35
COMMISSION = 0.75
LEVERAGE = 100.00
ONE_LOT_VALUE = 100000.00

# HEADER_ORDER_DICT = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance'] 
ORDER_TYPE_COL_INDEX = 3
ORDER_ID_COL_INDEX = 4
LOTS_COL_INDEX = 5
PRICE_ENTRY_COL_INDEX = 6
PRICE_EXIT_COL_INDEX = 7
TP_COL_INDEX = 9
PROFIT_COL_INDEX = 10
BALANCE_COL_INDEX = 11

# HEADER_TICK_DATA = [Date_Time, Date, Time, Bid, Ask]
# CALENDAR_DATA = [Date_Time, Date, Time, Symbol, Impact]
DATETIME_COL_INDEX = 0
DAY_COL_INDEX = 1
TIME_COL_INDEX = 2
BID_COL_INDEX = 3
ASK_COL_INDEX = 4
SYMBOL_COL_INDEX = 3
IMPACT_COL_INDEX = 4

# Time frame of each period in seconds
PERIOD_M1 = 60.00
PERIOD_M5 = 300.00
PERIOD_M15 = 900.00
PERIOD_M30 = 1800.00
PERIOD_H1 = 3600.00
PERIOD_H4 = 14400.00
PERIOD_D1 = 86400.00
PERIOD_W1 = 432000.00
PERIOD_MN = 1728000.00

TIME_FRAME = PERIOD_H1
SYMBOL = 'EURUSD'
QUOTE_CURRENCY = 'USD'
BASE_CURRENCY = 'EUR'
ALL_CURRENCY = 'ALL'

RUN_FREQUENCY_1_YEAR = '1'
RUN_FREQUENCY_3_YEAR = '3'
RUN_FREQUENCY_5_YEAR = '5'
RUN_FREQUENCY_7_YEAR = '7'
RUN_FREQUENCY_9_YEAR = '9'

SCR_DIR_PATH = os.getcwd()
FOLDER_DATA_INPUT = SCR_DIR_PATH + '/data/input/'
FOLDER_DATA_OUTPUT = SCR_DIR_PATH + '/data/output/'
FOLDER_TICK_DATA_ORIGINAL = '/USDJPY_GAINCapital_Original'
FOLDER_TICK_DATA_MODIFIED = '/EURUSD_GAINCapital_Modified'
FOLDER_CALENDAR_DATA_ORIGINAL = 'economic_calendar_01Jan2007_18Apr2014_original'
FOLDER_CALENDAR_DATA_MODIFIED = 'economic_calendar_01Jan2007_18Apr2014_modified/'

FILENAME_CALENDAR_DATA = '_NewsEvents_01Jan2007_18Apr2014.csv'
FILENAME_TICK_DATA = '/USDJPY-2009-05.csv'
FILENAME_PARAMETER_DEFAULT = 'default_parameters.csv'
FILENAME_PARAMETER_SETTING_2 = 'parameters_setting_2.csv'
FILENAME_PARAMETER_SETTING_3 = 'parameters_setting_3.csv'
FILENAME_OPTIMIZE_PARAMETER = 'optimized_parameters.csv'
FILENAME_POPULATION_INITIAL = 'population_initial.csv'
FILENAME_POPULATION_FINAL = 'population_final.csv'
FILENAME_LOG_EA = 'HappyForexEA_LogRun.log'
FILENAME_PROFILE_EA = "HappyForexEA_ProfileRun.prof"
FILENAME_LOG_BACKTEST = 'HappyForexBackTest_LogRun.log'
FILENAME_PROFILE_BACKTEST = "HappyForexBackTest_ProfileRun.prof"
FILENAME_BEST_SOLUTION = '_FITNESS_BEST_SOLUTION.csv'
FILENAME_BEST_PARAMETERS = '_WHOLE_BEST_PARAMETERS.csv'
FILENAME_HIGHEST_FITNESS = '_fitness_highest_solution.csv'
FILENAME_HIGHEST_PARAMETERS = '_whole_highest_parameters.csv'
FILENAME_ORDER_CLOSED_HISTORY = 'order_closed_history.csv'
FILENAME_ORDER_OPENED_HISTORY = 'order_opened_history.csv'
FILENAME_ORDER_DELETED_HISTORY = 'order_deleted_history.csv'
FILENAME_DATE_DICT = 'data_date_dict.csv'

MARKET_TIME_STANDARD = '1970.01.01_00:00:00'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S'
TIME_STAMP_FORMAT = '%Y.%m.%d_%H.%M.%S'

HEADER_PARAMETER_FILE = ['Parameter', 'Value']
HEADER_ORDER_DICT = ['Date_Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance'] 
HEADER_TICK_DATA = ['Date_Time', 'Bid', 'Ask', 'Bid_NextTick', 'Ask_NextTick']
OPTIMIZE_PARAMETERS_LIST = ['FilterSpread', 'Friday', 'OpenOrdersLimitDay', 'Time_closing_trades', 'Time_of_closing_in_hours',
                       'Profit_all_orders', 'Arrangements_of_trades', 'Lots']

PIP_VALUE_DICT = {}
PIP_VALUE_DICT['AUDCAD'] = 0.0001
PIP_VALUE_DICT['AUDUSD'] = 0.0001
PIP_VALUE_DICT['EURCAD'] = 0.0001
PIP_VALUE_DICT['EURGBP'] = 0.0001
PIP_VALUE_DICT['EURUSD'] = 0.0001
PIP_VALUE_DICT['GBPUSD'] = 0.0001
PIP_VALUE_DICT['USDCAD'] = 0.0001
PIP_VALUE_DICT['AUDJPY'] = 0.01
PIP_VALUE_DICT['CADJPY'] = 0.01
PIP_VALUE_DICT['EURJPY'] = 0.01
PIP_VALUE_DICT['GBPJPY'] = 0.01
PIP_VALUE_DICT['USDJPY'] = 0.01


################################################################################
##########################          FUNCTIONS        ###########################
################################################################################
def convert_backflash2forwardflash(backflash_path):
    forwardflash_path = ''
    
    # replace the back flash with forward flash
    for i in range(len(backflash_path)):
        if backflash_path[i] == '\\':
            forwardflash_path += '/'
        else:
            forwardflash_path += backflash_path[i]
        
    return forwardflash_path


#===============================================================================
def permutation_count(letters, digits):
    
    if (integer_checker(letters) 
        & integer_checker(digits)):
        
        return f(letters) // f(letters - digits)
    else:
        print("The inputs are NOT integer")
        return -1


#===============================================================================
def combination_count(letters, digits):
    if (integer_checker(letters) 
        & integer_checker(digits)):
    
        return f(letters) // f(letters - digits) // f(digits)


#===============================================================================
def copy_string_array(source_array):
    data_col = len(source_array[DEFAULT_NUMBER_INT]) 
    data_row = len(source_array)
    destination_array = [["" for x in range(data_col)] for y in range(data_row)] 
     
    for x in range(data_row):
        for y in range(data_col):
            destination_array[x][y] = source_array[x][y]
        
    return destination_array


#===============================================================================
def merge_2parametes_array_data(old_array, new_array):
    col_value_index = 1
    
    for row_new_array in range(len(new_array)):
        for row_old_array in range(len(old_array)):
            if str(old_array[row_old_array][DEFAULT_NUMBER_INT]) == str(new_array[row_new_array][DEFAULT_NUMBER_INT]):
                old_array[row_old_array][col_value_index] = new_array[row_new_array][col_value_index]
        
    return old_array


#===============================================================================
def combine_2arrays_data(array_1, array_2):
    
    data_col = len(array_1[DEFAULT_NUMBER_INT]) 
    data_row = len(array_1) + len(array_2)
    new_array = [["" for x in range(data_col)] for y in range(data_row)] 
    
    row_count = DEFAULT_NUMBER_INT
    for x in range(len(array_1)):
        for y in range(data_col):
            new_array[row_count][y] = array_1[x][y]
        row_count += DEFAULT_SECOND_NUMBER_INT
        
    for x in range(len(array_2)):
        for y in range(data_col):
            new_array[row_count][y] = array_2[x][y]
        row_count += DEFAULT_SECOND_NUMBER_INT
        
    return new_array


#===============================================================================
def load_csv2dataframe(file_name):
    
    # convert the back flash with forward flash (just in case)
    file_name = convert_backflash2forwardflash(file_name)
    
    # create a data frame with CSV file
    DataFrame = pd.read_csv(file_name)
     
    return DataFrame


#===============================================================================
def convert_backflash2forwardflash_change_output_folder(backflash_path):
    ''' convert back flash to forward flash and change the path name from 
    "input" folder into "output" folder '''
    
    forwardflash_path = ''
    
    # replace the back flash with forward flash
    i = DEFAULT_NUMBER_INT
    while (i < len(backflash_path)):
        if backflash_path[i] == '\\':
            forwardflash_path += '/'
        elif (backflash_path[i] == 'i' 
              and backflash_path[i + 1] == 'n' 
              and backflash_path[i + 2] == 'p' 
              and backflash_path[i + 3] == 'u' 
              and backflash_path[i + 4] == 't'):
            
            forwardflash_path += 'o'
            forwardflash_path += 'u'
            forwardflash_path += 't'
            forwardflash_path += 'p'
            forwardflash_path += 'u'
            forwardflash_path += 't'
            
            i = i + 4
            
        else:
            forwardflash_path += backflash_path[i]
            
        i += DEFAULT_SECOND_NUMBER_INT
                
    return forwardflash_path


#===============================================================================
def create_a_new_row_gaincapital_format(row):
    ''' For GAIN Capital Tick Data Format. 
    ==> Analyze the string separated by Space to get [Date, Time, Ask, Bid] and then create a new version 
    of that row as [Date_Time, Date, Time, Bid, Ask] 
    Ex: [4,"USD/JPY",2009-05-01 00:00:00, 102.540000, 102.580000,"D"]
        [22,"USD/JPY",2009-05-01 00:00:00, 102.540000, 102.580000,"D"]
        ==> [2009.05.01_00:00:00,000, 102.540000,102.580000, 102.540000,102.580000]
        ==> [1241136000296.000000, 14365.0, 000.0, 98.89, 98.902, 98.887, 98.899] '''
    
    # GAIN Capital tick data from 2005 to 2009 and datetime_col_index = 2 [0,1,2]
    datetime_col_index = 2
    bid_col_index = 3
    ask_col_index = 4
    
#     # GAIN Capital tick data from 2010 to 2017 datetime_col_index = 3 [0,1,2,3]
#     datetime_col_index = 3
#     bid_col_index = 4
#     ask_col_index = 5
    
    if (row[datetime_col_index] != '0'):
        # --> get the part BEFORE (Date) and AFTER (Time) the Space
        split_space = row[datetime_col_index].split(' ')
         
        date_part = split_space[DEFAULT_NUMBER_INT]
        time_second_part = split_space[DEFAULT_SECOND_NUMBER_INT]
         
        # --> format the date time as expected WITH millisecond
        date_modified_part = ('' + date_part.replace('-', '.') + '_' + time_second_part.split('.')[DEFAULT_NUMBER_INT] + '.000')
        
#         # --> format the date time as expected WITHOUT millisecond
#         date_modified_part = ('' + date_part.replace('-', '.') + '_' + time_second_part.split('.')[DEFAULT_NUMBER_INT])
        
        fdatetime_modified_part = convert_string_datetime2float_no_ms(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
        fday_modified_part = convert_string_day2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
        ftime_modified_part = convert_string_second2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
        
        # --> create a new row for Tick data
        new_row = ['%.1f' % fdatetime_modified_part, fday_modified_part, ftime_modified_part, float(row[bid_col_index]), float(row[ask_col_index])]
    else:
        # --> create a new row for Tick data
        new_row = row
    
    return new_row

 
#===============================================================================
def create_multiple_tick_data_from_wholefolder_gaincapital_format(folder_name):
    ''' For GAIN Capital Tick Data Format. 
    ==> Read each row of all Original Tick data file, create a new version of that row, and then
    combine them by writing each new version row into 1 new CSV file 
    Ex: [4,"USD/JPY",2009-05-01 00:00:00, 102.540000, 102.580000,"D"]
        [22,"USD/JPY",2009-05-01 00:00:00, 102.540000, 102.580000,"D"]
        ==> [2009.05.01_00:00:00,000, 102.540000,102.580000, 102.540000,102.580000]
        ==> [1241136000296.000000, 14365.0, 000.0, 98.89, 98.902, 98.887, 98.899] '''
     
    # convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    allFiles = glob.glob(folder_name + '/*.csv')
     
    file_index = DEFAULT_SECOND_NUMBER_INT
    for file_ in allFiles:
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        file_basename = os.path.basename(file_)
        print("{0} ==> processing file {1}: {2} ...".format(time_stamp, file_index, file_basename))
         
        file_name = convert_backflash2forwardflash_change_output_folder(file_)
          
        if (file_index % 10 == DEFAULT_NUMBER_INT):
            perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            print("{0} ... ==> processing {1}% of the data...".format(time_stamp, perc))
           
        # write an array to a CSV file
        csv_new_row_write = open(file_name, "w")  # "w" indicates that you're writing strings to the file
               
        # open the CSV file
        ifile = open(file_, "rU")
        reader = csv.reader(ifile, delimiter=",")
        
        # create a new version of row with (GAIN Capital Tick Data Format)
        for row in reader:
            new_row = (','. join([str(j) for j in create_a_new_row_gaincapital_format(row)])
                       + "\n")
            
            # write to CSV the new row: [Date_Time, Date, Time, Bid, Ask]
            csv_new_row_write.write(new_row)
             
        ifile.close()
       
        file_index += DEFAULT_SECOND_NUMBER_INT
           
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print("{0} ==> Completed {1} files!!!".format(time_stamp, file_index - DEFAULT_SECOND_NUMBER_INT))


#===============================================================================
def create_a_new_row_forexfactory_format(row):
    ''' For FOREXFACTORY Calendar Data Format. 
    ==> Analyze the string separated by Space to get [Date Time, Symbol, Impact Level] and then create a new version 
    of that row as [Date_Time, Date, Time, Symbol, Impact Level]
    Ex: [2009-05-01 00:00:00, ALL, 2] 
        ==> [1241136000296.0, 14365.0, 000.0, ALL, 2] '''
    
    # GAIN Capital tick data from 2007 to 2014
    datetime_col_index = 0
    symbol_col_index = 1
    impact_col_index = 2
    
    if (row[datetime_col_index] != '0'):
        # --> get the part BEFORE (Date) and AFTER (Time) the Space
        split_space = row[datetime_col_index].split(' ')
         
        date_part = split_space[DEFAULT_NUMBER_INT]
        time_second_part = split_space[DEFAULT_SECOND_NUMBER_INT]
         
        # --> format the date time as expected WITHOUT millisecond
        date_modified_part = ('' + date_part.replace('-', '.') + '_' + time_second_part.split('.')[DEFAULT_NUMBER_INT])
        
        fdatetime_modified_part = convert_string_datetime2float_no_ms(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
        fday_modified_part = convert_string_day2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
        ftime_modified_part = convert_string_second2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
        
        # --> create a new row for Tick data
        new_row = ['%.1f' % fdatetime_modified_part, fday_modified_part, ftime_modified_part, row[symbol_col_index], float(row[impact_col_index])]
    else:
        # --> create a new row for Tick data
        new_row = row
    
    return new_row

 
#===============================================================================
def create_multiple_calendar_data_from_wholefolder_forexfactory_format(folder_name):
    ''' For FOREXFACTORY Calendar Data Format. 
    ==> Read each row of all Original Tick data file [Date Time, Symbol, Impact Level], 
    create a new version of that row, and then
    combine them by writing each new version row into 1 new CSV file 
    Ex: [2009-05-01 00:00:00, ALL, 2] 
        ==> [1241136000296.000000, 14365.0, 000.0, ALL, 2] '''
     
    # convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    allFiles = glob.glob(folder_name + '/*.csv')
     
    file_index = DEFAULT_SECOND_NUMBER_INT
    for file_ in allFiles:
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        file_basename = os.path.basename(file_)
        print("{0} ==> processing file {1}: {2} ...".format(time_stamp, file_index, file_basename))
         
        file_name = convert_backflash2forwardflash_change_output_folder(file_)
          
        if (file_index % 10 == DEFAULT_NUMBER_INT):
            perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            print("{0} ... ==> processing {1}% of the data...".format(time_stamp, perc))
           
        # write an array to a CSV file
        csv_new_row_write = open(file_name, "w")  # "w" indicates that you're writing strings to the file
               
        # open the CSV file
        ifile = open(file_, "rU")
        reader = csv.reader(ifile, delimiter=",")
        
        # create a new version of row with (GAIN Capital Tick Data Format)
        for row in reader:
        
            new_row = (','. join([str(j) for j in create_a_new_row_forexfactory_format(row)])
                       + "\n")
            
            # write to CSV the new row: [Date_Time, Date, Time, Symbol, Impact Level]
            csv_new_row_write.write(new_row)
             
        ifile.close()
       
        file_index += DEFAULT_SECOND_NUMBER_INT
           
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print("{0} ==> Completed {1} files!!!".format(time_stamp, file_index - DEFAULT_SECOND_NUMBER_INT))

 
#===============================================================================
def create_a_new_row_pepperstone_format(previous_row, row):
    ''' For Pepperstone Tick Data Format. 
    ==> Analyze the string separated by Space to get Date, Time, Ask, Bid and then create a new version 
    of that row as Date_Time, Date, Time, Ask, Bid, Ask_NextTick (from next row), Bid_NextTick (from next row) 
    Ex: [USD/JPY, 20090501 00:00:00.296, 98.89, 98.902]
        [USD/JPY, 20090501 00:00:00.299, 98.887, 98.899]
        ==> [2009.05.01_00:00:00,296, 2009.05.01, 00:00:00,296, 98.89, 98.902, 98.887, 98.899]
        ==> [1241136000296.000000, 14365.0, 296.0, 98.89, 98.902, 98.887, 98.899] '''
    
    datetime_col_index = DEFAULT_SECOND_NUMBER_INT
    bid_col_index = 2
    ask_col_index = 3
    
    # --> get the part BEFORE (Date) and AFTER (Time) the Space
    split_space = previous_row[datetime_col_index].split(' ')
    
    date_part = split_space[DEFAULT_NUMBER_INT]
    time_part = split_space[DEFAULT_SECOND_NUMBER_INT].split('.')
    
    # --> get the part BEFORE (Second) and AFTER (Millisecond) the Dot
    time_second_part = time_part[DEFAULT_NUMBER_INT]
    time_milisecond_part = time_part[DEFAULT_SECOND_NUMBER_INT]
    
    # --> format the date time as expected
    date_modified_part = ('' + date_part[:4] + '.' + date_part[4:6] + '.' + date_part[6:8] 
                          + '_' + time_second_part + ',' + time_milisecond_part)
    
    fdate_modified_part = convert_string_datetime2float_no_ms(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
    fday_modified_part = convert_string_day2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
    ftime_modified_part = convert_string_second2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
    
    # --> create a new row for Tick data
    return (['%.2f' % fdate_modified_part, fday_modified_part, ftime_modified_part, float(previous_row[bid_col_index]), float(previous_row[ask_col_index]), float(row[bid_col_index]), float(row[ask_col_index])],
            ['%.2f' % fdate_modified_part, date_modified_part])


#===============================================================================
def create_multiple_tick_data_from_wholefolder_pepperstone_format(folder_name):
    ''' For Pepperstone Tick Data Format. 
    ==> Read each row of all Original Tick data file, create a new version of that row, and then
    combine them by writing each new version row into 1 new CSV file 
    Ex: [USD/JPY, 20090501 00:00:00.296, 98.89, 98.902]
        [USD/JPY, 20090501 00:00:00.299, 98.887, 98.899]
        ==> [2009.05.01_00:00:00,296, 2009.05.01, 00:00:00,296, 98.89, 98.902, 98.887, 98.899]
        ==> [1241136000296.000000, 14365.0, 296.0, 98.89, 98.902, 98.887, 98.899] '''
    
    # convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    allFiles = glob.glob(folder_name + '/*.csv')
    
    file_index = DEFAULT_NUMBER_INT
    for file_ in allFiles:
        print("==> processing file {0}...".format(file_index))
        
        file_name = convert_backflash2forwardflash_change_output_folder(file_)
         
        if (file_index % 10 == DEFAULT_NUMBER_INT):
            perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
            print("... ==> processing {0}% of the data...".format(perc))
          
        # write an array to a CSV file
        csv_new_row_write = open(file_name, "w")  # "w" indicates that you're writing strings to the file
        csv_date_dict = open(file_name.replace(".csv", "_date_dict.csv"), "w")  # "w" indicates that you're writing strings to the file
              
        # open the CSV file
        ifile = open(file_, "rU")
        reader = csv.reader(ifile, delimiter=",")
        previous_row = reader.next()
          
        for row in reader:
            
            # create a new version of row with 2 parts (Pepperstone Tick Data Format)
            new_row = create_a_new_row_pepperstone_format(previous_row, row)
            
            # write to CSV file part 1 of a new row: [Date_Time, Day, Millisecond, Bid, Ask, Bid_NextTick, Ak_NextTick]
            fdate_modified_part = ','. join([str(j) for j in new_row[DEFAULT_NUMBER_INT]]) + "\n"
            csv_new_row_write.write(fdate_modified_part)
            
            # write to CSV file part 1 of a new row: [Date_Time, Day, Millisecond, Bid, Ask, Bid_NextTick, Ak_NextTick]
            fdate_dictionary = ','. join([str(j) for j in new_row[DEFAULT_SECOND_NUMBER_INT]]) + "\n"
            csv_date_dict.write(fdate_dictionary)
              
            # --> save the current row
            previous_row = row
              
        ifile.close()
      
        # write the last row
        last_row = [0, 0, 0, 0]
        
        # create a new version of last row with 2 parts
        new_row = create_a_new_row_pepperstone_format(previous_row, last_row)
        
        # write to CSV file part 1 of the last new row: [Date_Time, Bid, Ask, Bid_NextTick, Ak_NextTick]
        fdate_modified_part = ','. join([str(j) for j in new_row[DEFAULT_NUMBER_INT]]) + "\n"
        csv_new_row_write.write(fdate_modified_part)
        
        # write to CSV file part 1 of the last new row: [Date_Time, Bid, Ask, Bid_NextTick, Ak_NextTick]
        fdate_dictionary = ','. join([str(j) for j in new_row[DEFAULT_SECOND_NUMBER_INT]]) + "\n"
        csv_date_dict.write(fdate_dictionary)
      
        file_index += DEFAULT_SECOND_NUMBER_INT
          
    print("==> Completed {0} files!!!".format(file_index))


#===============================================================================
def combine_all_files_in_a_folder(folder_name, combined_file_name, file_type):    
    ''' Combine all CSV files in a folder into 1 CSV file only with file_type (ex: *.csv) '''

    # convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    allFiles = glob.glob(folder_name + '/' + file_type)
    
    combined_file_name = convert_backflash2forwardflash(combined_file_name)
    csv_combined_file_write = open(combined_file_name, "w")  # "w" indicates that you're writing strings to the file
             
    file_index = DEFAULT_SECOND_NUMBER_INT
    for file_ in allFiles:
#         log.info(" ==> combining file {0}...".format(file_index))
#         time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#         print("{0} ==> combining file {1}...".format(time_stamp, file_index))
#         
#         if (file_index % 10 == DEFAULT_NUMBER_INT):
#             perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
#             log.info("... ==> processing {0}% of the data...".format(perc))
#             time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#             print("{0} ... ==> processing {1}% of the data...".format(time_stamp, perc))
          
        # open the CSV file
        ifile = open(file_, "rU")
        reader = csv.reader(ifile, delimiter=",")
          
        for row in reader:
            csv_combined_file_write.write(','. join([str(j) for j in row]) + "\n")
              
        ifile.close()
        
        file_index += DEFAULT_SECOND_NUMBER_INT
      
    '''
#     log.info("==> Completed combining {0} files!!!".format(file_index - DEFAULT_SECOND_NUMBER_INT))
#     time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#     print("{0} ==> Completed combining {1} files!!!".format(time_stamp, file_index - DEFAULT_SECOND_NUMBER_INT))
    '''


#===============================================================================
def load_wholefolder2array(folder_name):    
    ''' Read each row of all Original Tick data file, create a new version of that row, and then
    write each new version row into 1 new list. 
    Example of new version of a row
        [USD/JPY, 20090501 00:00:00.296, 98.89, 98.902]
        [USD/JPY, 20090501 00:00:00.299, 98.887, 98.899]
        ==> [20090501_00:00:00.296, 98.89, 98.902, 98.887, 98.899] '''
    
    # convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    
    allFiles = glob.glob(folder_name + "/*.csv")
    list_ = []
    for file_ in allFiles:
        # open the CSV file
        ifile = open(file_, "rU")
        reader = csv.reader(ifile, delimiter=",")
        previous_row = reader.next()
        
        for row in reader:
            
            new_row = create_a_new_row_pepperstone_format(previous_row, row)
            
            list_.append (new_row)
            
            # --> save the current row
            previous_row = row
            
        ifile.close()
    
        # save the last row
        last_row = [0, 0, 0, 0]
        new_last_row = create_a_new_row_pepperstone_format(previous_row, last_row)
        list_.append(new_last_row)
    
    return list_

   
#===============================================================================
def load_csv2array(file_name):    
    
    # convert the back flash with forward flash (just in case)
    file_name = convert_backflash2forwardflash(file_name)
    
    # open the CSV file
    ifile = open(file_name, "rU")
    reader = csv.reader(ifile, delimiter=",")

    # put the CSV into an array
    list = []

    for row in reader:
        list.append (row)
    
    ifile.close()
    
    return list


#===============================================================================
def float_checker(number):
     
    flag_float = isinstance(number, float)  # returns True if it's a float
     
    if (flag_float == False):
        print('This is NOT a float number')
        log.info('This is NOT a float number')
         
    return flag_float


#===============================================================================
def integer_checker(number):

    if sys.version < '3':
        integer_types = (int, long,)
    else:
        integer_types = (int,)
 
    flag_int = isinstance(number, integer_types)  # returns True if it's an integer
    
    if (flag_int == False):
        print('This is NOT a integer number')
        log.info('This is NOT a integer number')
    
    return flag_int


#===============================================================================
def number_after_decimal(number):
    # check number whether it is a float number (just in case)
    if float_checker(number) == False:
        return DEFAULT_NUMBER_INT
    else:
        return number % 1


#===============================================================================
def digit_of_symbol(number):
    # check number whether it is a float number (just in case)
    if float_checker(number) == False:
        return DEFAULT_NUMBER_INT
    else:
        num_of_digit = Decimal(str(number))
        digit = (num_of_digit.as_tuple().exponent) * (-1)
        return int(digit)


#===============================================================================
def point_of_symbol(number):
    ''' point=1/pow(10,digits): definition from MetaTrader 4 Manager API '''
    
    # check number whether it is a float number (just in case)
    if float_checker(number) == False:
        return DEFAULT_NUMBER_INT
    else:
        point = float(1) / pow(10, digit_of_symbol(number))
        return point


#===============================================================================
def get_subset_dataframe(origin_dataframe, subtract_list_string):
        
    # initialize the OPTIMIZED_PARAMETERS_DATA    
    list_count = DEFAULT_NUMBER_INT
    subset_data = origin_dataframe.loc[[subtract_list_string[list_count]]]
    
    # append all needed item in the list together
    while (list_count + 1 < len(subtract_list_string)):
        next_item = subtract_list_string[list_count + 1]
        subset_data = subset_data.append(origin_dataframe.loc[[next_item]])
        list_count += 1
    
    return subset_data

    
#===============================================================================
def get_subset_data(origin_data, subtract_list_string):
        
    # initialize the OPTIMIZED_PARAMETERS_DATA    
    list_count = DEFAULT_NUMBER_INT
    data_col = len(origin_data[DEFAULT_NUMBER_INT]) 
    data_row = len(subtract_list_string)
    subset_data = [["" for x in range(data_col)] for y in range(data_row)] 
    
    # append all needed item in the list together
    while (list_count < len(subtract_list_string)):
        for i in range(len(origin_data)):
            if subtract_list_string[list_count] == origin_data[i][DEFAULT_NUMBER_INT]:
                for j in range(len(origin_data[i])): 
                    subset_data[list_count][j] = origin_data[i][j]
        list_count += 1
        
    return subset_data


#===============================================================================
def write_array2csv_with_delimiter_no_header(array, file_name, delimiter):
     
    # # convert the back flash with forward flash (just in case)
    file_name = convert_backflash2forwardflash(file_name)
    
    # If applicable, delete the existing file to generate a fresh file during each execution
    if path.isfile(file_name):
        remove(file_name)
     
    # write an array to a CSV file
    csv = open(file_name, "w")  # "w" indicates that you're writing strings to the file
    
    for i in range(len(array)):
        sMyArray = [str(j) for j in array[i]]
        row = delimiter . join(sMyArray) + "\n"
        csv.write(row)


#===============================================================================
def write_wholedict2csv_no_header(dictionary_out, file_name):
     
    # convert the back flash with forward flash (just in case)
    file_name = convert_backflash2forwardflash(file_name)
    
    # If applicable, delete the existing file to generate a fresh file during each execution
    if path.isfile(file_name):
        remove(file_name)
     
    # write a dictionary to a CSV file
    with open(file_name, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dictionary_out.items():
            writer.writerow([key, value])


#===============================================================================
def write_value_of_dict2csv_no_header(dictionary_out, file_name):
     
    # convert the back flash with forward flash (just in case)
    file_name = convert_backflash2forwardflash(file_name)
    
    # If applicable, delete the existing file to generate a fresh file during each execution
    if path.isfile(file_name):
        remove(file_name)
     
    # write a dictionary to a CSV file
    with open(file_name, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dictionary_out.items():
            writer.writerow(value)


#===============================================================================
def write_list_of_dicts_no_header(list_of_dicts, file_name):
     
    # convert the back flash with forward flash (just in case)
    file_name = convert_backflash2forwardflash(file_name)
    
    # If applicable, delete the existing file to generate a fresh file during each execution
    if path.isfile(file_name):
        remove(file_name)
     
    # write a dictionary to a CSV file
    with open(file_name, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for dictionary_out in list_of_dicts:
            for key, value in dictionary_out.items():
                writer.writerow([key, value])


#===============================================================================
def display_an_array_with_delimiter(array_out, delimiter):
    out_length = len(array_out)
    
    if out_length == DEFAULT_NUMBER_INT:
        # print the summary
        print('[%s rows x %s columns]' % (out_length, out_length))
    elif out_length <= 100:
        for i in range(out_length):
            sMyArray = [str(j) for j in array_out[i]]
            print(delimiter . join(sMyArray))
        
        # print the summary
        print('[%s rows x %s columns]' % (out_length, len(array_out[DEFAULT_NUMBER_INT])))
    else:
        # display 20 first items
        for i in range(20):
            sMyArray = [str(j) for j in array_out[i]]
            print(delimiter . join(sMyArray))
            
        print('...    ...    ...    ...    ...    ...    ...')
        
        # display 20 last items
        i = out_length - 20
        while i < out_length:
            sMyArray = [str(j) for j in array_out[i]]
            print(delimiter . join(sMyArray))
            i += 1
        
        # print the summary
        print('[%s rows x %s columns]' % (out_length, len(array_out[DEFAULT_NUMBER_INT])))


#===============================================================================
def display_an_dict_with_delimiter(dict_out, delimiter):
    ''' Display dictionary with the input delimiter (ex: '=' or ',' or '/' etc.) '''
    
    # display dictionary with iterating over items returning key, value tuples
    for key, value in dict_out.iteritems():  
        print('%s' % str(key) + delimiter + '%s' % str(value))
        log.info('%s' % str(key) + delimiter + '%s' % str(value))


#===============================================================================
def is_time_earlier(early_timer, late_time, std_time, sformat):
    ''' Compare 2 times with a standard time. '''
    
    early_date = datetime.strptime(early_timer, sformat)  # early date
    late_date = datetime.strptime(late_time, sformat)  # late date
    std_date = datetime.strptime(std_time, sformat)  # standard date
    
    # calculate difference between early-late date
    diff_early_date = early_date - std_date
    diff_late_date = late_date - std_date
    
    # convert time to seconds
    seconds_early_date = diff_early_date.seconds + diff_early_date.days
    seconds_late_date = diff_late_date.seconds + diff_late_date.days

    # compare 2 times
    if (seconds_early_date < seconds_late_date):
        return True
    else:
        return False    

    
#===============================================================================
def convert_string_datetime2float_no_ms(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into seconds in float type '''
     
    # parse the time format using strptime.
    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
        
    # calculate difference between convert_datetime and std_date by milliseconds
    diff_time = convert_datetime - std_date
     
    # convert the different milliseconds into float
    diff_time_seconds = float(diff_time.days * SECONDS_OF_ADAY + diff_time.seconds)
     
    return diff_time_seconds    


#===============================================================================
def convert_string_datetime2float_with_ms(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into millisecond in float type '''
    
    # get the millisecond from the input date_time
    convert_datetime_milliseconds = convert_datetime.split(',')[DEFAULT_SECOND_NUMBER_INT]
    
    # parse the time format using strptime.
    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
       
    # calculate difference between convert_datetime and std_date by milliseconds
    diff_time = convert_datetime - std_date
    
    # convert the different milliseconds into float
    diff_time__milliseconds = float((diff_time.days * SECONDS_OF_ADAY + diff_time.seconds) * 1000) + float(convert_datetime_milliseconds)
    
    return diff_time__milliseconds  


#===============================================================================
def convert_string_day2float(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into float 
    of total days only '''

    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
    
    # calculate difference between convert_datetime and std_date
    diff_time = convert_datetime - std_date
    
    # convert the different days into total float
    return float(diff_time.days)    


#===============================================================================
def convert_string_second2float(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into float 
    which is sum of total seconds '''

    # parse the time format using strptime.
    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
    
    # calculate difference between convert_datetime and std_date
    diff_time = convert_datetime - std_date
    
    return diff_time.seconds    


#===============================================================================
def convert_string_millisecond2float(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into float 
    which is sum of total seconds and milliseconds '''

    # get the millisecond from the input date_time
    convert_datetime_milliseconds = convert_datetime.split(',')[DEFAULT_SECOND_NUMBER_INT]
    
    # parse the time format using strptime.
    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
    
    # calculate difference between convert_datetime and std_date
    diff_time = convert_datetime - std_date
    
    # convert the different milliseconds into float
    if (diff_time.seconds == DEFAULT_NUMBER_INT):
        diff_time__milliseconds = float(MILLISECONDS_OF_ASECOND) + float(convert_datetime_milliseconds)
    else:
        diff_time__milliseconds = float(diff_time.seconds * MILLISECONDS_OF_ASECOND) + float(convert_datetime_milliseconds)
    
    return diff_time__milliseconds    


#===============================================================================
def order_delete(self, row_index, array_data):
    ''' Delete s specific order in data. '''
 
    # delete the order if it's existed in the data
    if (row_index < len(array_data)):
        new_array_data = copy_string_array(array_data)
        del new_array_data[row_index]
        return new_array_data
    else:
        print("There's NO row %s in data." % row_index)
        log.info("There's NO row %s in data." % row_index)

        
def convert_datetime_back_whole_list(file_name_out):
    ''' Convert back Date Time from float to normal format. '''
    
    # load data from input file
    data_converted = load_csv2array(file_name_out)
    
    for i in range(len(data_converted)):
        # --> convert day from float
        scurrentday = date.fromordinal(DATEOFFSET + int(float(data_converted[i][DAY_COL_INDEX])))
        
        # slit date into year, month, and day
        dividend = str(scurrentday).split('-')
        year = dividend[DEFAULT_NUMBER_INT]
        month = dividend[DEFAULT_SECOND_NUMBER_INT]
        day = dividend[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
        
        # get the day from float number (DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S')
        day_converted = year + '.' + month + '.' + day

        # --> convert time from float
        hour_minute_second = int(float(data_converted[i][TIME_COL_INDEX])) 
        
        # --> get the time from float number (DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S')
        hour_converted = int(hour_minute_second / SECONDS_OF_ANHOUR)
        minute_converted = int(hour_minute_second % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
        second_converted = int(hour_minute_second % SECONDS_OF_ANHOUR % SECONDS_OF_AMINUTE)
        
        # adjust the hour for output when less than 10 hours
        if (hour_converted < 10):
            shour_converted = '0' + str(hour_converted)
        else:
            shour_converted = str(hour_converted)
        
        # adjust the minute for output when less than 10 hours
        if (minute_converted < 10):
            sminute_converted = '0' + str(minute_converted)
        else:
            sminute_converted = str(minute_converted)
        
        # adjust the second for output when less than 10 hours
        if (second_converted < 10):
            ssecond_converted = '0' + str(second_converted)
        else:
            ssecond_converted = str(second_converted)
        
        time_converted = shour_converted + ':' + sminute_converted + ':' + ssecond_converted
        
        # --> write all date and time converted into the output CSV file
        data_converted[i][DATETIME_COL_INDEX] = day_converted + '_' + time_converted
        data_converted[i][DAY_COL_INDEX] = day_converted
        data_converted[i][TIME_COL_INDEX] = time_converted
        
    return data_converted


################################################################################
#######################      LOAD HARDCODED DATA     ###########################
################################################################################
''' LOAD HARDCODED DATA '''


# # TODO: Run 2 times for 2 formats: 2005-2009 & 2010-2017
# # Create TICK_DATA with Modification from Original Tick Data CSV file WITH milliseconds
# # --> format the date time as expected WITH millisecond (Note: need to do 2 time with columns format from from 2005 to 2009 VS from 2010 to 2017)
# FOLDER_TICK_DATA_ORIGINAL = '/EURUSD_2006_2017_GAINCapital_Original_with_milliseconds_DTcol_2'
# MARKET_TIME_STANDARD = '1970.01.01_00:00:00.000'
# DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S.%f'
# create_multiple_tick_data_from_wholefolder_gaincapital_format(FOLDER_DATA_INPUT + SYMBOL + FOLDER_TICK_DATA_ORIGINAL)
#  
# # TODO: Run 2 times for 2 formats: 2005-2009 & 2010-2017
# # Create TICK_DATA with Modification from Original Tick Data CSV file WITHOUT milliseconds
# # --> format the date time as expected WITHOUT millisecond (Note: need to do 2 time with columns format from from 2005 to 2009 VS from 2010 to 2017)
# FOLDER_TICK_DATA_ORIGINAL = '/EURUSD_2006_2017_GAINCapital_Original_NO_milliseconds_DTcol_2'
# 
# 
# MARKET_TIME_STANDARD = '1970.01.01_00:00:00'
# DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S'
# create_multiple_tick_data_from_wholefolder_gaincapital_format(FOLDER_DATA_INPUT + SYMBOL + FOLDER_TICK_DATA_ORIGINAL)
#  
# # Create CALENDAR_DATA with Modification from Original Calendar Data CSV file WITHOUT milliseconds
# create_multiple_calendar_data_from_wholefolder_forexfactory_format(FOLDER_DATA_INPUT + FOLDER_CALENDAR_DATA_ORIGINAL)
'''==============================================================================='''


time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
log.info("==> Load DEFAULT_PARAMETERS_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_PARAMETER_DEFAULT))
log.info('===============================================================================')
print("%s ==> Load DEFAULT_PARAMETERS_DATA: %s ..." % (time_stamp, FOLDER_DATA_INPUT + FILENAME_PARAMETER_DEFAULT))
print('===============================================================================')
 
# Create DEFAULT_PARAMETERS_DATA with CSV file
DEFAULT_PARAMETERS_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_PARAMETER_DEFAULT)
 
time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
log.info("==> Load SETTING_PARAMETERS_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2))
log.info('===============================================================================')
print("%s ==> Load SETTING_PARAMETERS_DATA: %s ..." % (time_stamp, FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2))
print('===============================================================================')
 
# Create SETTING_2_PARAMETERS_DATA with CSV file
SETTING_2_PARAMETERS_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2)
SETTING_3_PARAMETERS_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_3)
 
time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
log.info("==> Create OPTIMIZED_PARAMETERS_DATA data: %s ..." % (FOLDER_DATA_OUTPUT + FILENAME_OPTIMIZE_PARAMETER))
log.info('===============================================================================')
print("%s ==> Create OPTIMIZED_PARAMETERS_DATA data: %s ..." % (time_stamp, FOLDER_DATA_OUTPUT + FILENAME_OPTIMIZE_PARAMETER))
print('===============================================================================')
# Create OPTIMIZED_PARAMETERS_DATA
OPTIMIZED_PARAMETERS_DATA = get_subset_data(DEFAULT_PARAMETERS_DATA, OPTIMIZE_PARAMETERS_LIST)
 
time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
log.info("==> Load CALENDAR_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2))
log.info('===============================================================================')
print("%s ==> Load CALENDAR_DATA: %s ..." % (time_stamp, FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2))
print('===============================================================================')
 
# Create CALENDAR_DATA with CSV file
# --> calendar of all symbols 
CALENDAR_ALL_SYMBOLS_DATA = load_csv2array(FOLDER_DATA_INPUT + FOLDER_CALENDAR_DATA_MODIFIED + 
                                           ALL_CURRENCY + FILENAME_CALENDAR_DATA)
 
# --> calendar of base symbol 
file_name_base_currency = str(FOLDER_DATA_INPUT + FOLDER_CALENDAR_DATA_MODIFIED + 
                              BASE_CURRENCY + FILENAME_CALENDAR_DATA)
if path.isfile(file_name_base_currency):
    CALENDAR_BASE_SYMBOL_DATA = load_csv2array(file_name_base_currency)
else:
    CALENDAR_BASE_SYMBOL_DATA = []
 
# --> calendar of quote symbol 
file_name_quote_currency = str(FOLDER_DATA_INPUT + FOLDER_CALENDAR_DATA_MODIFIED + 
                               QUOTE_CURRENCY + FILENAME_CALENDAR_DATA)
if path.isfile(file_name_quote_currency):
    CALENDAR_QUOTE_SYMBOL_DATA = load_csv2array(file_name_quote_currency)
else:
    CALENDAR_QUOTE_SYMBOL_DATA = []
 
display_an_array_with_delimiter(CALENDAR_ALL_SYMBOLS_DATA, ' ')
display_an_array_with_delimiter(CALENDAR_BASE_SYMBOL_DATA, ' ')
display_an_array_with_delimiter(CALENDAR_QUOTE_SYMBOL_DATA, ' ')
     
time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
log.info("==> All hard coded data have been loaded!!!")
log.info('===============================================================================')
print("%s ==> All hard coded data have been loaded!!!" % (time_stamp))
print('===============================================================================')


################################################################################
#########################           CLASS           ############################
################################################################################        
class HappyForexEA(object):
    '''
    classdocs
    '''
 
    #===============================================================================
    def __init__(self):
        '''
        Constructor
        '''
        # get the total parameters for running EA
        self.NAME_EA = ""
        self.MAGIC = DEFAULT_NUMBER_INT
        self.FILTERSPREAD = False
        self.SPREADMAX = DEFAULT_NUMBER_FLOAT
        self.A = ""
        self.MONDAY = False
        self.TUESDAY = False
        self.WEDNESDAY = False
        self.THURSDAY = False
        self.FRIDAY = False
        self.SATURDAY = False
        self.SUNDAY = False
        self.B = ""
        self.TRADING_24H = False
        self.GMT_OFFSET = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_FROM = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_TO = DEFAULT_NUMBER_INT
        self.USE_ORDERSLIMIT = False
        self.OPENORDERSLIMITDAY = DEFAULT_NUMBER_INT
        self.C = ""
        self.TIME_CLOSING_TRADES = False
        self.TIME_OF_CLOSING_IN_HOURS = DEFAULT_NUMBER_INT
        self.TIME_OF_CLOSING_IN_MINUTES = DEFAULT_NUMBER_INT
        self.D = ""
        self.PROFIT = False
        self.PROFIT_ALL_ORDERS = DEFAULT_NUMBER_FLOAT
        self.E = ""
        self.OPENORDERSLIMIT = DEFAULT_NUMBER_INT
        self.SINGLEORDERSL = DEFAULT_NUMBER_FLOAT
        self.SINGLEORDERTP = DEFAULT_NUMBER_FLOAT
        self.F = ""
        self.ARRANGEMENTS_OF_TRADES = DEFAULT_NUMBER_FLOAT
        self.G = ""
        self.LOTS = DEFAULT_NUMBER_FLOAT
        self.SLIPPAGE = DEFAULT_NUMBER_FLOAT
        self.H = ""
        self.SET_UP_OF_LOSS = False
        self.AMOUNT_OF_LOSS = DEFAULT_NUMBER_FLOAT
        self.I = ""
        self.CLOSING_OF_ALL_TRADES = False
        self.J = ""
        self.USENEWSFILTER = False
        self.MINSBEFORENEWS = DEFAULT_NUMBER_INT
        self.MINSAFTERNEWS = DEFAULT_NUMBER_INT
        self.NEWSIMPACT = DEFAULT_NUMBER_FLOAT
        self.K = ""
        self.FILTERING = False
        self.L = ""
        self.AUTOEQUITYMANAGER = False
        self.EQUITYGAINPERCENT = DEFAULT_NUMBER_FLOAT
        self.SAFEEQUITYSTOPOUT = False
        self.SAFEEQUITYRISK = DEFAULT_NUMBER_FLOAT

        # new variables which will be changed in the class
        self.net_profit = DEFAULT_NUMBER_FLOAT
        self.ords_in_a_day = DEFAULT_NUMBER_INT
        self.current_datetime = DEFAULT_NUMBER_FLOAT  # (year + month + day + hour + minute + second  in SECOND)
        self.current_day = DEFAULT_NUMBER_FLOAT  # (year + month + day in DAYS)
        self.current_time = DEFAULT_NUMBER_FLOAT  # (hour + minute + second in SECOND)
        self.current_datetime_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_day_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_time_nexttick = DEFAULT_NUMBER_FLOAT  
        self.bid_price = DEFAULT_NUMBER_FLOAT
        self.ask_price = DEFAULT_NUMBER_FLOAT
        self.bid_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.ask_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.yesterday_close = DEFAULT_NUMBER_FLOAT
        self.mode_spread = DEFAULT_NUMBER_FLOAT
        self.order_ID_dict = {}  # a dictionary (as a hash-map) for storing ID
        
        self.SpreadMax = DEFAULT_NUMBER_FLOAT
        self.Hour_of_trading_from = DEFAULT_NUMBER_INT
        self.Hour_of_trading_to = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_hours = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_minutes = DEFAULT_NUMBER_INT
        self.Time_closing_trades = False
        self.Lots = DEFAULT_NUMBER_FLOAT
        self.Slippage = DEFAULT_NUMBER_FLOAT
        
        self.balance = DEPOSIT
        self.CurrentProfit = DEFAULT_NUMBER_FLOAT  # current profit of all Opened orders (OP_BUY & OP_SELL)
        self.equity = self.balance + self.CurrentProfit
        
        self.EVENTS_OF_CALENDAR_ALL_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_BASE_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS = []
        self.TIMEFRAME_TICK_DATA = []
        self.TIMEFRAME_OHLC_DATA = []
        
        # Create dictionaries for storing Closed, Deleted, and Opened/Pending orders with KEY is OrderID
        self.ORDER_CLOSED_DICT = {} 
        self.ORDER_OPENED_DICT = {} 
        self.ORDER_DELETED_DICT = {} 
        
        # old variables from EA
        self.NDigits = DEFAULT_SECOND_NUMBER_FLOAT
        self.PipValue = DEFAULT_SECOND_NUMBER_FLOAT
        self.my_point = DEFAULT_SECOND_NUMBER_FLOAT
        
        self.ATR_Period = 7.0
        self.ATRPeriod1 = 3.0
        self.ATRPeriod2 = 5.0 
        self.ATRUpLimit1 = 13.0
        self.ATRDnLimit1 = 7.0
        self.ATRUpLimit2 = 21.0 
        self.ATRDnLimit2 = 16.0
        self.ATRUpLimit3 = 28.0
        self.ATRDnLimit3 = 25.0
        self.DeletePOATR = True      
        self.DeleteOrderATR = False
        
        self.LF = "\n"  
        self.ObjCount = DEFAULT_NUMBER_INT  
        self.FirstTime33 = False
        self.FirstTime35 = False
        self.Today6 = -1
        self.Count32 = DEFAULT_NUMBER_INT
        self.dblProfit = DEFAULT_NUMBER_FLOAT
        self.ATR = ""
        self.Trading = ""
        self.OrderCounter = DEFAULT_NUMBER_INT  # total Opened and Pending orders
        self.SellOrderExists = False
        self.BuyOrderExists = False
        self.BuyPOExists = False
        self.SellPOExists = False
        self.Overide = False
        self.Hour1 = DEFAULT_SECOND_NUMBER_INT
        self.Minute1 = DEFAULT_NUMBER_INT
        self.MagicChange = ""
        self.RMStatus = ""
        
        self.clear = False
    
    #===============================================================================
    def reset(self):
        '''
        Constructor
        '''
        # get the total parameters for running EA
        self.NAME_EA = ""
        self.MAGIC = DEFAULT_NUMBER_INT
        self.FILTERSPREAD = False
        self.SPREADMAX = DEFAULT_NUMBER_FLOAT
        self.A = ""
        self.MONDAY = False
        self.TUESDAY = False
        self.WEDNESDAY = False
        self.THURSDAY = False
        self.FRIDAY = False
        self.SATURDAY = False
        self.SUNDAY = False
        self.B = ""
        self.TRADING_24H = False
        self.GMT_OFFSET = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_FROM = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_TO = DEFAULT_NUMBER_INT
        self.USE_ORDERSLIMIT = False
        self.OPENORDERSLIMITDAY = DEFAULT_NUMBER_INT
        self.C = ""
        self.TIME_CLOSING_TRADES = False
        self.TIME_OF_CLOSING_IN_HOURS = DEFAULT_NUMBER_INT
        self.TIME_OF_CLOSING_IN_MINUTES = DEFAULT_NUMBER_INT
        self.D = ""
        self.PROFIT = False
        self.PROFIT_ALL_ORDERS = DEFAULT_NUMBER_FLOAT
        self.E = ""
        self.OPENORDERSLIMIT = DEFAULT_NUMBER_INT
        self.SINGLEORDERSL = DEFAULT_NUMBER_FLOAT
        self.SINGLEORDERTP = DEFAULT_NUMBER_FLOAT
        self.F = ""
        self.ARRANGEMENTS_OF_TRADES = DEFAULT_NUMBER_FLOAT
        self.G = ""
        self.LOTS = DEFAULT_NUMBER_FLOAT
        self.SLIPPAGE = DEFAULT_NUMBER_FLOAT
        self.H = ""
        self.SET_UP_OF_LOSS = False
        self.AMOUNT_OF_LOSS = DEFAULT_NUMBER_FLOAT
        self.I = ""
        self.CLOSING_OF_ALL_TRADES = False
        self.J = ""
        self.USENEWSFILTER = False
        self.MINSBEFORENEWS = DEFAULT_NUMBER_INT
        self.MINSAFTERNEWS = DEFAULT_NUMBER_INT
        self.NEWSIMPACT = DEFAULT_NUMBER_FLOAT
        self.K = ""
        self.FILTERING = False
        self.L = ""
        self.AUTOEQUITYMANAGER = False
        self.EQUITYGAINPERCENT = DEFAULT_NUMBER_FLOAT
        self.SAFEEQUITYSTOPOUT = False
        self.SAFEEQUITYRISK = DEFAULT_NUMBER_FLOAT

        # new variables which will be changed in the class
        self.total_win = DEFAULT_NUMBER_FLOAT 
        self.total_loss = DEFAULT_NUMBER_FLOAT
        self.net_profit = DEFAULT_NUMBER_FLOAT
        self.ords_in_a_day = DEFAULT_NUMBER_INT
        self.current_datetime = DEFAULT_NUMBER_FLOAT  # (year + month + day + hour + minute + second + millisecond in MILLISECOND)
        self.current_day = DEFAULT_NUMBER_FLOAT  # (year + month + day in DAYS)
        self.current_time = DEFAULT_NUMBER_FLOAT  # (hour + minute + second + millisecond in MILLISECOND)
        self.current_datetime_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_day_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_time_nexttick = DEFAULT_NUMBER_FLOAT  
        self.bid_price = DEFAULT_NUMBER_FLOAT
        self.ask_price = DEFAULT_NUMBER_FLOAT
        self.bid_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.ask_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.yesterday_close = DEFAULT_NUMBER_FLOAT
        self.mode_spread = DEFAULT_NUMBER_FLOAT
        self.order_ID_dict = {}  # a dictionary (as a hash-map) for storing ID
            
        self.SpreadMax = DEFAULT_NUMBER_FLOAT
        self.Hour_of_trading_from = DEFAULT_NUMBER_INT
        self.Hour_of_trading_to = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_hours = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_minutes = DEFAULT_NUMBER_INT
        self.Time_closing_trades = False
        self.Lots = DEFAULT_NUMBER_FLOAT
        self.Slippage = DEFAULT_NUMBER_FLOAT
        
        self.balance = DEPOSIT
        self.CurrentProfit = DEFAULT_NUMBER_FLOAT  # current profit of all Opened orders (OP_BUY & OP_SELL)
        self.equity = self.balance + self.CurrentProfit
        
        self.EVENTS_OF_CALENDAR_ALL_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_BASE_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS = []
        self.TIMEFRAME_TICK_DATA = []
        self.TIMEFRAME_OHLC_DATA = []
        
        # Create a dictionary (as a hash-map) for storing Closed, Deleted, and Opened/Pending orders with KEY is OrderID
        self.ORDER_CLOSED_DICT = {} 
        self.ORDER_OPENED_DICT = {} 
        self.ORDER_DELETED_DICT = {} 
       
        # old variables from EA
        self.NDigits = DEFAULT_SECOND_NUMBER_FLOAT
        self.PipValue = DEFAULT_SECOND_NUMBER_FLOAT
        self.my_point = DEFAULT_SECOND_NUMBER_FLOAT
        
        self.ATR_Period = 7.0
        self.ATRPeriod1 = 3.0
        self.ATRPeriod2 = 5.0 
        self.ATRUpLimit1 = 13.0
        self.ATRDnLimit1 = 7.0
        self.ATRUpLimit2 = 21.0 
        self.ATRDnLimit2 = 16.0
        self.ATRUpLimit3 = 28.0
        self.ATRDnLimit3 = 25.0
        self.DeletePOATR = True      
        self.DeleteOrderATR = False
        
        self.LF = "\n"  
        self.ObjCount = DEFAULT_NUMBER_INT  
        self.FirstTime33 = False
        self.FirstTime35 = False
        self.Today6 = -1
        self.Count32 = DEFAULT_NUMBER_INT
        self.dblProfit = DEFAULT_NUMBER_FLOAT
        self.ATR = ""
        self.Trading = ""
        self.OrderCounter = DEFAULT_NUMBER_INT  # total Opened and Pending orders
        self.SellOrderExists = False
        self.BuyOrderExists = False
        self.BuyPOExists = False
        self.SellPOExists = False
        self.Overide = False
        self.Hour1 = DEFAULT_SECOND_NUMBER_INT
        self.Minute1 = DEFAULT_NUMBER_INT
        self.MagicChange = ""
        self.RMStatus = ""
        
        self.clear = False

    #===============================================================================
    def BrokerIs5Digit_0(self):
        ''' Return TRUE if the Broker is the 5 Digits Broker '''
    
        if (self.NDigits == 5 or self.NDigits == 3): 
            return(True)
        else:
            return(False)

    #===============================================================================
    def CalculateProfit_5(self, entry_price, exit_price, lots, order_type):
        ''' Calculates the profit or loss of a position in the home currency of the account. 
        1/When you go long, you enter the market at the ASK price and exit the market at BID price.
        2/When you go short, you enter the market at the BID price and exit at the ASK price.
        3/Pip Value = Pip in decimal places / Market Price * Trade Size
        For QUOTE_CURRENCY = 'USD', Pip Value will be multiple to Market Price 1 more time
        
        ==> Pip in decimal places = 0.0001 since 1/10,000th is a pip for all pairs (except JPY pairs)
                              = 0.01 for a JPY pair.
        ==> In all pairs involving the Japanese Yen (JPY), a pip is the 1/100th place -- 2 places to the right of the decimal. 
        In all other currency pairs, a pip is the 1/10,000 the place -- 4 places to the right of the decimal.
        '''
        
#         OLD CODES (17/01/2018_17:00:00)
#         result = DEFAULT_NUMBER_FLOAT
#     
#         if  (order_type == OP_BUY): 
#             result = ((exit_price - entry_price) * self.Lots * (1 / self.my_point) 
#                       * (PIP_VALUE_DICT[SYMBOL] * self.Lots / EXCHANGE_RATE_USD[QUOTE_CURRENCY]))
#         
#         
#         elif (order_type == OP_SELL):
#             result = ((entry_price - exit_price) * self.Lots * (1 / self.my_point) 
#                       * (PIP_VALUE_DICT[SYMBOL] * self.Lots / EXCHANGE_RATE_USD[QUOTE_CURRENCY]))
#         
#         return result
     
        result = DEFAULT_NUMBER_FLOAT
     
        if  (order_type == OP_BUY): 
            result = (exit_price - entry_price) * lots * ONE_LOT_VALUE - COMMISSION
         
        elif (order_type == OP_SELL):
            result = (entry_price - exit_price) * lots * ONE_LOT_VALUE - COMMISSION
        
        return round(float(result), self.NDigits)
        
    #===============================================================================
    def CreateUniqueOrderID_9(self, order_type):
        '''Create the unique order ID. Return -1 when cannot generate an order ID. '''
        
        # create the unique order ID which is the combination of all Values of parameters
        new_id = self.current_datetime + float(datetime.now().second)
        
        # keep create an individual while the ID is not unique
        while (new_id in self.order_ID_dict):
            new_id = self.current_datetime + float(datetime.now().second)
        
        # save new ID into the ID dictionary
        self.order_ID_dict[new_id] = order_type
        
        return new_id
    
    #===============================================================================
    def MaxOrders_9(self, num):
        ''' Return TRUE if the total number of orders in a day equal the Orders limit per day
            and delete all pending order in Opened and Pending orders pool when max orders reached '''
        
        ords = self.ords_in_a_day
        
        if (self.USE_ORDERSLIMIT == False): 
            return False
        
#         # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
#         # get all Opened and Pending orders in the pool
#         for order_id in self.ORDER_OPENED_DICT.keys():
#             # --> get the date-time of the opened/pending orders
#             opened_order = self.ORDER_OPENED_DICT[order_id]
#             order_type = opened_order[ORDER_TYPE_COL_INDEX]
#             OrderOpenTime = opened_order[DAY_COL_INDEX]
#             
#             # --> count orders when orders are BUY/SELL and in the current day (replace for: iBarShift(NULL,PERIOD_D1,OrderOpenTime())==0)
#             if (order_type < 2.00 and OrderOpenTime == self.current_day):
#                 ords += DEFAULT_SECOND_NUMBER_INT
#         
#         # get all Closed orders in the pool
#         for order_id in self.ORDER_CLOSED_DICT.keys():
#             # --> get the date-time of the closed/deleted orders and current date-time
#             closed_order = self.ORDER_CLOSED_DICT[order_id]
#             order_type = closed_order[ORDER_TYPE_COL_INDEX]
#             OrderClosedTime = float(closed_order[DAY_COL_INDEX])
#             
#             # --> count orders when orders are BUY/SELL and in the current day (replace for: iBarShift(NULL,PERIOD_D1,OrderOpenTime())==0)
#             if (order_type < 2.00 and OrderClosedTime == self.current_day):
#                 ords += DEFAULT_SECOND_NUMBER_INT
        
        # delete all pending order in Opened and Pending orders pool when max orders reached
        if (ords >= num):
            # get all Opened and Pending orders in the pool
            for order_id in self.ORDER_OPENED_DICT.keys():
               
                order = self.ORDER_OPENED_DICT[order_id]
                order_type = order[ORDER_TYPE_COL_INDEX]
            
                if (order_type > 1.00):
                    # --> delete orders when they are BUYLIMIT/SELLLIMIT
                    self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)
                    
                    # --> save this deleted orders in the Deleted orders pool
                    self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
    
            # max number of orders reached
            return True  
        else:
            return False
        
    #===============================================================================
    def ProfitCheck_3(self):
        ''' Return Profit of all closed trades following the '''
    
        net_profit = DEFAULT_NUMBER_FLOAT
        
        # get all the profits from Opened and Pending orders pool
        for order_id in self.ORDER_OPENED_DICT.keys():  # The order of the k's is not defined
            order = self.ORDER_OPENED_DICT[order_id]
            net_profit += order[PROFIT_COL_INDEX]
        
        return net_profit
        
    #===============================================================================
    def AccountBalance_1(self):
        ''' Return current balance of all orders '''
    
        account_bal = self.balance
        
#         if (len(self.ORDER_OPENED_DICT) == DEFAULT_NUMBER_INT and len(self.ORDER_CLOSED_DICT) == DEFAULT_NUMBER_INT):
#             return account_bal
#         else:
#             # get all the balance from Closed orders pool
#             for order_id in self.ORDER_CLOSED_DICT.keys():  # The order of the k's is not defined
# 
#                 order = self.ORDER_CLOSED_DICT[order_id]
#                 if (order[BALANCE_COL_INDEX] > account_bal):
#                     account_bal = order[BALANCE_COL_INDEX]
#     
#             # get all the balance from Opened and Pending orders pool
#             for order_id in self.ORDER_OPENED_DICT.keys():  # The order of the k's is not defined
# 
#                 order = self.ORDER_OPENED_DICT[order_id]
#                 if (order[BALANCE_COL_INDEX] > account_bal):
#                     account_bal = order[BALANCE_COL_INDEX]

        return account_bal
    
    #===============================================================================
    def DayOfWeek_3(self):
        ''' Return the current zero-based day of the week (0-Monday,1,2,3,4,5,6) 
        for the Tick data. '''
        
        # get back the date from number
        scurrentday = date.fromordinal(DATEOFFSET + int(self.current_day))
        
        # slit date into year, month, and day
        dividend = str(scurrentday).split('-')
        year = dividend[DEFAULT_NUMBER_INT]
        month = dividend[DEFAULT_SECOND_NUMBER_INT]
        day = dividend[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
        
        # get the day of the week from selected date
        day_of_week = date(int(year), int(month), int(day)).weekday()
        
        return day_of_week
    
    #===============================================================================
    def TimeHour_4(self):
        ''' Return the Hour(s) of the Tick data. '''
    
        hour_minute_second = int(self.current_time) 
        
        hour_tick = int(hour_minute_second / SECONDS_OF_ANHOUR)
        
        return hour_tick
    
    #===============================================================================
    def TimeMinute_3(self):
        ''' Return the Minute(s) of the Tick data. '''
        
        hour_minute_second = int(self.current_time) 
        
        minute_tick = int(hour_minute_second % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
        
        return minute_tick
    
    #===============================================================================
    def TimeHour_4_WithMilliSecondFormat(self):
        ''' Return the Hour(s) of the Tick data. '''
    
        # hr_min_sec_ms = self.current_time
        hour_minute_second = int(self.current_time / MILLISECONDS_OF_ASECOND) 
        
        hour_tick = int(hour_minute_second / SECONDS_OF_ANHOUR)
        
        return hour_tick
    
    #===============================================================================
    def TimeMinute_3_WithMilliSecondFormat(self):
        ''' Return the Minute(s) of the Tick data. '''
        
        # hr_min_sec_ms = self.current_time
        hour_minute_second = int(self.current_time / MILLISECONDS_OF_ASECOND) 
        
        minute_tick = int(hour_minute_second % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
        
        return minute_tick
    
    #===============================================================================
    def TimeSecond_3_WithMilliSecondFormat(self):
        ''' Return the Second(s) of the Tick data. '''
        
        # hr_min_sec_ms = self.current_time
        hour_minute_second = int(self.current_time / MILLISECONDS_OF_ASECOND) 
        
        second_tick = int(hour_minute_second % SECONDS_OF_ANHOUR % SECONDS_OF_AMINUTE)
        
        return second_tick
    
    #===============================================================================
    def TimeMilliSecond_3_WithMilliSecondFormat(self):
        ''' Return the MilliSecond(s) of the Tick data. '''
        
        return int(self.current_time % MILLISECONDS_OF_ASECOND)
    
    #===============================================================================
    def MODE_SPREAD_1(self, bid_price, ask_price):
        ''' Return spread of one record in TICK_DATA. '''
    
        spread = abs(bid_price - ask_price)
        
        for i in range(self.NDigits):
            spread *= float(10)
        
        return spread
    
    #===============================================================================
    def OrderType_5(self, order_id, dict_data):
        ''' Return order type of a record in the data. 
            OP_BUY          = 0.00
            OP_SELL         = 1.00
            OP_BUYLIMIT     = 2.00
            OP_SELLLIMIT    = 3.00
            OP_BUYSTOP      = 4.00
            OP_SELLSTOP     = 5.00 '''
        
        order_type = -1
        
        if (len(dict_data) != DEFAULT_NUMBER_INT):
            order = dict_data[order_id]
            order_type = float(order[ORDER_TYPE_COL_INDEX])
        else:
            log.info("There is NO data. Data size = 0")
                
        return order_type
    
    #===============================================================================
    def OrderDelete_4(self, order_id, dict_data):
        ''' Delete s specific order in data. '''
    
        # delete the order if it's existed in the data
        if (order_id in dict_data):
            del dict_data[order_id]
            return True
        else:
            log.info("There's NO %s in data. Data is the same as before deleting." % order_id)
            return False
        
    #===============================================================================
    def OrderAdd_10(self, order_id, order, dict_data):
        ''' Add a specific order in data. '''
    
        # add the order if it's NOT existed in the data
        if (order_id in dict_data):
            log.info("There's the oder %s in data already." % order_id)
            return False
        else:
            # add order to the data
            dict_data[order_id] = order
            return True
        
    #===============================================================================
    def OrderClose_4(self, order, order_id, order_type):
        ''' Close a specific old_opended_order in data by:
        * deleting this order in the Opened and Pending orders pool 
        * update the new values for this order from Opened to Close position
        * and save this deleted order in the Closed orders pools'''
        
        flag_order_closed = True
        
        # get the specific order
        new_closed_order = order
         
        if (order_type == OP_BUY or order_type == OP_SELL):
            # ORDER_OPENED_DICT[] = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
            # delete this order in the Opened and Pending orders pool
            if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                 
                # update the new values for this order from Opened to Close position
                profit = new_closed_order[PROFIT_COL_INDEX]
                self.balance = self.balance + profit
                                                 
                new_closed_order[DATETIME_COL_INDEX] = self.current_datetime
                new_closed_order[DAY_COL_INDEX] = self.current_day
                new_closed_order[TIME_COL_INDEX] = self.current_time
                new_closed_order[BALANCE_COL_INDEX] = self.balance 
                 
                # save this NEW Closed order in the Closed orders pool
                flag_order_closed = self.OrderAdd_10(order_id, new_closed_order, self.ORDER_CLOSED_DICT)    
                
            else:
                flag_order_closed = False
        
        # inform the result after placing the pending order OP_SELLLIMIT
        if (flag_order_closed):
#             print("Successfully Close the Opened order %s." % order_id)
            log.info("Successfully Close the Opened order %s." % order_id)
        else:
#             print("Error when closing the Opened order %s." % order_id)
            log.info("Error when closing the Opened order %s." % order_id)

        return flag_order_closed
         
    #===============================================================================
    def DeletePendingOrder19_3(self):
        ''' Delete an order OP_SELLLIMIT in the Opened and Pending order pool. '''
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
                
            # when the order is OP_SELLLIMIT
            if (order_type == OP_SELLLIMIT):
                # --> delete this OP_SELLLIMIT in the Opened and Pending orders pool
                if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                    # --> update date time and save this deleted OP_SELLLIMIT in the Deleted orders pool
                    order[DATETIME_COL_INDEX] = self.current_datetime
                    order[DAY_COL_INDEX] = self.current_day
                    order[TIME_COL_INDEX] = self.current_time
                    self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
        
    #===============================================================================
    def DeletePendingOrder18_3(self):
        ''' Delete an order OP_BUYLIMIT in the Opened and Pending order pool. '''
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # when the order is OP_BUYLIMIT
            if (order_type == OP_BUYLIMIT):
                # --> delete this OP_BUYLIMIT in the Opened and Pending orders pool
                if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                    # --> update date time and save this deleted OP_BUYLIMIT in the Deleted orders pool
                    order[DATETIME_COL_INDEX] = self.current_datetime
                    order[DAY_COL_INDEX] = self.current_day
                    order[TIME_COL_INDEX] = self.current_time
                    self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
        
    #===============================================================================
    def CheckLastOrderType33_4(self):
        ''' Check the last order and delete the pending OP_SELLLIMIT order when the last order was OP_SELL. '''
        
        orderType = -1.00
        lastCloseTime = DEFAULT_NUMBER_FLOAT

        # get all Closed orders in the pool
        # ORDER_CLOSED_DICT = {order_id:['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_CLOSED_DICT.keys():

            closed_order = self.ORDER_CLOSED_DICT[order_id]
            OrderCloseTime = closed_order[DATETIME_COL_INDEX]
            
            if (lastCloseTime < OrderCloseTime):
                lastCloseTime = OrderCloseTime
                orderType = closed_order[ORDER_TYPE_COL_INDEX]
        
        # delete the opened OP_SELLLIMIT orders when the last order was OP_SELL
        if (orderType == OP_SELL or self.FirstTime33):
            self.FirstTime33 = False
            self.DeletePendingOrder19_3()
    
    #===============================================================================
    def MathMax_6(self, float_num_1, float_num_2):
        max_number = DEFAULT_NUMBER_FLOAT
    
        if float_num_1 >= float_num_2:
            max_number = float_num_1
        else:
            max_number = float_num_2
                
        return max_number
    
    #===============================================================================
    def NormalizeDouble_9(self, float_num, digit_num):
        
        list_normalized_num = str_num = list(str(float_num))
            
        for i in range(len(str_num)):
            if (str_num[i] == '.'):
                # only normalize when numbers of digit numbers after decimal point matching input digit
                if (len(str_num) - i > i + digit_num):
                    # get all digits from float number until the expected digit number after decimal point
                    for j in range(i + digit_num):
                        list_normalized_num[j] = str_num[j]
                    
                    # assign the rest of the expected float number
                    k = len(str_num) - DEFAULT_SECOND_NUMBER_INT
                    while (k > i + digit_num):
                        if (digit_num == DEFAULT_NUMBER_INT):
                            list_normalized_num[k] = '0'
                        else:
                            list_normalized_num[k] = '9'
                        k -= DEFAULT_SECOND_NUMBER_INT    
                    
                break
        
        str_normalized_num = ''.join(list_normalized_num)
        
        return float(str_normalized_num)
        
    #===============================================================================
    def OrderSend_9(self, order_id, order_type, order_lots, order_price, order_slippage, order_sl, order_tp):
        ''' In this EA, this function is to place a Pending order OP_BUYLIMIT or OP_SELLLIMIT. 
        * return False when the order is not a Pending order.
        * order_slippage: Maximum price slippage (for buy or sell orders only). 
        * order_expire: Order expiration time (for pending orders only).'''

        # calculate slippage_in_decimal
        slippage_in_decimal = order_slippage
        for i in range(self.NDigits):
            slippage_in_decimal /= float(10)

        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        
        if (order_type != OP_BUYLIMIT and order_type != OP_SELLLIMIT):
            # print("This is not a Pending order OP_BUYLIMIT or OP_SELLLIMIT. Its type is %s." % (order_id, order_type))
            log.info("This is not a Pending order OP_BUYLIMIT or OP_SELLLIMIT. Its type is %s." % (order_id, order_type))
            return False
        # create a pending order OP_BUYLIMIT or OP_SELLLIMIT
        else:
            if (order_type == OP_BUYLIMIT):
                entry_price = order_price + slippage_in_decimal
                
            elif (order_type == OP_SELLLIMIT):
                entry_price = order_price - slippage_in_decimal
            
            order = [self.current_datetime,
                     self.current_day,
                     self.current_time,
                     order_type,
                     order_id,
                     order_lots,
                     round(entry_price, self.NDigits),
                     DEFAULT_NUMBER_FLOAT,
                     order_sl,
                     order_tp,
                     DEFAULT_NUMBER_FLOAT,
                     DEFAULT_NUMBER_FLOAT]
           
            # save this order in the Opened and Pending orders pool
            flag_added = self.OrderAdd_10(order_id, order, self.ORDER_OPENED_DICT)
            
            if (flag_added):
                return True
            
    #===============================================================================
    def BuyPendingOrder13_8(self):
        ''' Buy Pending Order OP_BUYLIMIT. '''
        
        # exit when reaching maximum orders per day
        if (self.MaxOrders_9(self.OPENORDERSLIMITDAY)):
            return
        
        # calculate all variables for placing an order
        price = (self.NormalizeDouble_9(self.ask_price, self.NDigits) 
                 + (self.ARRANGEMENTS_OF_TRADES * self.PipValue) * self.my_point)
        
        # calculate Stop Loss (SL) and Take Profit (TP_
        SL = price - (self.SINGLEORDERSL * self.PipValue * self.my_point)
        if (self.SINGLEORDERSL == DEFAULT_NUMBER_FLOAT):
            SL = DEFAULT_NUMBER_FLOAT
        
        TP = price + (self.SINGLEORDERTP * self.PipValue * self.my_point)
        if (self.SINGLEORDERTP == DEFAULT_NUMBER_FLOAT):
            TP = DEFAULT_NUMBER_FLOAT
           
        # place the pending order OP_BUYLIMIT
        order_id = self.CreateUniqueOrderID_9(OP_BUYLIMIT)
        ticket = self.OrderSend_9(order_id, OP_BUYLIMIT, self.Lots, price, self.SLIPPAGE, SL, TP)
        
        # inform the result after placing the pending order OP_BUYLIMIT
        if (ticket == False):
#             print("OrderSend_9() error for OP_BUYLIMIT %s" % order_id)
            log.info("OrderSend_9() error for OP_BUYLIMIT %s" % order_id)
        else:
#             print("Successfully placed the Pending order OP_BUYLIMIT %s." % order_id)
            log.info("Successfully placed the Pending order OP_BUYLIMIT %s." % order_id)
            
    #===============================================================================
    def SellPendingOrder14_8(self):
        ''' Sell Pending Order OP_SELLLIMIT. '''
        
        # exit when reaching maximum orders per day
        if (self.MaxOrders_9(self.OPENORDERSLIMITDAY)):
            return
        
        # calculate all variables for placing an order
        price = (self.NormalizeDouble_9(self.ask_price, self.NDigits) 
                 - (self.ARRANGEMENTS_OF_TRADES * self.PipValue) * self.my_point)
        
        # calculate Stop Loss (SL) and Take Profit (TP_
        SL = price + (self.SINGLEORDERSL * self.PipValue * self.my_point)
        if (self.SINGLEORDERSL == DEFAULT_NUMBER_FLOAT):
            SL = DEFAULT_NUMBER_FLOAT
        
        TP = price - (self.SINGLEORDERTP * self.PipValue * self.my_point)
        if (self.SINGLEORDERTP == DEFAULT_NUMBER_FLOAT):
            TP = DEFAULT_NUMBER_FLOAT
        
        # place the pending order OP_SELLLIMIT
        order_id = self.CreateUniqueOrderID_9(OP_SELLLIMIT)
        ticket = self.OrderSend_9(order_id, OP_SELLLIMIT, self.Lots, price, self.SLIPPAGE, SL, TP)
        
        # inform the result after placing the pending order OP_SELLLIMIT
        if (ticket == False):
#             print("OrderSend_9() error for OP_SELLLIMIT %s" % order_id)
            log.info("OrderSend_9() error for OP_SELLLIMIT %s" % order_id)
        else:
#             print("Successfully placed the Pending order OP_SELLLIMIT %s." % order_id)
            log.info("Successfully placed the Pending order OP_SELLLIMIT %s." % order_id)
            
    #===============================================================================
    def IfSellOrderDoesNotExist4_7(self, Mode):
        ''' Check whether the order OP_SELL existed in the Opened and Pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_SELL
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_SELL:
                self.SellOrderExists = True
                exists = True
            else:
                self.SellOrderExists = False
                
        if (exists == False and Mode == DEFAULT_SECOND_NUMBER_INT):
            self.BuyPendingOrder13_8()
        
        if (exists == True and Mode == 2):
            self.DeletePendingOrder18_3();
    
    #===============================================================================
    def IfBuyOrderDoesNotExist6_7(self, Mode):
        ''' Check whether the order OP_BUY existed in the Opened and Pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_BUY
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_BUY:
                self.BuyOrderExists = True
                exists = True
            else:
                self.BuyOrderExists = False
                
        if (exists == False and Mode == DEFAULT_SECOND_NUMBER_INT):
            self.SellPendingOrder14_8()
        
        if (exists == True and Mode == 2):
            self.DeletePendingOrder19_3();
    
    #===============================================================================
    def IfOrderDoesNotExist11_6(self):
        ''' Check whether the order OP_BUYLIMIT existed in the opned and pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_BUYLIMIT
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_BUYLIMIT:
                self.BuyPOExists = True
                exists = True
            else:
                self.BuyPOExists = False
                
        if (exists == False):
            self.IfSellOrderDoesNotExist4_7(1)
        
        if (exists == True):
            self.IfSellOrderDoesNotExist4_7(2);
        
    #===============================================================================
    def IfOrderDoesNotExist12_6(self):
        ''' Check whether the order OP_SELLLIMIT existed in the opned and pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_SELLLIMIT
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_SELLLIMIT:
                self.SellPOExists = True
                exists = True
            else:
                self.SellPOExists = False
                
        if (exists == False):
            self.IfBuyOrderDoesNotExist6_7(1)
        
        if (exists == True):
            self.IfBuyOrderDoesNotExist6_7(2);
    
    #===============================================================================
    def ExpMovingAverage(self, values, window):
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()
        a = np.convolve(values, weights, mode='full')[:len(values)]
        a[:window] = a[window]
        
        return a
    
    #===============================================================================
    def iTrueRange(self, open, high, low, close, yesterday_close):
        
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
    def ATRPips(self, atr, size, point):
        
        # create the atr_pips list following the size of atr
        data_col = len(atr[DEFAULT_NUMBER_INT]) 
        data_row = len(atr)
        atr_pips = [[DEFAULT_NUMBER_FLOAT for x in range(data_col)] for y in range(data_row)] 
        
        for row_count in range(int(size)):
            for col_count in range(len(atr[row_count])):
                atr_pips[row_count][col_count] = int(float(atr[row_count][col_count]) / point)
        
        return atr_pips

    #===============================================================================
    def ohlc_resample(self, timeframe_tickdata):
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
    def iATR(self, period, shift):
        ''' ATR function '''

        if (len(self.TIMEFRAME_OHLC_DATA) > int(period - shift)
            and int(period - shift) > DEFAULT_NUMBER_INT):
            # calculate the True Range and ATR
            TrueRanges = []
            open_inx_col = 0
            high_inx_col = 1
            low_inx_col = 2
            close_inx_col = 3
            
            for rate in self.TIMEFRAME_OHLC_DATA:
                openp = float(str(rate[open_inx_col]))
                highp = float(str(rate[high_inx_col]))
                lowp = float(str(rate[low_inx_col]))
                closep = float(str(rate[close_inx_col]))
                
                TrueRange = self.iTrueRange(openp, highp, lowp, closep, self.yesterday_close)
        
                # save TrueRange into an array for ATR calculation            
                TrueRanges.append(TrueRange)
            
            ATR = self.ExpMovingAverage(TrueRanges, int(period - shift))
            ATR_list = np.array(ATR).tolist()
            
        else:
            ATR_list = []
        
        return ATR_list

    #===============================================================================
    def ATRFilter_5(self):
        ''' ATRFilter_5. '''

        atr = [DEFAULT_NUMBER_FLOAT for i in range(int(self.MathMax_6(self.ATRPeriod1, self.ATRPeriod2) + self.ATR_Period))]
        
        # calculate open, high, low, close of the bid price following the TIME FRAME 
        self.TIMEFRAME_OHLC_DATA.append(self.ohlc_resample(self.TIMEFRAME_TICK_DATA))
        
        # calculate the ATR
        for i in range(int(self.MathMax_6(self.ATRPeriod1, self.ATRPeriod2) + self.ATR_Period)):
            # iATR(Symbol(), TIME_FRAME, self.ATR_Period, i): Calculates the Average True Range indicator and returns its value.
            atr[i] = self.iATR(self.ATR_Period, i)
           
        # calculate the ATR_PIP
        if (len(atr[DEFAULT_NUMBER_INT]) != DEFAULT_NUMBER_INT):
            atr_pips = self.ATRPips(atr, self.MathMax_6(self.ATRPeriod1, self.ATRPeriod2) + self.ATR_Period, self.my_point)
        else:
            atr_pips = [DEFAULT_NUMBER_FLOAT for i in range(int(self.MathMax_6(self.ATRPeriod1, self.ATRPeriod2) + self.ATR_Period))]
            
        # retrieve back the results from ATR_PIP
        atr_p = atr_pips[DEFAULT_NUMBER_INT]
        ATRPrePips1 = atr_pips[int(self.ATRPeriod1)]
        ATRPrePips2 = atr_pips[int(self.ATRPeriod2)]
         
        # placing Pending orders with constraints
        if ((((ATRPrePips1 >= self.ATRDnLimit1 and ATRPrePips1 <= self.ATRUpLimit1 and ATRPrePips2 >= self.ATRDnLimit1 and ATRPrePips2 <= self.ATRUpLimit1 and atr_p >= self.ATRDnLimit1 and atr_p <= self.ATRUpLimit1) 
              or (ATRPrePips1 >= self.ATRDnLimit2 and ATRPrePips1 <= self.ATRUpLimit2 and ATRPrePips2 >= self.ATRDnLimit2 and ATRPrePips2 <= self.ATRUpLimit2 and atr_p >= self.ATRDnLimit2 and atr_p <= self.ATRUpLimit2) 
              or (ATRPrePips1 >= self.ATRDnLimit3 and ATRPrePips1 <= self.ATRUpLimit3 and ATRPrePips2 >= self.ATRDnLimit3 and ATRPrePips2 <= self.ATRUpLimit3 and atr_p >= self.ATRDnLimit3 and atr_p <= self.ATRUpLimit3)) 
             and(self.FILTERING == True)) or (self.SellOrderExists == True) or (self.BuyOrderExists == True)):
     
            ATR = "Not ATR filtering!"
            log.info(ATR)
            self.IfOrderDoesNotExist11_6()
            self.IfOrderDoesNotExist12_6()
        
        # TODO: DEMO --> START here: 2 functions lead to placing Pending orders 
        elif (ATRPrePips1 == DEFAULT_NUMBER_FLOAT and ATRPrePips2 == DEFAULT_NUMBER_FLOAT):
            ATR = "Not ATR filtering!"
            log.info(ATR)
            self.IfOrderDoesNotExist11_6()
            self.IfOrderDoesNotExist12_6()
        # DEMO --> END here
        else:
            ATR = "ATR Filtering!"
            log.info(ATR)
            if((self.DeletePOATR == True) and (self.FILTERING == True)):
                self.DeletePendingOrder18_3()
                self.DeletePendingOrder19_3()
             
            if((self.DeleteOrderATR == True) and (self.FILTERING == True)):
                self.CloseOrder16_3()
                self.CloseOrder17_3()
            
        if (self.FILTERING == False):  
            ATR = ""
            log.info(ATR)
            self.IfOrderDoesNotExist11_6()
            self.IfOrderDoesNotExist12_6()
        
    #===============================================================================
    def LimitOpenOrders28_4(self):
        ''' Count all the number in the Opened and Pending order pool. '''
    
        count = DEFAULT_NUMBER_INT
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        
        # TODO: function leads to place Pending orders
        if (len(self.ORDER_OPENED_DICT) == DEFAULT_NUMBER_INT or self.OPENORDERSLIMIT == DEFAULT_NUMBER_INT):
            self.ATRFilter_5()
        else:
            for i in self.ORDER_OPENED_DICT.keys():
                count += DEFAULT_SECOND_NUMBER_INT
                
                # TODO: function leads to place Pending orders
                if (count < self.OPENORDERSLIMIT) or (self.OPENORDERSLIMIT == DEFAULT_NUMBER_INT):
                    self.ATRFilter_5()  
                           
                if (self.SellOrderExists == False) and (self.BuyOrderExists == False):
                    count = DEFAULT_NUMBER_INT
                    self.OrderCounter = count
                else:
                    count = count - DEFAULT_SECOND_NUMBER_INT
                    self.OrderCounter = count
                
    #===============================================================================
    def CheckLastOrderType35_4(self):
        ''' Check the last order and delete the pending OP_BUYLIMIT order when the last order was OP_BUY. '''
        
        orderType = -1.00
        lastCloseTime = DEFAULT_NUMBER_FLOAT

        # get all Closed orders in the pool
        # ORDER_CLOSED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_CLOSED_DICT.keys():
            
            closed_order = self.ORDER_CLOSED_DICT[order_id]
            OrderCloseTime = closed_order[DATETIME_COL_INDEX]
            
            if (lastCloseTime < OrderCloseTime):
                lastCloseTime = OrderCloseTime
                orderType = closed_order[ORDER_TYPE_COL_INDEX]
        
        # delete the opened OP_BUYLIMIT orders when the last order was OP_BUY
        if (orderType == OP_BUY or self.FirstTime35):
            self.FirstTime35 = False
            self.DeletePendingOrder18_3()

    #===============================================================================
    def get_previous_event_minute(self, current_minute, list_data):   
        ''' Get the previous minute of Calendar data comparing with Tick Data '''
             
        previous_event_minute = DEFAULT_NUMBER_INT
        
        for row_index in range(len(list_data)):
            time = int(list_data[row_index][TIME_COL_INDEX])
            minute_calendar = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
            
            # stop when minute of Calendar data is greater than current minute of Tick data
            if (minute_calendar > current_minute
                and row_index != DEFAULT_NUMBER_INT):
                
                # get previous_event_minute
                previous_time = int(list_data[row_index][TIME_COL_INDEX])
                previous_event_minute = int(previous_time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)   
        
        return previous_event_minute
    
    #===============================================================================
    def get_next_event_minute(self, current_minute, list_data):        
        ''' Get the next minute and its index of Calendar data comparing with Tick Data '''
        
        next_event_minute = DEFAULT_NUMBER_INT
        next_event_minute_index = -1
        
        for row_index in range(len(list_data)):
            time = int(list_data[row_index][TIME_COL_INDEX])
            minute_calendar = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
            
            # stop when minute of Calendar data is less than current minute of Tick data
            if (minute_calendar > current_minute
                and row_index != DEFAULT_NUMBER_INT):
                
                # get next_event_minute
                next_event_minute = minute_calendar
                next_event_minute_index = row_index   
        
        return [next_event_minute, next_event_minute_index]
    
    #===============================================================================
    def NewsTime_4(self):
        ''' NewsTime_4. '''
        
        News = False
        PrevMinute = -1
        
        # set default values
        minutesSincePrevEvent = DEFAULT_NUMBER_INT
        minutesUntilNextEvent = DEFAULT_NUMBER_INT
        impactOfNextEvent = DEFAULT_NUMBER_INT
        
        if (self.TimeMinute_3() != PrevMinute):     
            
            PrevMinute = self.TimeMinute_3()
            
            # Check the Calendar Event of ALL SYMBOLS
            if (self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT] != DEFAULT_NUMBER_INT):
                # get minutesSincePrevEvent
                previous_event_minute = self.get_previous_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT])
                minutesSincePrevEvent = PrevMinute - previous_event_minute 
            
                # get nminutesUntilNextEvent
                [next_event_minute, next_event_minute_index] = self.get_next_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT]) 
                minutesUntilNextEvent = next_event_minute - PrevMinute
                
                # get value of News impact
                if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                     or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                    and next_event_minute_index != -1):
                    
                    next_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT]
                    impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                    if (impactOfNextEvent >= self.NEWSIMPACT): 
                        News = True
            else:
                # get minutesSincePrevEvent
                if (self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    previous_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
                    time = int(previous_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                    previous_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                else:
                    previous_event_minute = DEFAULT_NUMBER_INT
                    
                minutesSincePrevEvent = PrevMinute - previous_event_minute 
            
                # get nminutesUntilNextEvent
                if (self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    next_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                    time = int(next_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                    next_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                else:
                    next_event_minute = DEFAULT_NUMBER_INT
                
                next_event_minute_index = DEFAULT_NUMBER_INT 
                minutesUntilNextEvent = next_event_minute - PrevMinute
                
                # get value of News impact
                if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                     or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                    and next_event_minute_index != -1):
                    
                    next_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                    impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                    if (impactOfNextEvent >= self.NEWSIMPACT): 
                        News = True
            
            # Check the Calendar Event of BASE SYMBOL
            if (News == False):
                if (self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    # get minutesSincePrevEvent
                    previous_event_minute = self.get_previous_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT])
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    [next_event_minute, next_event_minute_index] = self.get_next_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT]) 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                         or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
                else:
                    # get minutesSincePrevEvent
                    if (self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        previous_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
                        time = int(previous_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        previous_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        previous_event_minute = DEFAULT_NUMBER_INT
                        
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    if (self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        next_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        time = int(next_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        next_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        next_event_minute = DEFAULT_NUMBER_INT
                    
                    next_event_minute_index = DEFAULT_NUMBER_INT 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if ((minutesUntilNextEvent <= self.MINSBEFORENEWS 
                         or minutesSincePrevEvent <= self.MINSAFTERNEWS) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
             
            # Check the Calendar Event of QUOTE SYMBOL
            if (News == False):
                if (self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    # get minutesSincePrevEvent
                    previous_event_minute = self.get_previous_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT])
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    [next_event_minute, next_event_minute_index] = self.get_next_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT]) 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                         or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
                    
                else:
                    # get minutesSincePrevEvent
                    if (self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        previous_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
                        time = int(previous_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        previous_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        previous_event_minute = DEFAULT_NUMBER_INT
                        
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    if (self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        next_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        time = int(next_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        next_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        next_event_minute = DEFAULT_NUMBER_INT
                    
                    next_event_minute_index = DEFAULT_NUMBER_INT 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if ((minutesUntilNextEvent <= self.MINSBEFORENEWS 
                         or minutesSincePrevEvent <= self.MINSAFTERNEWS) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
                        
        return News

    #===============================================================================
    def HoursFilter22_3(self):
        ''' HoursFilter22_3. '''
    
        # get the Hour of local time/system time
        hour0 = self.TimeHour_4()
        
        if (self.NewsTime_4() == False 
            and (((self.Hour_of_trading_from < self.Hour_of_trading_to and hour0 >= self.Hour_of_trading_from and hour0 < self.Hour_of_trading_to) 
                  or (self.Hour_of_trading_from > self.Hour_of_trading_to and (hour0 < self.Hour_of_trading_to or hour0 >= self.Hour_of_trading_from))) and (self.TRADING_24H == False))):
             
            self.Trading = "Trading!"
            if (self.FILTERSPREAD and self.mode_spread > self.SpreadMax):
                # print("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                log.info("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                return
 
            self.CheckLastOrderType33_4()
            self.LimitOpenOrders28_4()
            self.CheckLastOrderType35_4()
        else:
            if (self.TRADING_24H == False) and (self.SellOrderExists == False) and (self.BuyOrderExists == False):
                self.Trading = "Not Trading!"
                self.DeletePendingOrder18_3()
                self.DeletePendingOrder19_3()
            else:
                self.Trading = "Override Hour/Day Filter"
                if  (self.FILTERSPREAD == True and self.mode_spread > self.SpreadMax):
                    # print("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    log.info("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    return
                    
                self.CheckLastOrderType33_4()
                self.LimitOpenOrders28_4()
                self.CheckLastOrderType35_4()
                
        if (self.TRADING_24H == True):
            if (self.Overide == True):
                self.Trading = "Override Hour/Day Filter"
            else:
                self.Trading = "Trading 24h"
                 
                if (self.FILTERSPREAD == True) and (self.mode_spread > self.SpreadMax):
                    # print("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    log.info("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    return
                 
                self.CheckLastOrderType33_4()
                self.LimitOpenOrders28_4()
                self.CheckLastOrderType35_4()
    
    #===============================================================================
    def WeekdayFilter23_2(self):
        ''' WeekdayFilter23_2  '''
            
        # (0 - Monday, 1, 2, 3, 4, 5, 6)
        if ((self.MONDAY and self.DayOfWeek_3() == 0) 
            or (self.TUESDAY and self.DayOfWeek_3() == 1) 
            or (self.WEDNESDAY and self.DayOfWeek_3() == 2) 
            or (self.THURSDAY and self.DayOfWeek_3() == 3) 
            or (self.FRIDAY and self.DayOfWeek_3() == 4) 
            or (self.SATURDAY and self.DayOfWeek_3() == 5) 
            or (self.SUNDAY and self.DayOfWeek_3() == 6)):
            
            self.Overide = False
            self.HoursFilter22_3()
        
        else:
            if (self.SellOrderExists == False) and (self.BuyOrderExists == False):
                self.Trading = "Not Trading!"
                self.DeletePendingOrder18_3()
                self.DeletePendingOrder19_3()
            else:
                self.Overide = True
                self.HoursFilter22_3()
        
    #===============================================================================
    def CloseOrder17_3(self):
        ''' Close OP_BUY and delete OP_BUYLIMIT in Opened and Pending order pool. '''
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # close orders when they are OP_BUY orders
            if  (order_type == OP_BUY):
                # --> Close a specific old_opended_order in data by deleting this OP_BUY in the Opened and Pending orders pool 
                # and return new value of order from Opened position to Close position
                self.OrderClose_4(order, order_id, order_type)
        
        self.DeletePendingOrder18_3()         
        
    #===============================================================================
    def CloseOrder16_3(self):
        ''' Close OP_SELL and delete OP_SELLLIMIT in Opened and Pending order pool. '''
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # close orders when they are OP_SELL orders
            if  (order_type == OP_SELL):
                # --> Close a specific old_opended_order in data by deleting this OP_SELL in the Opened and Pending orders pool 
                # and return new value of order from Opened position to Close position
                self.OrderClose_4(order, order_id, order_type)
                
        self.DeletePendingOrder19_3()   
        
    #===============================================================================
    def CloseOrderIf21_2(self):
        ''' Close all orders in Opened orders pool when satisfied conditions. '''
        
        dblProfit = DEFAULT_NUMBER_FLOAT
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            OrderProfit = float(order[PROFIT_COL_INDEX])
            dblProfit += OrderProfit
        
        if  ((self.PROFIT and dblProfit >= self.PROFIT_ALL_ORDERS) 
             or (dblProfit <= self.AMOUNT_OF_LOSS and self.SET_UP_OF_LOSS == True) 
             or self.CLOSING_OF_ALL_TRADES == True):
        
            for order_id in self.ORDER_OPENED_DICT.keys():
                self.CloseOrder16_3()
                self.CloseOrder17_3()
        
    #===============================================================================
    def AtCertainTime6_2(self):
        ''' Return  '''
    
        # get the Hour of local time/system time
        hour0 = self.TimeHour_4()
        minute0 = self.TimeMinute_3()
        
        if ((self.DayOfWeek_3() != self.Today6 and hour0 > self.Time_of_closing_in_hours and minute0 > self.Time_of_closing_in_minutes) 
            and (self.Time_closing_trades == True) 
            and  self.ProfitCheck_3() > DEFAULT_NUMBER_FLOAT):

            self.Today6 = self.DayOfWeek_3();
            self.CloseOrder17_3();
            self.CloseOrder16_3();
        
    #===============================================================================
    def OnEveryTick24_1(self):
        ''' Actions for every tick  '''
        
        # functions for placing Pending orders
        self.WeekdayFilter23_2()
        self.AtCertainTime6_2()
        
        # TODO: Extra Functions for having Open/Market orders: 
        self.ModifyPendingOrder_2()
        
        # function for closing orders
        self.CloseOrderIf21_2()
                
    #===============================================================================
    def CloseDeleteAll_1(self):
        ''' Close all orders  '''
        
        flag_close_delete_all = True
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # when the order is OP_BUY or OP_SELL
            if  (order_type == OP_BUY or order_type == OP_SELL):
                # --> Close a specific old_opended_order in data by deleting this OP_BUY in the Opened and Pending orders pool 
                # and return new value of order from Opened position to Close position
                flag_close_delete_all = self.OrderClose_4(order, order_id, order_type)
                
                if (flag_close_delete_all == False):
                    return flag_close_delete_all
            
            # when the order is OP_BUYLIMIT or OP_SELLLIMIT
            if  (order_type == OP_BUYLIMIT or order_type == OP_SELLLIMIT):
                
                # --> delete this OP_BUYLIMIT or OP_SELLLIMIT oder in the Opened and Pending orders pool
                flag_close_delete_all = self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)
               
                if (flag_close_delete_all):
                    # --> update date time and save this deleted OP_BUYLIMIT or OP_SELLLIMIT oder in the Deleted orders pool
                    order[DATETIME_COL_INDEX] = self.current_datetime
                    order[DAY_COL_INDEX] = self.current_day
                    order[TIME_COL_INDEX] = self.current_time
                    flag_close_delete_all = self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
            
                    if (flag_close_delete_all == False):
                        return flag_close_delete_all
            
        return flag_close_delete_all
            
    #===============================================================================
    def CheckEnoughMoney_2(self, order):
        ''' Check if there are enough money in the account for open an order by calculating Equity. '''
        
        self.CurrentProfit = self.ProfitCheck_3()
        
        # EQUITY = BALANCE + PROFIT
        equity = self.balance + self.CurrentProfit
            
        # MARGIN = ENTRY PRICE * SIZE /LEVERAGE 
        margin = order[PRICE_ENTRY_COL_INDEX] * order[LOTS_COL_INDEX] * ONE_LOT_VALUE / LEVERAGE
        
        # FREE MARGIN = EQUITY - MARGIN
        free_magin = equity - margin
        
        if (free_magin >= margin):
            return True
        else:
            # print("There are not enough money in account to open order %s" % order[ORDER_ID_COL_INDEX])
            log.info("There are not enough money in account to open order %s" % order[ORDER_ID_COL_INDEX])
            return False
        
    #===============================================================================
    def ModifyPendingOrder_2(self):
        ''' If there are enough money in the account for opening a pending order, this pending order will 
        be modified into a market one (opened). '''
        
        if (self.ords_in_a_day >= self.OPENORDERSLIMITDAY):
#             print("Cannot modify this Pending order due to reaching maximum %s orders per day." % self.OPENORDERSLIMITDAY)
            log.info("Cannot modify this Pending order due to reaching maximum %s orders per day." % self.OPENORDERSLIMITDAY)
        else:
            # get all Opened and Pending orders in the pool
            # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
            for order_id in self.ORDER_OPENED_DICT.keys():
                order = self.ORDER_OPENED_DICT[order_id]
                order_type = order[ORDER_TYPE_COL_INDEX]
                    
                # check if it can be modified to become an Open order or not when this order is OP_BUYLIMIT or OP_BUYLIMIT 
                if  (order_type == OP_BUYLIMIT or order_type == OP_SELLLIMIT):
                    
                    entry_price = order[PRICE_ENTRY_COL_INDEX]
                    exit_price = DEFAULT_NUMBER_FLOAT
                    flag_modified = False
                    message = ""
                    
                    # compare entry price with exit price from next tick
                    if (order_type == OP_BUYLIMIT):
                        exit_price = self.bid_nexttick_price
                        message = "Modified the Pending order OP_BUYLIMIT " + str(order_id) + " to Open order OP_BUY."
                        
                        if (entry_price <= exit_price
                            and exit_price != DEFAULT_NUMBER_FLOAT):
                            flag_modified = True
                        else:
                            flag_modified = False
#                             print("Cannot modify order OP_BUYLIMIT %s due to entry_price <= exit_price." % order_id)
                            log.info("Cannot modify order OP_BUYLIMIT %s due to entry_price <= exit_price." % order_id)
                            
                    # compare entry price with exit price from next tick
                    elif (order_type == OP_SELLLIMIT):
                        exit_price = self.ask_nexttick_price
                        message = "Modified the Pending order OP_SELLLIMIT " + str(order_id) + " to Open order OP_SELL."
                        
                        if (entry_price >= exit_price
                            and exit_price != DEFAULT_NUMBER_FLOAT):
                            flag_modified = True
                        else:
                            flag_modified = False
#                             print("Cannot modify order OP_SELLLIMIT %s due to entry_price >= exit_price." % order_id)
                            log.info("Cannot modify order OP_SELLLIMIT %s due to entry_price >= exit_price." % order_id)
                            
                    # when this Pending order can be modified
                    if (flag_modified):
                        # modified this Pending order to become Open order when having enough money
                        if (self.CheckEnoughMoney_2(order)):  
                            # delete this order in the Opened and Pending orders pool
                            if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                                '''When you go long, you enter the market at the ASK price and exit the market at BID price.
                                When you go short, you enter the market at the BID price and exit at the ASK price.'''
                                # ORDER_OPENED_DICT[] = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
                                
                                # update the new type for this Pending order 
                                new_order_type = order_type
                                if (order_type == OP_BUYLIMIT):
                                    new_order_type = OP_BUY
                                    
                                elif (order_type == OP_SELLLIMIT):
                                    new_order_type = OP_SELL
                                    
                                # calculate the new profit   
                                lots = order[LOTS_COL_INDEX]
                                profit = self.CalculateProfit_5(entry_price, exit_price, lots, new_order_type)
                                self.net_profit = self.net_profit + profit
                                                
                                order[DATETIME_COL_INDEX] = self.current_datetime_nexttick
                                order[DAY_COL_INDEX] = self.current_day_nexttick
                                order[TIME_COL_INDEX] = self.current_time_nexttick
                                order[ORDER_TYPE_COL_INDEX] = new_order_type
                                order[PRICE_ENTRY_COL_INDEX] = entry_price
                                order[PRICE_EXIT_COL_INDEX] = exit_price
                                order[PROFIT_COL_INDEX] = profit
                                if (profit < DEFAULT_NUMBER_FLOAT):
                                    order[TP_COL_INDEX] = DEFAULT_SECOND_NUMBER_FLOAT
                                        
                                # save back this deleted order in the Opened and Pending orders pool with updated values
                                # and update the numbers of Open orders per day
                                if (self.OrderAdd_10(order_id, order, self.ORDER_OPENED_DICT)):
                                    self.ords_in_a_day += DEFAULT_SECOND_NUMBER_INT
#                                     print(message)
                                    log.info(message)
                        else:
#                             print("There are NOT enough money to modify this Pending order %s to Open order." % order_id)
                            log.info("There are NOT enough money to modify this Pending order %s to Open order." % order_id)

    #===============================================================================
    def initilize(self, PARAMETERS_COMPLETED, DIGITS, POINT):
    
        # get the total parameters for running EA
        name_ea_row_index = 0
        magic_row_index = 1
        filterspread_row_index = 2
        spreadmax_row_index = 3
        a_row_index = 4
        monday_row_index = 5
        tuesday_row_index = 6
        wednesday_row_index = 7
        thursday_row_index = 8
        friday_row_index = 9
        saturday_row_index = 10
        sunday_row_index = 11
        b_row_index = 12
        trading_24h_row_index = 13
        gmt_offset_row_index = 14
        hour_of_trading_from_row_index = 15
        hour_of_trading_to_row_index = 16
        use_orderslimit_row_index = 17
        openorderslimitday_row_index = 18
        c_row_index = 19
        time_closing_trades_row_index = 20
        time_of_closing_in_hours_row_index = 21
        time_of_closing_in_minutes_row_index = 22
        d_row_index = 23
        profit_row_index = 24
        profit_all_orders_row_index = 25
        e_row_index = 26
        openorderslimit_row_index = 27
        singleordersl_row_index = 28
        singleordertp_row_index = 29
        f_row_index = 30
        arrangements_of_trades_row_index = 31
        g_row_index = 32
        lots_row_index = 33
        slippage_row_index = 34
        h_row_index = 35
        set_up_of_loss_row_index = 36
        amount_of_loss_row_index = 37
        i_row_index = 38
        closing_of_all_trades_row_index = 39
        j_row_index = 40
        usenewsfilter_row_index = 41
        minsbeforenews_row_index = 42
        minsafternews_row_index = 43
        newsimpact_row_index = 44
        k_row_index = 45
        filtering_row_index = 46
        l_row_index = 47
        autoequitymanager_row_index = 48
        equitygainpercent_row_index = 49
        safeequitystopout_row_index = 50
        safeequityrisk_row_index = 51
        
        self.NAME_EA = str(PARAMETERS_COMPLETED[name_ea_row_index]
                           [VALUE_COL_INDEX])
        self.MAGIC = int(PARAMETERS_COMPLETED[magic_row_index]
                         [VALUE_COL_INDEX])
        self.FILTERSPREAD = bool(str(PARAMETERS_COMPLETED[filterspread_row_index]
                                     [VALUE_COL_INDEX]).title())
        self.SPREADMAX = float(PARAMETERS_COMPLETED[spreadmax_row_index]
                               [VALUE_COL_INDEX])
        self.A = str(PARAMETERS_COMPLETED[a_row_index]
                     [VALUE_COL_INDEX])
        self.MONDAY = bool(str(PARAMETERS_COMPLETED[monday_row_index]
                               [VALUE_COL_INDEX]).title())
        self.TUESDAY = bool(str(PARAMETERS_COMPLETED[tuesday_row_index]
                                [VALUE_COL_INDEX]).title())
        self.WEDNESDAY = bool(str(PARAMETERS_COMPLETED[wednesday_row_index]
                                  [VALUE_COL_INDEX]).title())
        self.THURSDAY = bool(str(PARAMETERS_COMPLETED[thursday_row_index]
                                 [VALUE_COL_INDEX]).title())
        self.FRIDAY = bool(str(PARAMETERS_COMPLETED[friday_row_index]
                               [VALUE_COL_INDEX]).title())
        self.SATURDAY = bool(str(PARAMETERS_COMPLETED[saturday_row_index]
                                 [VALUE_COL_INDEX]).title())
        self.SUNDAY = bool(str(PARAMETERS_COMPLETED[sunday_row_index]
                               [VALUE_COL_INDEX]).title())
        self.B = str(PARAMETERS_COMPLETED[b_row_index]
                     [VALUE_COL_INDEX])
        self.TRADING_24H = bool(str(PARAMETERS_COMPLETED[trading_24h_row_index]
                                    [VALUE_COL_INDEX]).title())
        self.GMT_OFFSET = int(PARAMETERS_COMPLETED[gmt_offset_row_index][VALUE_COL_INDEX])
        self.HOUR_OF_TRADING_FROM = int(PARAMETERS_COMPLETED[hour_of_trading_from_row_index]
                                        [VALUE_COL_INDEX])
        self.HOUR_OF_TRADING_TO = int(PARAMETERS_COMPLETED[hour_of_trading_to_row_index]
                                      [VALUE_COL_INDEX])
        self.USE_ORDERSLIMIT = bool(str(PARAMETERS_COMPLETED[use_orderslimit_row_index]
                                        [VALUE_COL_INDEX]).title())
        self.OPENORDERSLIMITDAY = int(PARAMETERS_COMPLETED[openorderslimitday_row_index]
                                      [VALUE_COL_INDEX])
        self.C = str(PARAMETERS_COMPLETED[c_row_index]
                     [VALUE_COL_INDEX])
        self.TIME_CLOSING_TRADES = bool(str(PARAMETERS_COMPLETED[time_closing_trades_row_index]
                                            [VALUE_COL_INDEX]).title())
        self.TIME_OF_CLOSING_IN_HOURS = int(PARAMETERS_COMPLETED[time_of_closing_in_hours_row_index]
                                            [VALUE_COL_INDEX])
        self.TIME_OF_CLOSING_IN_MINUTES = int(PARAMETERS_COMPLETED[time_of_closing_in_minutes_row_index]
                                              [VALUE_COL_INDEX])
        self.D = str(PARAMETERS_COMPLETED[d_row_index]
                     [VALUE_COL_INDEX])
        self.PROFIT = bool(str(PARAMETERS_COMPLETED[profit_row_index]
                               [VALUE_COL_INDEX]).title())
        self.PROFIT_ALL_ORDERS = float(PARAMETERS_COMPLETED[profit_all_orders_row_index]
                                       [VALUE_COL_INDEX])
        self.E = str(PARAMETERS_COMPLETED[e_row_index]
                     [VALUE_COL_INDEX])
        self.OPENORDERSLIMIT = int(PARAMETERS_COMPLETED[openorderslimit_row_index]
                                   [VALUE_COL_INDEX])
        self.SINGLEORDERSL = float(PARAMETERS_COMPLETED[singleordersl_row_index]
                                   [VALUE_COL_INDEX])
        self.SINGLEORDERTP = float(PARAMETERS_COMPLETED[singleordertp_row_index]
                                   [VALUE_COL_INDEX])
        self.F = str(PARAMETERS_COMPLETED[f_row_index]
                     [VALUE_COL_INDEX])
        self.ARRANGEMENTS_OF_TRADES = float(PARAMETERS_COMPLETED[arrangements_of_trades_row_index]
                                            [VALUE_COL_INDEX])
        self.G = str(PARAMETERS_COMPLETED[g_row_index]
                     [VALUE_COL_INDEX])
        self.LOTS = float(PARAMETERS_COMPLETED[lots_row_index]
                          [VALUE_COL_INDEX])
        self.SLIPPAGE = float(PARAMETERS_COMPLETED[slippage_row_index]
                              [VALUE_COL_INDEX])
        self.H = str(PARAMETERS_COMPLETED[h_row_index]
                     [VALUE_COL_INDEX])
        self.SET_UP_OF_LOSS = bool(str(PARAMETERS_COMPLETED[set_up_of_loss_row_index]
                                       [VALUE_COL_INDEX]).title())
        self.AMOUNT_OF_LOSS = float(PARAMETERS_COMPLETED[amount_of_loss_row_index]
                                    [VALUE_COL_INDEX])
        self.I = str(PARAMETERS_COMPLETED[i_row_index]
                     [VALUE_COL_INDEX])
        self.CLOSING_OF_ALL_TRADES = bool(str(PARAMETERS_COMPLETED[closing_of_all_trades_row_index]
                                              [VALUE_COL_INDEX]).title())
        self.J = str(PARAMETERS_COMPLETED[j_row_index]
                     [VALUE_COL_INDEX])
        self.USENEWSFILTER = bool(str(PARAMETERS_COMPLETED[usenewsfilter_row_index]
                                      [VALUE_COL_INDEX]).title())
        self.MINSBEFORENEWS = int(PARAMETERS_COMPLETED[minsbeforenews_row_index]
                                  [VALUE_COL_INDEX])
        self.MINSAFTERNEWS = int(PARAMETERS_COMPLETED[minsafternews_row_index]
                                 [VALUE_COL_INDEX])
        self.NEWSIMPACT = float(PARAMETERS_COMPLETED[newsimpact_row_index]
                              [VALUE_COL_INDEX])
        self.K = str(PARAMETERS_COMPLETED[k_row_index]
                     [VALUE_COL_INDEX])
        self.FILTERING = bool(str(PARAMETERS_COMPLETED[filtering_row_index]
                                  [VALUE_COL_INDEX]).title())
        self.L = str(PARAMETERS_COMPLETED[l_row_index]
                     [VALUE_COL_INDEX])
        self.AUTOEQUITYMANAGER = bool(str(PARAMETERS_COMPLETED[autoequitymanager_row_index]
                                          [VALUE_COL_INDEX]).title())
        self.EQUITYGAINPERCENT = float(PARAMETERS_COMPLETED[equitygainpercent_row_index]
                                       [VALUE_COL_INDEX])
        self.SAFEEQUITYSTOPOUT = bool(str(PARAMETERS_COMPLETED[safeequitystopout_row_index]
                                          [VALUE_COL_INDEX]).title())
        self.SAFEEQUITYRISK = float(PARAMETERS_COMPLETED[safeequityrisk_row_index]
                                    [VALUE_COL_INDEX])
        
        # set up all other parameters
        self.SpreadMax = self.SPREADMAX
        self.Hour_of_trading_from = self.HOUR_OF_TRADING_FROM
        self.Hour_of_trading_to = self.HOUR_OF_TRADING_TO
        self.Time_of_closing_in_hours = self.TIME_OF_CLOSING_IN_HOURS
        self.Time_of_closing_in_minutes = self.TIME_OF_CLOSING_IN_MINUTES
        self.Time_closing_trades = self.TIME_CLOSING_TRADES
        self.Lots = self.LOTS
        self.Slippage = self.SLIPPAGE
        self.NDigits = DIGITS
        self.my_point = POINT
        
        # Adjust for 4/5 digit brokers
        if self.BrokerIs5Digit_0(): 
            self.PipValue = float(10)
            self.my_point *= float(10)
            self.SpreadMax *= float(10)
        
        # Adjust the time following local time
        self.Hour_of_trading_from += self.GMT_OFFSET
        if(self.Hour_of_trading_from >= HOURS_OF_ADAY):
            self.Hour_of_trading_from -= HOURS_OF_ADAY
        if(self.Hour_of_trading_from < DEFAULT_NUMBER_INT):
            self.Hour_of_trading_from += HOURS_OF_ADAY 
                
        self.Hour_of_trading_to += self.GMT_OFFSET
        if(self.Hour_of_trading_to >= HOURS_OF_ADAY):
            self.Hour_of_trading_to -= HOURS_OF_ADAY
        if(self.Hour_of_trading_to < DEFAULT_NUMBER_INT):
            self.Hour_of_trading_to += HOURS_OF_ADAY 
        
        self.Time_of_closing_in_hours += self.GMT_OFFSET
        if(self.Time_of_closing_in_hours >= HOURS_OF_ADAY):
            self.Time_of_closing_in_hours -= HOURS_OF_ADAY
        if(self.Time_of_closing_in_hours < DEFAULT_NUMBER_INT):
            self.Time_of_closing_in_hours += HOURS_OF_ADAY

    #===============================================================================
    def get_event_in_a_day(self, current_day, list_data):
        ''' Get all events happen in a specific day '''
        
        event_in_current_day = []
        event_in_next_day = []
        event_in_previous_day = []
        flag_event = False

        for event_index in range(len(list_data)):
            day = float(list_data[event_index][DAY_COL_INDEX])

            # get all event in the same day            
            if (day == current_day):
                event_in_current_day.append(list_data[event_index])
                flag_event = True 
            # when there is no same day
            else:
                if (flag_event):
                    break
                else:
                    if (day > current_day):
                        next_day_index = event_index
                        previous_day_index = event_index - DEFAULT_SECOND_NUMBER_INT
                        
                        # get all events of the next available day
                        current_day = day
                        while (day == current_day and next_day_index < len(list_data)):
                            event_in_next_day.append(list_data[next_day_index])
                            next_day_index += DEFAULT_SECOND_NUMBER_INT
                            day = float(list_data[next_day_index][DAY_COL_INDEX])
                            
                        # get all events of the previous available day
                        day = float(list_data[previous_day_index][DAY_COL_INDEX])
                        current_day = day
                        while (day == current_day and previous_day_index > DEFAULT_NUMBER_INT):
                            event_in_previous_day.append(list_data[previous_day_index])
                            previous_day_index -= DEFAULT_SECOND_NUMBER_INT
                            day = float(list_data[previous_day_index][DAY_COL_INDEX])
                            
                        break
                    else:
                        pass
                    
        return [event_in_current_day, event_in_next_day, event_in_previous_day]
    
    #===============================================================================
    def analised_tick_data(self, PARAMETERS_DATA, folder_output, file_):
        
        # get the file name
        file_name = convert_backflash2forwardflash(file_)
        file_basename = str(os.path.basename(file_))
        
        ''' For EA running by itself 
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==> Loading TICK DATA from file: {0}...".format(file_basename))
        print("{0} ==> Loading TICK DATA from file: {1}...".format(time_stamp, file_basename))
        '''
        
        # Create TICK_DATA from the Modified CSV file
        TICK_DATA = load_csv2array(file_name)
        DIGITS = digit_of_symbol(float(TICK_DATA[DEFAULT_NUMBER_INT][BID_COL_INDEX]))
        POINT = point_of_symbol(float(TICK_DATA[DEFAULT_NUMBER_INT][BID_COL_INDEX]))
        
        # set up all the total parameters for running EA
        self.reset()
        self.initilize(PARAMETERS_DATA, DIGITS, POINT)
        
        fprevious_day = float(TICK_DATA[DEFAULT_NUMBER_INT][DAY_COL_INDEX])
        self.yesterday_close = float(TICK_DATA[DEFAULT_NUMBER_INT][BID_COL_INDEX])
        
        # get all events of the CALENDAR_DATA
        self.EVENTS_OF_CALENDAR_ALL_SYMBOLS = self.get_event_in_a_day(fprevious_day, CALENDAR_ALL_SYMBOLS_DATA)
        self.EVENTS_OF_CALENDAR_BASE_SYMBOLS = self.get_event_in_a_day(fprevious_day, CALENDAR_BASE_SYMBOL_DATA)
        self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS = self.get_event_in_a_day(fprevious_day, CALENDAR_QUOTE_SYMBOL_DATA)
        
        current_tick = DEFAULT_NUMBER_INT
        next_tick = DEFAULT_NUMBER_INT
        while (current_tick < len(TICK_DATA) - DEFAULT_SECOND_NUMBER_INT):
            
            ''' For EA running by itself 
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            if (current_tick == DEFAULT_NUMBER_INT):
                log.info("... ==> start processing the data...")
                print("%s... ==> start processing the data..." % time_stamp)
            '''
            
            # get the values from the current tick
            self.current_datetime = float(TICK_DATA[current_tick][DATETIME_COL_INDEX])
            self.current_day = float(TICK_DATA[current_tick][DAY_COL_INDEX])
            self.current_time = float(TICK_DATA[current_tick][TIME_COL_INDEX])
            self.bid_price = float(TICK_DATA[current_tick][BID_COL_INDEX])
            self.ask_price = float(TICK_DATA[current_tick][ASK_COL_INDEX])
            
            self.mode_spread = self.MODE_SPREAD_1(self.bid_price, self.ask_price)

            # save the previous date when going to a new date 
            if (fprevious_day != self.current_day):
                
                ''' For EA running by itself 
                time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
                log.info("==> current_tick: %s" % current_tick)
                log.info("==> checking date %s" % self.current_datetime)
                print("{0} ==> current_tick: {1}".format(time_stamp, current_tick))
                print("{0} ==> checking date {1}".format(time_stamp, self.current_datetime))
                 
                run_percentage = round((float(current_tick) / float(len(TICK_DATA))) * float(100), 2)
                 
#                 log.info("==> current_tick: %s" % current_tick)
                log.info("... ==> processing {0}% of the data, date {1}...".format(run_percentage, self.current_datetime))
                time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#                 print("{0} ==> current_tick: {1}".format(time_stamp, current_tick))
                print("{0}... ==> processing {1}% of the data...".format(time_stamp, run_percentage, self.current_datetime))
                '''
                
                # save the old date
                fprevious_day = self.current_day
                self.yesterday_close = float(TICK_DATA[current_tick][BID_COL_INDEX])
                
                # reset the Maximum Open orders per day
                self.ords_in_a_day = DEFAULT_NUMBER_INT
              
            # find the next tick following the input Time Frame
            while next_tick < range(len(TICK_DATA) - current_tick):
                
                # save all rows from current tick to next tick
                self.TIMEFRAME_TICK_DATA.append(TICK_DATA[next_tick])
                
                # get day and time of next tick
                self.current_day_nexttick = float(TICK_DATA[next_tick][DAY_COL_INDEX])
                self.current_time_nexttick = float(TICK_DATA[next_tick][TIME_COL_INDEX])
                
                # get the values from the next tick
                diff_time = (self.current_day_nexttick + self.current_time_nexttick) - (self.current_day + self.current_time) 
                
                if (self.current_day != self.current_day_nexttick):
                    self.current_day_nexttick = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][DAY_COL_INDEX])
                    self.current_time_nexttick = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][TIME_COL_INDEX])
                    self.current_datetime_nexttick = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][DATETIME_COL_INDEX])
                    self.bid_nexttick_price = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][BID_COL_INDEX])
                    self.ask_nexttick_price = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][ASK_COL_INDEX])
            
                    # move to next tick
                    current_tick = next_tick
                    next_tick += DEFAULT_SECOND_NUMBER_INT
                    break
                elif (diff_time >= TIME_FRAME
                    or next_tick == len(TICK_DATA) - DEFAULT_SECOND_NUMBER_INT):
                    
                    self.current_datetime_nexttick = float(TICK_DATA[next_tick][DATETIME_COL_INDEX])
                    self.bid_nexttick_price = float(TICK_DATA[next_tick][BID_COL_INDEX])
                    self.ask_nexttick_price = float(TICK_DATA[next_tick][ASK_COL_INDEX])
            
                    # move to next tick
                    current_tick = next_tick
                    next_tick += DEFAULT_SECOND_NUMBER_INT
                    break
                else:
                    next_tick += DEFAULT_SECOND_NUMBER_INT
            
            # check if reaching maximum orders and delete the pending orders            
            if (self.MaxOrders_9(self.OPENORDERSLIMITDAY)):
                continue
            else:
                if (self.clear):                       
                    if (self.CloseDeleteAll_1()):
                        self.clear = False
                    else:
                        return
                            
                # check total profit at the moment
                self.CurrentProfit = self.ProfitCheck_3()
                
                # check total balance at the moment
                self.balance = self.AccountBalance_1()  # uzavrete obchody
                    
                # --> SAFEEQUITYSTOPOUT and AUTOEQUITYMANAGER
                if (self.SAFEEQUITYSTOPOUT 
                    and (self.SAFEEQUITYRISK / float(100)) * self.balance < self.CurrentProfit * float(-1) 
                    and self.CloseDeleteAll_1() == False):
                            self.clear = True
                            return 
                
                if (self.AUTOEQUITYMANAGER 
                    and (self.EQUITYGAINPERCENT / float(100)) * self.balance < self.CurrentProfit 
                    and self.CloseDeleteAll_1() == False):
                            self.clear = True
                            return
               
                # Original Function from original EA
                self.OnEveryTick24_1()
        
        ''' For EA running by itself 
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Completed running tick data file: {0} with profit {1}!".format(file_basename, self.net_profit))
        print("{0} ==>  Completed running tick data file: {1} with profit {2}!".format(time_stamp, file_basename, self.net_profit))
        ''' 
                              
        # Write out other data for reference
        file_basename = file_basename.split('.')[DEFAULT_NUMBER_INT]
        write_value_of_dict2csv_no_header(self.ORDER_CLOSED_DICT, folder_output + file_basename + '_' + FILENAME_ORDER_CLOSED_HISTORY)
        write_value_of_dict2csv_no_header(self.ORDER_DELETED_DICT, folder_output + file_basename + '_' + FILENAME_ORDER_DELETED_HISTORY)
                
        return self.net_profit

    #===============================================================================
    def ea_run_testing(self):
        ''' Randomly create values of NetProfit for testing only '''
    
        return (random.random() * NET_PROFIT)
        
    #===============================================================================
    def ea_run(self, PARAMETERS_DATA, individual_ID, RUN_FREQUENCY_BY_YEAR):
        ''' EA running '''
        
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Start calculating fitness for individual {0} for {1} year(s)!".format(individual_ID, RUN_FREQUENCY_BY_YEAR))
        print("{0} ==>  Start calculating fitness for individual {1} for {2} year(s)!".format(time_stamp, individual_ID, RUN_FREQUENCY_BY_YEAR))
            
        total_profit = DEFAULT_NUMBER_FLOAT 
#         self.PARAMETERS_DATA = copy_string_array(PARAMETERS_DATA)
        
        # Create an folder for storing all outputs in this section 
        symbol_folder_output = FOLDER_DATA_OUTPUT + SYMBOL
        if os.path.exists(symbol_folder_output) == False:
            os.makedirs(symbol_folder_output)
        
        folder_output = symbol_folder_output + '/ind_' + str(individual_ID) + '_outputs/'
        if os.path.exists(folder_output):
            shutil.rmtree(folder_output)
        os.makedirs(folder_output)
        
        # Access the input folder to get the Tick Data
        folder_name = convert_backflash2forwardflash(FOLDER_DATA_INPUT + SYMBOL + FOLDER_TICK_DATA_MODIFIED)
        allFiles = glob.glob(folder_name + '/*.csv')
        
        # create a list of files to analyze based on RUN_FREQUENCY_BY_YEAR
        allFile_w_frequency = []
        total_analyzed_files = int(RUN_FREQUENCY_BY_YEAR) * MONTHS_OF_A_YEAR
        
        # identify where to get all the file for analysis
        if(len(allFiles) > total_analyzed_files):
            file_count = len(allFiles) - total_analyzed_files
        else:
            file_count = DEFAULT_NUMBER_INT
            
        while (file_count < len(allFiles)):
            allFile_w_frequency.append(allFiles[file_count])
            file_count += DEFAULT_SECOND_NUMBER_INT
        
        ''' SINGLETHREADING 
        for file_ in allFiles:
            total_profit += HappyForexEA().analised_tick_data(PARAMETERS_DATA, folder_output, file_,)
        '''
        
        ''' MULTITHREADING '''
        # make the Pool of workers
        pool_size = multiprocessing.cpu_count()
        
        ''' For EA running by itself 
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Pool size of ThreadPool: {0}!".format(pool_size))
        print("{0} ==>  Pool size of ThreadPool: {1}!".format(time_stamp, pool_size))
        ''' 
        
        ''' ANOTHER MULTITHREADING METHOD 
        results = ea_pool.map(self.analised_tick_data, allFiles)
        ea_pool.close() 
        ea_pool.join()
         
        for profit_ in results:
            total_profit += float(profit_)
        '''
        
        ea_pool = ThreadPool(pool_size)
        
        # Running EA process
        results = [ea_pool.apply_async(HappyForexEA().analised_tick_data, (PARAMETERS_DATA, folder_output, file_,))
                   for file_ in allFile_w_frequency]
         
        # --> proxy.get() waits for task completion and returns the result
        profits = [r.get() for r in results]  
         
        # close the pool and wait for the work to finish 
        ea_pool.close() 
        
        # get the total profit after running all the Tick data
        for profit_ in profits:
            total_profit += float(profit_)
            
        # write out other data for reference
        file_name_out = symbol_folder_output + '/' + SYMBOL + '_ind_' + str(individual_ID) + '_$' + str(round(total_profit, 2)) + '_' + FILENAME_ORDER_CLOSED_HISTORY
        combine_all_files_in_a_folder(folder_output, file_name_out,
                                      '*_' + FILENAME_ORDER_CLOSED_HISTORY)
        
        # convert back the Date Time for output file
        converted_data = convert_datetime_back_whole_list(file_name_out)
        
        # create a new file name
        write_array2csv_with_delimiter_no_header(converted_data, file_name_out, ',')
    
        # delete output folder after writing out the order history 
        if os.path.exists(folder_output):
            shutil.rmtree(folder_output)
            
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Completed calculating fitness for individual {0} with profit {1}!".format(individual_ID, round(total_profit, 2)))
        print("{0} ==>  Completed calculating fitness for individual {1} with profit {2}!".format(time_stamp, individual_ID, round(total_profit, 2)))
            
        return total_profit


################################################################################
##########################           CLASS           ###########################
################################################################################
class Individual(object):
    '''
    classdocs
    '''
    
    #===============================================================================
    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        
        # default attributes
        self.net_profit = DEFAULT_NUMBER_INT
        self.total_win = DEFAULT_NUMBER_INT
        self.fitness = DEFAULT_NUMBER_INT
        self.individual_ID = str(DEFAULT_NUMBER_INT)
       
        # copy optimize-needed and default parameters for each individual to become its genes
        self.genes = copy_string_array(OPTIMIZED_PARAMETERS_DATA)
        self.genes_completed = copy_string_array(DEFAULT_PARAMETERS_DATA)
        
        # create dictionaries for storing orders pools 
        self.ORDER_CLOSED_DICT = {} 
        self.ORDER_OPENED_DICT = {} 
        self.ORDER_DELETED_DICT = {}
        
    #===============================================================================
    def create_a_set_of_genes(self):
        # reset genes for each individual
        row = DEFAULT_NUMBER_INT
        col = 1
        
        # --> FilterSpread ==> pickup value 1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT, sys.maxint) % 2  
        row += 1
        # --> Friday ==> pickup value  1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT, sys.maxint) % 2  
        row += 1
        # --> OpenOrdersLimitDay ==> pickup value 1 to 3
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT + 1, int(self.genes[row][col]))  
        row += 1
        # --> Time_closing_trades ==> pickup value 1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT, sys.maxint) % 2  
        # --> only change value of Time_of_closing_in_hours ==> pickup value 5 or 6 when Time_closing_trades==True
        if self.genes[row][col] == '1':
            row += 1
            self.genes[row][col] = random.randint(int(self.genes[row][col]), int(self.genes[row][col]) + 1) 
        else:
            row += 2
        # --> Profit_all_orders ==> pickup value 1 to 12 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT + 1, int(self.genes[row][col]))  
        row += 1
        # --> Arrangements_of_trades ==> pickup value 1 or 25
        random_num = random.randint(DEFAULT_NUMBER_INT + 1, abs(int(self.genes[row][col])))
        self.genes[row][col] = random_num * (-1)  
        row += 1
        # --> Lots ==> pickup value 0.01 to 0.1
        random_num = random.uniform(float(self.genes[row][col]), MAX_LOTS)
        self.genes[row][col] = round(random_num, 2)  
        
        # create the whole completed parameters for running EA
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
    
    #===============================================================================

    '''
    manual_parameters_list = ['FilterSpread', 'Friday', 'OpenOrdersLimitDay', 'Time_closing_trades', 'Time_of_closing_in_hours',
                       'Profit_all_orders', 'Arrangements_of_trades', 'Lots']
    '''

    def create_a_fixed_set_genes(self, manual_parameters_list):
        # reset genes randomly for each individual
        row = DEFAULT_NUMBER_INT
        col = 1
        
        # --> FilterSpread
        self.genes[row][col] = manual_parameters_list[row] 
        row += 1
        # --> Friday
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> OpenOrdersLimitDay
        self.genes[row][col] = manual_parameters_list[row]   
        row += 1
        # --> Time_closing_trades
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> Time_of_closing_in_hours
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> Profit_all_orders
        self.genes[row][col] = manual_parameters_list[row]   
        row += 1
        # --> Arrangements_of_trades
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> Lots
        self.genes[row][col] = manual_parameters_list[row]   
    
        # create the whole completed parameters for running EA
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
    
    #===============================================================================
    def create_ind_uniqueID(self, dictionary_IDlist):

        # create the individual's ID which is the combination of all Values of parameters
        col_index_value = 1
        new_id = '_' . join([str(row[col_index_value]) for row in self.genes])
        
        # keep create an individual while the ID is not unique
        while (new_id in dictionary_IDlist == True):
            self.create_a_set_of_genes()
            new_id = '_' . join([str(row[col_index_value]) for row in self.genes])
        
        # assign the new ID to an individual
        self.individual_ID = new_id
           
        return new_id
    
    #===============================================================================
    def flip_value(self, mutation_point):
        
        key_col_index = DEFAULT_NUMBER_INT
         
        # Flip values at the mutation point
        # --> FilterSpread=true (default) ==> 1/0
        if self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_SECOND_NUMBER_INT):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
         
        # --> Friday=true (default) ==> 1/0
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_SECOND_NUMBER_INT):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_SECOND_NUMBER_INT)
         
        # --> OpenOrdersLimitDay ==> 1 to 3
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(DEFAULT_NUMBER_INT + 1,
                                                                             int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
        
        # --> Time_closing_trades=false ==> 1/0
        # Check the special variable of Time_of_closing_in_hours 
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_NUMBER_INT):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_SECOND_NUMBER_INT)
                
                # --> only change value of Time_of_closing_in_hours ==> pickup value 5 or 6 when Time_closing_trades==True/1
                self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(5, 6) 
                
                if self.genes[mutation_point + 1][VALUE_COL_INDEX] == '5':
                    self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(int(self.genes[mutation_point + 1][VALUE_COL_INDEX]),
                                                                                     int(self.genes[mutation_point + 1][VALUE_COL_INDEX]) + 1) 
                elif self.genes[mutation_point + 1][VALUE_COL_INDEX] == '6':
                    self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(int(self.genes[mutation_point + 1][VALUE_COL_INDEX] - 1),
                                                                                     int(self.genes[mutation_point + 1][VALUE_COL_INDEX]))
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
    
        # --> Profit_all_orders ==> 1 to 12
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(DEFAULT_NUMBER_INT + 1,
                                                                             int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
        
        # --> Arrangements_of_trades ==> 1 to 25
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) + 1,
                                                                             DEFAULT_NUMBER_INT - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
    
        # --> Lots ==> 0.01 to 0.1
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.uniform(float(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) * 2,
                                                                             MAX_LOTS)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
    
        # create the whole completed parameters for running EA
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
    
        
################################################################################
##########################           CLASS           ###########################
################################################################################
class Population(object):
    '''
    classdocs
    '''

    #===============================================================================
    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        
        # TODO: For testing only
        self.popSize = 5
         
        # TODO: UNCOMMENT when finishing testing
#         # reduce 1 for size of permutation due to the condition True/False of Time_closing_trades
#         letters = digits = len(OPTIMIZE_PARAMETERS_LIST) - 1  
#         self.popSize = permutation_count(letters, digits)

        self.fittest = DEFAULT_NUMBER_INT
        self.individuals = [Individual()] * self.popSize
        self.individuals_ID_dict = {}  # a dictionary (as a hash-map) for storing ID
        self.FITNESS_DICT = {}  # a dictionary for storing fitness of all individuals
 
        # create an instance of EA for running 
        self.happyforex_EA_instance = HappyForexEA()
        
    #===============================================================================
    # Initialize population
    def initialize_population(self):
        for i in range(self.popSize):
            # create the individual with its attributes
            an_individual = Individual()
            an_individual.create_a_set_of_genes()
            new_id = an_individual.create_ind_uniqueID(self.individuals_ID_dict)

            # assign the individual with unique ID into population
            self.individuals[i] = an_individual
            self.individuals_ID_dict[new_id] = i 
            
#             # add the genes completed to the pool
#             self.all_genes_pool[an_individual.genes_completed] = i
            
    #===============================================================================
    # Get the highest fitness individual
    def get_fittest(self):
        max_fit = -sys.maxint - 1
        max_fit_index = DEFAULT_NUMBER_INT
        
        for i in range(len(self.individuals)):
            if max_fit <= self.individuals[i].fitness:
                max_fit_index = i
                max_fit = self.individuals[i].fitness
        
        self.fittest = max_fit
        
        highest_fitness_ind = Individual()
        highest_fitness_ind.individual_ID = self.individuals[max_fit_index].individual_ID
        highest_fitness_ind.net_profit = self.individuals[max_fit_index].net_profit
        highest_fitness_ind.total_win = self.individuals[max_fit_index].total_win
        highest_fitness_ind.fitness = self.individuals[max_fit_index].fitness
        highest_fitness_ind.genes = copy_string_array(self.individuals[max_fit_index].genes)
        highest_fitness_ind.genes_completed = copy_string_array(self.individuals[max_fit_index].genes_completed)
        
        return highest_fitness_ind     
        
    #===============================================================================
    # Get the second most highest fitness individual
    def get_second_fittest(self):
        max_fit_1 = max_fit_2 = DEFAULT_NUMBER_INT
        
        for i in range(len(self.individuals)):
            if self.individuals[i].fitness > self.individuals[max_fit_1].fitness:
                max_fit_2 = max_fit_1
                max_fit_1 = i
            elif self.individuals[i].fitness > self.individuals[max_fit_2].fitness:
                max_fit_2 = i
        
        highest_second_fitness_ind = Individual()
        highest_second_fitness_ind.individual_ID = self.individuals[max_fit_2].individual_ID
        highest_second_fitness_ind.net_profit = self.individuals[max_fit_2].net_profit
        highest_second_fitness_ind.total_win = self.individuals[max_fit_2].total_win
        highest_second_fitness_ind.fitness = self.individuals[max_fit_2].fitness
        highest_second_fitness_ind.genes = copy_string_array(self.individuals[max_fit_2].genes)
        highest_second_fitness_ind.genes_completed = copy_string_array(self.individuals[max_fit_2].genes_completed)
        
        return highest_second_fitness_ind 
    
    #===============================================================================
    # Get index of the least fitness individual
    def get_least_fittest(self):
        min_fitness = sys.maxint
        min_fitness_index = DEFAULT_NUMBER_INT
        
        for i in range(len(self.individuals)):
            if min_fitness >= self.individuals[i].fitness:
                min_fitness = self.individuals[i].fitness
                min_fitness_index = i
        
        return min_fitness_index
    
    #===============================================================================
    # Calculate the fitness of each individual
    def cal_fitness(self, ind_, RUN_FREQUENCY_BY_YEAR):
        
        ind_.fitness = DEFAULT_NUMBER_INT
        
        # run the EA logic to return the profit
        ind_.net_profit = self.happyforex_EA_instance.ea_run(ind_.genes_completed, ind_.individual_ID, RUN_FREQUENCY_BY_YEAR)
#         ind_.net_profit = self.happyforex_EA_instance.ea_run_testing()
        ind_.ORDER_CLOSED_DICT = self.happyforex_EA_instance.ORDER_CLOSED_DICT
        ind_.ORDER_OPENED_DICT = self.happyforex_EA_instance.ORDER_OPENED_DICT
        ind_.ORDER_DELETED_DICT = self.happyforex_EA_instance.ORDER_DELETED_DICT
        
        # save profit to dictionary
        self.FITNESS_DICT[str(ind_.individual_ID) + '_origin'] = round(ind_.net_profit, 2)
        
        # calculate fitness for the HappyForex EA
        if ind_.net_profit > NET_PROFIT:
            ind_.fitness = MAX_FITNESS
        else:
            if ind_.net_profit <= DEFAULT_NUMBER_FLOAT:
                ind_.fitness = DEFAULT_NUMBER_FLOAT
            else:
                ind_.fitness = round(100 * ind_.net_profit / NET_PROFIT, 2)
            
        return ind_
            
    #===============================================================================
    # Calculate the fitness of each individual
    def calculate_fittest(self, RUN_FREQUENCY_BY_YEAR):
        
        ''' MONOTHREADING
        for ind_ in self.individuals:
            ind_ = self.cal_fitness(ind_)
        MONOTHREADING '''

        ''' MULTITHREADING '''
        # make the Pool of workers
        pool_size = multiprocessing.cpu_count()
        ea_pool = ThreadPool(pool_size)
        
        # and return the all_fitness_results
#         individuals_w_fitness = ea_pool.map(self.cal_fitness, self.individuals)
        results = [ea_pool.apply_async(self.cal_fitness, (ind_, RUN_FREQUENCY_BY_YEAR,)) for ind_ in self.individuals]
         
        # --> proxy.get() waits for task completion and returns the result
        individuals_w_fitness = [r.get() for r in results]  
        self.individuals = individuals_w_fitness
         
        # close the pool and wait for the work to finish 
        ea_pool.close() 
#         ea_pool.join() 
        ''' MULTITHREADING '''

        
################################################################################
##########################           CLASS           ###########################
################################################################################
class HappyForexGenericAlgorithm(object):
    '''
    classdocs
    '''
 
    #===============================================================================
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.generationCount = DEFAULT_NUMBER_INT
        self.population = Population()
        self.fittest_ind = Individual()
        self.second_fittest_ind = Individual()
        self.least_fittest_ind = Individual()
        self.added_offstring_ind = Individual()
        
    #===============================================================================
    # Selection
    def selection(self):
        # Select the most highest fitness individual 
        self.fittest_ind = self.population.get_fittest()
        
        # Select the second most highest fitness individual
        self.second_fittest_ind = self.population.get_second_fittest()
        
    #===============================================================================
    # Crossover
    def crossover(self):
        # Select a crossover point, from 0 to 6 (make sure less than the length of OPTIMIZE_PARAMETERS_LIST)
        cross_over_point = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 2);
        print("cross_over_point: %s" % cross_over_point)
        log.info("cross_over_point: %s" % cross_over_point)
        
        # Swap values among parents
        i = DEFAULT_NUMBER_INT
        while i <= cross_over_point:
            temp = self.fittest_ind.genes[i]
            self.fittest_ind.genes[i] = self.second_fittest_ind.genes[i]
            self.second_fittest_ind.genes[i] = temp
            i += 1
        
        # Check the special variable of Time_of_closing_in_hours 
        # --> only change value of Time_of_closing_in_hours ==> pickup value 5 or 6 when Time_closing_trades==True/1
        row_time_closing_index = 3
        row_time_of_closing_inhour_index = 4
        
        # In father's genes
        if self.fittest_ind.genes[row_time_closing_index][VALUE_COL_INDEX] == '1':
            if self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '5': 
                self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]),
                                                                                                     int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]) + 1) 
            elif self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '6':
                self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] - 1),
                                                                                                       int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]))
        # In mother's genes
        if self.second_fittest_ind.genes[row_time_closing_index][VALUE_COL_INDEX] == '1':
            if self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '5':
                self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]),
                                                                                                       int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]) + 1) 
            elif self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '6':
                self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] - 1),
                                                                                                    int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]))

        # update individual ID
        new_id_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.fittest_ind.genes])
        self.fittest_ind.individual_ID = new_id_fittest
        
        new_id_second_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.second_fittest_ind.genes])
        self.second_fittest_ind.individual_ID = new_id_second_fittest
        
        # create the whole completed parameters for running EA
        self.fittest_ind.genes_completed = merge_2parametes_array_data(self.fittest_ind.genes_completed, self.fittest_ind.genes)
        self.second_fittest_ind.genes_completed = merge_2parametes_array_data(self.second_fittest_ind.genes_completed, self.second_fittest_ind.genes)

    #===============================================================================
    # Mutation
    def mutation(self):
        row_Time_of_closing_in_hours = 4
        
        # Select a mutation point for fittest_ind  from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
        mutation_point_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
        
        # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
        if mutation_point_fittest == row_Time_of_closing_in_hours:
            mutation_point_fittest -= 1
        print("mutation_point_fittest: %s" % mutation_point_fittest) 
        log.info("mutation_point_fittest: %s" % mutation_point_fittest) 
        
        # Flip values at the mutation point
        self.fittest_ind.flip_value(mutation_point_fittest)
        
        # create the individual's ID which is the combination of all Values of parameters
        id_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.fittest_ind.genes])
        
        # keep create an individual while the ID is not unique
        while (id_fittest in self.population.individuals_ID_dict == True):
            # Select a mutation point from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
            mutation_point_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
            
            # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
            if mutation_point_fittest == row_Time_of_closing_in_hours:
                mutation_point_fittest -= 1
            print("mutation_point_fittest in loops: %s" % mutation_point_fittest) 
            log.info("mutation_point_fittest in loops: %s" % mutation_point_fittest) 
            
            # Flip values at the mutation point
            self.fittest_ind.flip_value(mutation_point_fittest)
            
            id_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.fittest_ind.genes])
        
        # update individual ID
        self.fittest_ind.individual_ID = id_fittest
        
        # Select a mutation point for second_fittest_ind from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
        mutation_point_second_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
        
        # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
        if mutation_point_second_fittest == row_Time_of_closing_in_hours:
            mutation_point_second_fittest -= 1
        print("mutation_point_second_fittest: %s" % mutation_point_second_fittest) 
        log.info("mutation_point_second_fittest: %s" % mutation_point_second_fittest) 
            
        # Flip values at the mutation point
        self.second_fittest_ind.flip_value(mutation_point_second_fittest)
    
        # create the individual's ID which is the combination of all Values of parameters
        id_second_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.second_fittest_ind.genes])
        
        # keep create an individual while the ID is not unique
        while (id_second_fittest in self.population.individuals_ID_dict == True):
            # Select a mutation point from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
            mutation_point_second_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
            
            # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
            if mutation_point_second_fittest == row_Time_of_closing_in_hours:
                mutation_point_second_fittest -= 1
            print("mutation_point_second_fittest in loops: %s" % mutation_point_second_fittest) 
            log.info("mutation_point_second_fittest in loops: %s" % mutation_point_second_fittest) 
            
            # Flip values at the mutation point
            self.second_fittest_ind.flip_value(mutation_point_second_fittest)
            
            id_second_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.second_fittest_ind.genes])
        
        # update individual ID
        self.second_fittest_ind.individual_ID = id_second_fittest
        
    #===============================================================================
    # Get the highest fitness offspring
    def get_fittest_offspring(self):
        if self.fittest_ind.fitness > self.second_fittest_ind.fitness:
            return self.fittest_ind
        
        return self.second_fittest_ind
    
    #===============================================================================
    # Replace least fitness individual from most highest fitness offspring
    def add_fittest_offspring(self):
        # Update fitness values of offspring (after crossover and mutation)
        self.fittest_ind.genes_completed = merge_2parametes_array_data(self.fittest_ind.genes_completed,
                                                                       self.fittest_ind.genes)
        self.second_fittest_ind.genes_completed = merge_2parametes_array_data(self.second_fittest_ind.genes_completed,
                                                                       self.second_fittest_ind.genes)
        
        ''' MONOTHREADING
        # Calculate fitness for these high fitness individuals
        self.fittest_ind = self.population.cal_fitness(self.fittest_ind)
        self.second_fittest_ind = self.population.cal_fitness(self.second_fittest_ind)
        MONOTHREADING ''' 
        
        highest_individuals = [self.fittest_ind, self.second_fittest_ind]
        
        ''' MULTITHREADING '''
        # make the Pool of workers
        pool_size = multiprocessing.cpu_count()
        ea_pool = ThreadPool(pool_size)
        
        # and return the all_fitness_results
        results = [ea_pool.apply_async(self.population.cal_fitness, (ind_,)) for ind_ in highest_individuals]
         
        # --> proxy.get() waits for task completion and returns the result
        individuals_w_fitness = [r.get() for r in results]  
        self.fittest_ind = individuals_w_fitness[DEFAULT_NUMBER_INT]
        self.second_fittest_ind = individuals_w_fitness[DEFAULT_SECOND_NUMBER_INT]
         
        # close the pool and wait for the work to finish 
        ea_pool.close() 
        ''' MULTITHREADING '''
        
        # Get index of least fit individual to retrieve that individual
        least_fittest_index = self.population.get_least_fittest()
        self.least_fittest_ind = self.population.individuals[least_fittest_index]
        
        # Save profit to dictionary
        self.population.FITNESS_DICT[str(self.added_offstring_ind.individual_ID) + '_eliminated'] = round(self.added_offstring_ind.net_profit, 2)
        
        # Retrieve the highest fitness offspring
        self.added_offstring_ind = self.get_fittest_offspring()
       
        # Replace least fitness individual by the highest fitness offspring
        self.population.individuals[least_fittest_index] = self.added_offstring_ind
        
        # Update individuals_ID_dict
        value_least_fittest_ind = self.population.individuals_ID_dict[self.least_fittest_ind.individual_ID]
        del self.population.individuals_ID_dict[self.least_fittest_ind.individual_ID]
        self.population.individuals_ID_dict[self.added_offstring_ind.individual_ID] = value_least_fittest_ind

        # Save profit to dictionary
        self.population.FITNESS_DICT[str(self.added_offstring_ind.individual_ID) + '_added'] = round(self.added_offstring_ind.net_profit, 2)

    #===============================================================================
    def ga_run(self, RUN_FREQUENCY_BY_YEAR):
        # Create an instance for HappyForexGenericAlgorithm to run the program
        happyforexGA = HappyForexGenericAlgorithm()
        
        # Create an folder for storing all outputs in this section 
        folder_output = FOLDER_DATA_OUTPUT + SYMBOL + '_optimization_output/'
        if os.path.exists(folder_output):
            shutil.rmtree(folder_output)
        os.makedirs(folder_output)
        
        # Initialize population
        log.info('#============================== Initialize population ==============================')
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#============================== %s Initialize population ==============================' % time_stamp)
        happyforexGA.population.initialize_population()
        
        log.info('==> population size: %s' % happyforexGA.population.popSize)
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('%s ==> population size: %s' % (time_stamp, happyforexGA.population.popSize))
        
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info('#============================================================')
        log.info('==> first individual genes and genes_completed:')
        print('#============================================================')
        print('%s ==> first individual genes and genes_completed:' % time_stamp)
        display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER_INT].genes_completed, '=')
        log.info('#============================================================')
        print('#============================================================')
        display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER_INT].genes, '=')
        
        # Write the individual_ID_list to a CSV file for reference
        log.info('#============================== Write the individual_ID_list to a CSV file ==============================')
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#============================== %s Write the individual_ID_list to a CSV file ==============================' % time_stamp)
        write_wholedict2csv_no_header(happyforexGA.population.individuals_ID_dict, folder_output + FILENAME_POPULATION_INITIAL)
         
        # Calculate fitness of each individual
        log.info('#============================== Calculate fitness of each individual ==============================')
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#============================== %s Calculate fitness of each individual ==============================' % time_stamp)
        happyforexGA.population.calculate_fittest(RUN_FREQUENCY_BY_YEAR)
    
        # Get the individual with highest fitness ==> retrieve the highest fitness for the population
        log.info('#============================== Get the individual with highest fitness ==============================')
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#============================== %s Get the individual with highest fitness ==============================' % time_stamp)
        happyforexGA.fittest_ind = happyforexGA.population.get_fittest()
               
        log.info('#============================== Population gets an individual with maximum fitness ==============================')
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#============================== %s Population gets an individual with maximum fitness ==============================' % time_stamp)
        # While population gets an individual with maximum fitness or the population has converged (does not produce different offspring)
        while (happyforexGA.population.fittest < MAX_FITNESS 
                and happyforexGA.generationCount < happyforexGA.population.popSize * 2):  # TODO: for testing only
            
            happyforexGA.generationCount += 1
               
            # Do selection
            log.info('#============================== population selection ==============================')
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            print('#============================== %s population selection ==============================' % time_stamp)
            happyforexGA.selection()
            
            print("==> self.fittest_ind.individual_ID at selection: %s" % happyforexGA.fittest_ind.individual_ID)
            print("==> self.second_fittest_ind.individual_ID at selection: %s" % happyforexGA.second_fittest_ind.individual_ID)
            log.info("==> self.fittest_ind.individual_ID at selection: %s" % happyforexGA.fittest_ind.individual_ID)
            log.info("==> self.second_fittest_ind.individual_ID at selection: %s" % happyforexGA.second_fittest_ind.individual_ID)
               
            # Do crossover
            log.info('#============================== population crossover ==============================')
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            print('#============================== %s population crossover ==============================' % time_stamp)
            happyforexGA.crossover()
            
            print("==> self.fittest_ind.individual_ID after crossover: %s" % happyforexGA.fittest_ind.individual_ID)
            print("==> self.second_fittest_ind.individual_ID after crossover: %s" % happyforexGA.second_fittest_ind.individual_ID)
            log.info("==> self.fittest_ind.individual_ID after crossover: %s" % happyforexGA.fittest_ind.individual_ID)
            log.info("==> self.second_fittest_ind.individual_ID after crossover: %s" % happyforexGA.second_fittest_ind.individual_ID)
               
            # Do mutation under probability
            if random.randint(DEFAULT_NUMBER_INT, MAX_FITNESS) < MAX_FITNESS:
                
                log.info('#============================== population mutation ==============================')
                time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
                print('#============================== %s population mutation ==============================' % time_stamp)
                happyforexGA.mutation()
                
                print("==> self.fittest_ind.individual_ID after mutation: %s" % happyforexGA.fittest_ind.individual_ID)
                print("==> self.second_fittest_ind.individual_ID after mutation: %s" % happyforexGA.second_fittest_ind.individual_ID)
                log.info("==> self.fittest_ind.individual_ID after mutation: %s" % happyforexGA.fittest_ind.individual_ID)
                log.info("==> self.second_fittest_ind.individual_ID after mutation: %s" % happyforexGA.second_fittest_ind.individual_ID)
                       
            # Add highest fitness offspring to population
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            happyforexGA.add_fittest_offspring()
            print("==> Least_fittest_ind.individual_ID: %s" % happyforexGA.least_fittest_ind.individual_ID)
            print("... ==> least_fittest_ind.fitness: %s" % happyforexGA.least_fittest_ind.fitness)                   
            print("... replace by highest fitness offspring individual ==> added_offstring_ind.individual_ID: %s" % happyforexGA.added_offstring_ind.individual_ID)
            print("... ==> added_offstring_ind.fitness: %s" % happyforexGA.added_offstring_ind.fitness)                   
            log.info("==> Least_fittest_ind.individual_ID: %s" % happyforexGA.least_fittest_ind.individual_ID)
            log.info("... ==> least_fittest_ind.fitness: %s" % happyforexGA.least_fittest_ind.fitness)                   
            log.info("... replace by highest fitness offspring individual ==> added_offstring_ind.individual_ID: %s" % happyforexGA.added_offstring_ind.individual_ID)
            log.info("... ==> added_offstring_ind.fitness: %s" % happyforexGA.added_offstring_ind.fitness)                   
            
    #             # Calculate new fitness value
    #             happyforexGA.population.calculate_fittest()
             
            # Get the new individual with highest fitness ==> retrieve the highest fitness for the population
            happyforexGA.fittest_ind = happyforexGA.population.get_fittest()
            
            # Print out and write to CSV file the highest solution + remove the old highest solution file
            log.info("Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            print("%s Generation: %s - Highest Fitness: %s" % (time_stamp, happyforexGA.generationCount, happyforexGA.population.fittest))
            
            if happyforexGA.fittest_ind.fitness < MAX_FITNESS:
                time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
                file_path_highest_solution = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_HIGHEST_FITNESS
                file_path_highest_parameters = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_HIGHEST_PARAMETERS
            
                write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
                write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, file_path_highest_parameters, '=')
            
            write_wholedict2csv_no_header(happyforexGA.population.FITNESS_DICT, folder_output + 'profit_list.csv')
            
            print('#===========================================================================')
            log.info('#===========================================================================')
            
        # Print out and write to CSV file the best solution
        log.info('#===========================================================================')
        log.info("==> Solution found in generation: %s" % happyforexGA.generationCount);
        log.info("Fitness: %s" % happyforexGA.fittest_ind.fitness);
        log.info("Individual_ID: %s" % happyforexGA.fittest_ind.individual_ID)
        log.info("Genes: %s" % happyforexGA.fittest_ind.genes);
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#===========================================================================')
        print("%s ==> Solution found in generation: %s" % (time_stamp, happyforexGA.generationCount))
        print("Fitness: %s" % happyforexGA.fittest_ind.fitness);
        print("Individual_ID: %s" % happyforexGA.fittest_ind.individual_ID)
        print("Genes: %s" % happyforexGA.fittest_ind.genes);
        
        # Write out the whole best parameters
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_BEST_SOLUTION, '=')
        write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_BEST_PARAMETERS, '=')
        
        # Write the population final to a CSV file for reference
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info('#============================== Write the population final to a CSV file ==============================')
        print('#============================== %s Write the population final to a CSV file ==============================' % time_stamp)
        write_wholedict2csv_no_header(happyforexGA.population.individuals_ID_dict,
                                 folder_output + FILENAME_POPULATION_FINAL.replace(".csv", "_" + str(happyforexGA.generationCount) + "th_gen.csv"))
    

################################################################################
########################         MAIN FUNCTIONS        #########################
################################################################################
def main():
        
    #===============================================================================
    ''' RUNNING WHOLE EA WITH GENETIC OPTIMIZATION WITH LOG AND PROFILE 

    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile(FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST):
        remove(FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST)
         
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST))
     
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
     
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
     
    try:
        # running ST
        cProfile.run('ga_run()', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_BACKTEST)
         
    except Exception:
        logging.exception("Exception in main")
        exit(1) 
    '''
    
    #===============================================================================
    ''' RUNNING WHOLE EA WITH GENETIC OPTIMIZATION 
        ga_run()
    '''
    
    #===============================================================================
    ''' RUNNING EA BY ITSELF 
    # create an instance EA for running 
    happyforex_EA_instance = HappyForexEA()
              
    # running EA
    happyforex_EA_instance.ea_run(DEFAULT_PARAMETERS_DATA, 1)
    '''
    
    #===============================================================================
    ''' RUNNING EA BY ITSELF WITH LOG AND PROFILE '''

    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile(FOLDER_DATA_OUTPUT + FILENAME_LOG_EA):
        remove(FOLDER_DATA_OUTPUT + FILENAME_LOG_EA)
           
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", FOLDER_DATA_OUTPUT + FILENAME_LOG_EA))
       
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
       
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
       
    try:
        # print command line arguments
        if (len(sys.argv[1:]) == DEFAULT_NUMBER_INT):
            print("Nothing")
        else:
            for arg in sys.argv[1:]:
                print arg
        
#         # get RUN_FREQUENCY_BY_YEAR
#         RUN_FREQUENCY_BY_YEAR = str(sys.argv[DEFAULT_NUMBER_INT])
#         print("==> RUN_FREQUENCY_BY_YEAR = %s" % RUN_FREQUENCY_BY_YEAR)
#             
#         if (len(sys.argv) == DEFAULT_NUMBER_INT
#             or RUN_FREQUENCY_BY_YEAR != RUN_FREQUENCY_1_YEAR
#             or RUN_FREQUENCY_BY_YEAR != RUN_FREQUENCY_3_YEAR
#             or RUN_FREQUENCY_BY_YEAR != RUN_FREQUENCY_5_YEAR
#             or RUN_FREQUENCY_BY_YEAR != RUN_FREQUENCY_7_YEAR
#             or RUN_FREQUENCY_BY_YEAR != RUN_FREQUENCY_9_YEAR):
#             
#             # create an instance EA for running 
#             happyforex_EA_instance = HappyForexEA()
#               
#             # running EA
#             cProfile.run('happyforex_EA_instance.ea_run(DEFAULT_PARAMETERS_DATA, 1, 1)', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_EA)
# 
#         else:
#             
#             # create an instance EA for running 
#             happyforex_EA_instance = HappyForexEA()
#               
#             # running EA
#             cProfile.run('happyforex_EA_instance.ea_run(DEFAULT_PARAMETERS_DATA, 1, ' + RUN_FREQUENCY_BY_YEAR + ')', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_EA)
                  
    except Exception:
        logging.exception("Exception in main")
        exit(1) 


################################################################################
##########################           MAIN           ############################
################################################################################        
if __name__ == "__main__":

    #===============================================================================
    ''' RUNNING WHOLE EA WITH GENETIC OPTIMIZATION BY ITSELF
    # create an instance GA for running 
    happyforex_GA_instance = HappyForexGenericAlgorithm()
              
    # running GA
    happyforex_GA_instance.run(1)
    '''
    
    #===============================================================================
    ''' RUNNING WHOLE EA WITH GENETIC OPTIMIZATION WITH LOG AND PROFILE '''
    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile(FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST):
        remove(FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST)
         
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST))
     
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
     
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
     
    try:
        print("==> RUN_FREQUENCY_BY_YEAR: %s" % len(sys.argv[1:]))
        
        # get RUN_FREQUENCY_BY_YEAR
        if (len(sys.argv[1:]) == DEFAULT_NUMBER_INT):
            # create an instance GA for running 
            happyforex_GA_instance = HappyForexGenericAlgorithm()
                      
            # running whole EA with optimization
            cProfile.run('happyforex_GA_instance.ga_run(1)', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_BACKTEST)
        else:
            for RUN_FREQUENCY_BY_YEAR in sys.argv[1:]:
                if (str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_1_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_3_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_5_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_7_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_9_YEAR):
                    
                    # create an instance GA for running 
                    happyforex_GA_instance = HappyForexGenericAlgorithm()
                              
                    # running whole EA with optimization
                    cProfile.run('happyforex_GA_instance.ga_run(' + str(RUN_FREQUENCY_BY_YEAR) + ')'
                                 , FOLDER_DATA_OUTPUT + FILENAME_PROFILE_BACKTEST)
                    
                    break
    except Exception:
        logging.exception("Exception in main")
        exit(1) 
    
    #===============================================================================
    ''' RUNNING EA BY ITSELF 
    # create an instance EA for running 
    happyforex_EA_instance = HappyForexEA()
              
    # running EA
    happyforex_EA_instance.ea_run(DEFAULT_PARAMETERS_DATA, 1)
    '''
    
    #===============================================================================
    ''' RUNNING EA BY ITSELF WITH LOG AND PROFILE 
    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile(FOLDER_DATA_OUTPUT + FILENAME_LOG_EA):
        remove(FOLDER_DATA_OUTPUT + FILENAME_LOG_EA)
           
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", FOLDER_DATA_OUTPUT + FILENAME_LOG_EA))
       
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
       
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
       
    try:
        # get RUN_FREQUENCY_BY_YEAR
        if (len(sys.argv[1:]) == DEFAULT_NUMBER_INT):
             
            # create an instance EA for running 
            happyforex_EA_instance = HappyForexEA()
               
            # running EA
            cProfile.run('happyforex_EA_instance.ea_run(DEFAULT_PARAMETERS_DATA, 1, 1)', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_EA)
        else:
            for RUN_FREQUENCY_BY_YEAR in sys.argv[1:]:
                if (str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_1_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_3_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_5_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_7_YEAR
                    or str(RUN_FREQUENCY_BY_YEAR) == RUN_FREQUENCY_9_YEAR):
                    
                    # create an instance EA for running 
                    happyforex_EA_instance = HappyForexEA()
                       
                    # running EA
                    cProfile.run('happyforex_EA_instance.ea_run(DEFAULT_PARAMETERS_DATA, 1, ' + str(RUN_FREQUENCY_BY_YEAR) + ')'
                                 , FOLDER_DATA_OUTPUT + FILENAME_PROFILE_EA)
                    
                    break
    except Exception:
        logging.exception("Exception in main")
        exit(1) 
    '''
