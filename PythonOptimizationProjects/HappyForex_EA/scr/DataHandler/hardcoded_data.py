'''
Created on Dec 29, 2017

@author: cao.vu.lam
'''
#!/usr/bin/env python

#===============================================================================
DEFAULT_NUMBER_INT = 0
DEFAULT_SECOND_NUMBER_INT = 1
DEFAULT_NUMBER_FLOAT = 0.00
DEFAULT_SECOND_NUMBER_FLOAT = 1.00

VALUE_COL_INDEX = 1

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
SYMBOL = 'USDJPY'
QUOTE_CURRENCY = 'JPY'
BASE_CURRENCY = 'USD'
ALL_CURRENCY = 'ALL'

import os
SCR_DIR_PATH = os.path.dirname(os.getcwd())
FOLDER_DATA_INPUT = SCR_DIR_PATH + '/DataHandler/data/input/'
FOLDER_DATA_OUTPUT = SCR_DIR_PATH + '/DataHandler/data/output/'
FOLDER_TICK_DATA_ORIGINAL = '/USDJPY_GAINCapital_Original'
FOLDER_TICK_DATA_MODIFIED = '/USDJPY_GAINCapital_Modified'
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

#===============================================================================
import pandas as pd
import sys
import csv
import logging
import glob
import _strptime
from datetime import datetime, date
from os import path, remove
from decimal import Decimal
from math import factorial as f

log = logging.getLogger(__name__)

       
################################################################################
#########################           CLASS           ############################
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
    
#     # GAIN Capital tick data from 2005 to 2009
#     datetime_col_index = 2
#     bid_col_index = 3
#     ask_col_index = 4
    
    # GAIN Capital tick data from 2010 to 2017
    datetime_col_index = 3
    bid_col_index = 4
    ask_col_index = 5
    
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
      
#     log.info("==> Completed combining {0} files!!!".format(file_index - DEFAULT_SECOND_NUMBER_INT))
#     time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#     print("{0} ==> Completed combining {1} files!!!".format(time_stamp, file_index - DEFAULT_SECOND_NUMBER_INT))


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
def point_of_symbol(number):
    ''' point=1/pow(10,digits): definition from MetaTrader 4 Manager API '''
    
    # check number whether it is a float number (just in case)
    if float_checker(number) == False:
        return DEFAULT_NUMBER_INT
    else:
        point = float(1) / pow(10, digit_of_symbol(number))
        return point


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

        
#===============================================================================
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
        
#===============================================================================
# # Create TICK_DATA with Modification from Original Tick Data CSV file WITH milliseconds
# # --> format the date time as expected WITH millisecond (Note: need to do 2 time with columns format from from 2005 to 2009 VS from 2010 to 2017)
# FOLDER_TICK_DATA_ORIGINAL = '/USDJPY_GAINCapital_Original_with_milliseconds'
# MARKET_TIME_STANDARD = '1970.01.01_00:00:00.000'
# DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S.%f'
# create_multiple_tick_data_from_wholefolder_gaincapital_format(FOLDER_DATA_INPUT + SYMBOL + FOLDER_TICK_DATA_ORIGINAL)
# 
# # Create TICK_DATA with Modification from Original Tick Data CSV file WITHOUT milliseconds
# # --> format the date time as expected WITHOUT millisecond (Note: need to do 2 time with columns format from from 2005 to 2009 VS from 2010 to 2017)
# FOLDER_TICK_DATA_ORIGINAL = '/USDJPY_GAINCapital_Original_without_milliseconds'
# MARKET_TIME_STANDARD = '1970.01.01_00:00:00'
# DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S'
# create_multiple_tick_data_from_wholefolder_gaincapital_format(FOLDER_DATA_INPUT + SYMBOL + FOLDER_TICK_DATA_ORIGINAL)
# 
# # Create CALENDAR_DATA with Modification from Original Calendar Data CSV file WITHOUT milliseconds
# create_multiple_calendar_data_from_wholefolder_forexfactory_format(FOLDER_DATA_INPUT + FOLDER_CALENDAR_DATA_ORIGINAL)


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

