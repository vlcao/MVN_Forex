'''
Created on Dec 29, 2017

@author: cao.vu.lam
'''
#!/usr/bin/env python

#===============================================================================
DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1

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
NET_PROFIT = 360.00
COMMISSION = 0.75
LEVERAGE = 100.00
ONE_LOT_VALUE = 100000.00

# HEADER_ORDER_DICT = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance'] 
ORDER_TYPE_COL_INDEX = 3
ORDER_ID_COL_INDEX = 4
LOTS_COL_INDEX = 5
PRICE_ENTRY_COL_INDEX = 6
PRICE_EXIT_COL_INDEX = 7
PROFIT_COL_INDEX = 10
BALANCE_COL_INDEX = 11

# HEADER_TICK_DATA = ['Date_Time', Day, Time, 'Bid', 'Ask', 'Bid_NextTick', 'Ask_NextTick']
DATETIME_COL_INDEX = 0
DAY_COL_INDEX = 1
TIME_COL_INDEX = 2
BID_COL_INDEX = 3
ASK_COL_INDEX = 4
BID_NEXTTICK_COL_INDEX = 5
ASK_NEXTTICK_COL_INDEX = 6

PERIOD = 'H1'
SYMBOL = 'USDJPY'
QUOTE_CURRENCY = 'JPY'

import os
SCR_DIR_PATH = os.path.dirname(os.getcwd())
FOLDER_DATA_INPUT = SCR_DIR_PATH + '/DataHandler/data/input/'
FOLDER_DATA_OUTPUT = SCR_DIR_PATH + '/DataHandler/data/output/'
FOLDER_TICK_DATA_ORIGINAL = '/USDJPY_Ticks_May2009_Nov2016_Original'
FOLDER_TICK_DATA_MODIFIED = '/USDJPY_Ticks_May2009_Nov2016_Modified'

FILENAME_TICK_DATA = SYMBOL + '/USDJPY-2009-05.csv'
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
FILENAME_BEST_SOLUTION = 'fitness_best_solution.csv'
FILENAME_BEST_PARAMETERS = SYMBOL + '_whole_best_parameters.csv'
FILENAME_HIGHEST_FITNESS = 'fitness_highest_solution.csv'
FILENAME_HIGHEST_PARAMETERS = SYMBOL + '_whole_highest_parameters.csv'
FILENAME_ORDER_CLOSED_HISTORY = 'order_closed_history.csv'
FILENAME_ORDER_OPENED_HISTORY = 'order_opened_history.csv'
FILENAME_ORDER_DELETED_HISTORY = 'order_deleted_history.csv'
FILENAME_DATE_DICT = 'data_date_dict.csv'

MARKET_TIME_STANDARD = '1970.01.01_00:00:00,000'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S,%f'
TIME_STAMP_FORMAT = '%Y.%m.%d_%H.%M.%S.%f'

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
from datetime import datetime
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
    data_col = len(source_array[DEFAULT_NUMBER]) 
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
            if str(old_array[row_old_array][DEFAULT_NUMBER]) == str(new_array[row_new_array][DEFAULT_NUMBER]):
                old_array[row_old_array][col_value_index] = new_array[row_new_array][col_value_index]
        
    return old_array

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
    i = DEFAULT_NUMBER
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
            
        i += DEFAULT_SECOND_NUMBER
                
    return forwardflash_path

#===============================================================================
def create_a_new_row(previous_row, row):
    ''' Analyze the string separated by Space to get Date, Time, Ask, Bid and then create a new version 
    of that row as Date_Time, Ask, Bid, Ask_NextTick (from next row), Bid_NextTick (from next row) 
    Ex: [USD/JPY, 20090501 00:00:00.296, 98.89, 98.902]
        [USD/JPY, 20090501 00:00:00.299, 98.887, 98.899]
        ==> [2009.05.01_00:00:00,296, 98.89, 98.902, 98.887, 98.899]
        ==> [1241136000296.0, 98.89, 98.902, 98.887, 98.899] '''
    
    # --> get the part BEFORE (Date) and AFTER (Time) the Space
    split_space = previous_row[DEFAULT_SECOND_NUMBER].split(' ')
    date_part = split_space[DEFAULT_NUMBER]
    time_part = split_space[DEFAULT_SECOND_NUMBER].split('.')
    
    # --> get the part BEFORE (Second) and AFTER (Millisecond) the Dot
    time_second_part = time_part[DEFAULT_NUMBER]
    time_milisecond_part = time_part[DEFAULT_SECOND_NUMBER]
    
    # --> format the date time as expected
    date_modified_part = ('' + date_part[:4] + '.' + date_part[4:6] + '.' + date_part[6:8] 
                          + '_' + time_second_part + ',' + time_milisecond_part)
    
    fdate_modified_part = convert_string_datetime2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
    fday_modified_part = convert_string_day2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
    ftime_modified_part = convert_string_millisecond2float(date_modified_part, MARKET_TIME_STANDARD, DATETIME_FORMAT)
    
    # --> create a new row for Tick data
    return (['%f' % fdate_modified_part, fday_modified_part, ftime_modified_part, float(previous_row[2]), float(previous_row[3]), float(row[2]), float(row[3])],
            ['%f' % fdate_modified_part, date_modified_part])

#===============================================================================
def create_multiple_tick_data_from_wholefolder(folder_name):
    ''' Read each row of all Original Tick data file, create a new version of that row, and then
    combine them by writing each new version row into 1 new CSV file 
    Ex: [USD/JPY, 20090501 00:00:00.296, 98.89, 98.902]
        [USD/JPY, 20090501 00:00:00.299, 98.887, 98.899]
        ==> [2009.05.01_00:00:00,296, 98.89, 98.902, 98.887, 98.899]
        ==> [1241136000296.0, 98.89, 98.902, 98.887, 98.899] '''
    
    # convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    allFiles = glob.glob(folder_name + '/*.csv')
    
    file_index = DEFAULT_NUMBER
    for file_ in allFiles:
        print("==> processing file {0}...".format(file_index))
        
        file_name = convert_backflash2forwardflash_change_output_folder(file_)
         
        if (file_index % 10 == DEFAULT_NUMBER):
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
            
            # create a new version of row with 2 parts
            new_row = create_a_new_row(previous_row, row)
            
            # write to CSV file part 1 of a new row: [Date_Time, Day, Millisecond, Bid, Ask, Bid_NextTick, Ak_NextTick]
            fdate_modified_part = ','. join([str(j) for j in new_row[DEFAULT_NUMBER]]) + "\n"
            csv_new_row_write.write(fdate_modified_part)
            
            # write to CSV file part 1 of a new row: [Date_Time, Day, Millisecond, Bid, Ask, Bid_NextTick, Ak_NextTick]
            fdate_dictionary = ','. join([str(j) for j in new_row[DEFAULT_SECOND_NUMBER]]) + "\n"
            csv_date_dict.write(fdate_dictionary)
              
            # --> save the current row
            previous_row = row
              
        ifile.close()
      
        # write the last row
        last_row = [0, 0, 0, 0]
        
        # create a new version of last row with 2 parts
        new_row = create_a_new_row(previous_row, last_row)
        
        # write to CSV file part 1 of the last new row: [Date_Time, Bid, Ask, Bid_NextTick, Ak_NextTick]
        fdate_modified_part = ','. join([str(j) for j in new_row[DEFAULT_NUMBER]]) + "\n"
        csv_new_row_write.write(fdate_modified_part)
        
        # write to CSV file part 1 of the last new row: [Date_Time, Bid, Ask, Bid_NextTick, Ak_NextTick]
        fdate_dictionary = ','. join([str(j) for j in new_row[DEFAULT_SECOND_NUMBER]]) + "\n"
        csv_date_dict.write(fdate_dictionary)
      
        file_index += DEFAULT_SECOND_NUMBER
          
    print("==> Completed {0} files!!!".format(file_index))

#===============================================================================
def create_a_tick_data_from_wholefolder(folder_name, file_name):
    ''' Read each row of all Original Tick data file, create a new version of that row, and then
    combine them by writing each new version row into 1 new CSV file 
    Ex: [USD/JPY, 20090501 00:00:00.296, 98.89, 98.902]
        [USD/JPY, 20090501 00:00:00.299, 98.887, 98.899]
        ==> [2009.05.01_00:00:00,296, 98.89, 98.902, 98.887, 98.899]
        ==> [1241136000296.0, 98.89, 98.902, 98.887, 98.899] '''
    
# convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    allFiles = glob.glob(folder_name + '/*.csv')
    
    file_name = convert_backflash2forwardflash_change_output_folder(file_name)
        
    file_index = DEFAULT_NUMBER
    for file_ in allFiles:
        print("==> processing file {0}...".format(file_index))
         
        if (file_index % 10 == DEFAULT_NUMBER):
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
            
            # create a new version of row with 2 parts
            new_row = create_a_new_row(previous_row, row)
            
            # write to CSV file part 1 of a new row: [Date_Time, Day, Millisecond, Bid, Ask, Bid_NextTick, Ak_NextTick]
            fdate_modified_part = ','. join([str(j) for j in new_row[DEFAULT_NUMBER]]) + "\n"
            csv_new_row_write.write(fdate_modified_part)
            
            # write to CSV file part 1 of a new row: [Date_Time, Day, Millisecond, Bid, Ask, Bid_NextTick, Ak_NextTick]
            fdate_dictionary = ','. join([str(j) for j in new_row[DEFAULT_SECOND_NUMBER]]) + "\n"
            csv_date_dict.write(fdate_dictionary)
              
            # --> save the current row
            previous_row = row
              
        ifile.close()
      
        # write the last row
        last_row = [0, 0, 0, 0]
        
        # create a new version of last row with 2 parts
        new_row = create_a_new_row(previous_row, last_row)
        
        # write to CSV file part 1 of the last new row: [Date_Time, Bid, Ask, Bid_NextTick, Ak_NextTick]
        fdate_modified_part = ','. join([str(j) for j in new_row[DEFAULT_NUMBER]]) + "\n"
        csv_new_row_write.write(fdate_modified_part)
        
        # write to CSV file part 1 of the last new row: [Date_Time, Bid, Ask, Bid_NextTick, Ak_NextTick]
        fdate_dictionary = ','. join([str(j) for j in new_row[DEFAULT_SECOND_NUMBER]]) + "\n"
        csv_date_dict.write(fdate_dictionary)
      
        file_index += DEFAULT_SECOND_NUMBER
          
    print("==> Completed {0} files!!!".format(file_index))

#===============================================================================
def combine_all_files_in_a_folder(folder_name, combined_file_name):    
    ''' Combine all CSV files in a folder into 1 CSV file only '''

    # convert the back flash with forward flash (just in case)
    folder_name = convert_backflash2forwardflash(folder_name)
    allFiles = glob.glob(folder_name + '/*.csv')
    
#     combined_file = []
    combined_file_name = convert_backflash2forwardflash(combined_file_name)
    csv_combined_file_write = open(combined_file_name, "w")  # "w" indicates that you're writing strings to the file
             
    file_index = DEFAULT_NUMBER
    for file_ in allFiles:
        print("==> processing file {0}...".format(file_index))
        
        if (file_index % 10 == DEFAULT_NUMBER):
            perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
            print("... ==> processing {0}% of the data...".format(perc))
          
        # open the CSV file
        ifile = open(file_, "rU")
        reader = csv.reader(ifile, delimiter=",")
          
        for row in reader:
            csv_combined_file_write.write(','. join([str(j) for j in row]) + "\n")
              
        ifile.close()
        
        file_index += DEFAULT_SECOND_NUMBER
      
    print("==> Completed {0} files!!!".format(file_index))

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
            
            new_row = create_a_new_row(previous_row, row)
            
            list_.append (new_row)
            
            # --> save the current row
            previous_row = row
            
        ifile.close()
    
        # save the last row
        last_row = [0, 0, 0, 0]
        new_last_row = create_a_new_row(previous_row, last_row)
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
        return DEFAULT_NUMBER
    else:
        return number % 1

#===============================================================================
def point_of_symbol(number):
    ''' point=1/pow(10,digits): definition from MetaTrader 4 Manager API '''
    
    # check number whether it is a float number (just in case)
    if float_checker(number) == False:
        return DEFAULT_NUMBER
    else:
        point = float(1) / pow(10, digit_of_symbol(number))
        return point

#===============================================================================
def digit_of_symbol(number):
    # check number whether it is a float number (just in case)
    if float_checker(number) == False:
        return DEFAULT_NUMBER
    else:
        num_of_digit = Decimal(str(number))
        digit = (num_of_digit.as_tuple().exponent) * (-1)
        return int(digit)

#===============================================================================
def get_subset_dataframe(origin_dataframe, subtract_list_string):
        
    # initialize the OPTIMIZED_PARAMETERS_DATA    
    list_count = DEFAULT_NUMBER
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
    list_count = DEFAULT_NUMBER
    data_col = len(origin_data[DEFAULT_NUMBER]) 
    data_row = len(subtract_list_string)
    subset_data = [["" for x in range(data_col)] for y in range(data_row)] 
    
    # append all needed item in the list together
    while (list_count < len(subtract_list_string)):
        for i in range(len(origin_data)):
            if subtract_list_string[list_count] == origin_data[i][DEFAULT_NUMBER]:
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
def write_dict2csv_no_header(dictionary_out, file_name):
     
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
def display_an_array_with_delimiter(array_out, delimiter):
    out_length = len(array_out)
    
    if out_length <= 100:
        for i in range(out_length):
            sMyArray = [str(j) for j in array_out[i]]
            print(delimiter . join(sMyArray))
            log.info(delimiter . join(sMyArray))
    else:
        # display 20 first items
        for i in range(20):
            sMyArray = [str(j) for j in array_out[i]]
            print(delimiter . join(sMyArray))
            log.info(delimiter . join(sMyArray))
            
        print('...    ...    ...    ...    ...    ...    ...')
        log.info('...    ...    ...    ...    ...    ...    ...')
        
        # display 20 last items
        i = out_length - 20
        while i < out_length:
            sMyArray = [str(j) for j in array_out[i]]
            print(delimiter . join(sMyArray))
            log.info(delimiter . join(sMyArray))
            i += 1
        
    # print the summary
    print('[%s rows x %s columns]' % (out_length, len(array_out[DEFAULT_NUMBER])))
    log.info('[%s rows x %s columns]' % (out_length, len(array_out[DEFAULT_NUMBER])))

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
def convert_string_datetime2float(convert_datetime, std_datetime, sformat):
#     ''' Convert a string of date and time with its standard time and format into integer 
#     which is sum of total days and total seconds. '''
# 
#     convert_datetime = datetime.strptime(convert_datetime, sformat)  
#     std_date = datetime.strptime(std_datetime, sformat)  # standard date
#     
#     # calculate difference between convert_datetime and std_date
#     diff_time = convert_datetime - std_date
#     
#     
#     # convert the different days, seconds and milliseconds into total float
#     return float(diff_time.seconds + diff_time.days)

    ''' Convert a string of date and time with its standard time and format into millisecond in float type '''
    
    # get the millisecond from the input date_time
    convert_datetime_milliseconds = convert_datetime.split(',')[DEFAULT_SECOND_NUMBER]
    
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
def convert_string_millisecond2float(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into float 
    which is sum of total seconds and milliseconds '''

    # get the millisecond from the input date_time
    convert_datetime_milliseconds = convert_datetime.split(',')[DEFAULT_SECOND_NUMBER]
    
    # parse the time format using strptime.
    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
    
    # calculate difference between convert_datetime and std_date
    diff_time = convert_datetime - std_date
    
    # convert the different milliseconds into float
    diff_time__milliseconds = float(diff_time.seconds * 1000) + float(convert_datetime_milliseconds)
    
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
# Create TICK_DATA with Modification from Original Tick Data CSV file
# TICK_DATA = create_a_tick_data_from_wholefolder(FOLDER_DATA_INPUT + SYMBOL + FOLDER_TICK_DATA_ORIGINAL, FOLDER_DATA_OUTPUT + FILENAME_TICK_DATA)
# create_multiple_tick_data_from_wholefolder('E:\EclipsePreferences-csse120-2011-06\Happy Forex\src\DataHandler\data\input\USDJPY\USDJPY_Ticks_May2009_Nov2016_Original')
 

log.info("==> Load DEFAULT_PARAMETERS_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_PARAMETER_DEFAULT))
log.info('===============================================================================')
time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
print("%s ==> Load DEFAULT_PARAMETERS_DATA: %s ..." % (time_stamp, FOLDER_DATA_INPUT + FILENAME_PARAMETER_DEFAULT))
print('===============================================================================')

# Create DEFAULT_PARAMETERS_DATA with CSV file
DEFAULT_PARAMETERS_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_PARAMETER_DEFAULT)

log.info("==> Load SETTING_PARAMETERS_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2))
log.info('===============================================================================')
time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
print("%s ==> Load SETTING_PARAMETERS_DATA: %s ..." % (time_stamp, FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2))
print('===============================================================================')

# Create SETTING_2_PARAMETERS_DATA with CSV file
SETTING_2_PARAMETERS_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_2)
SETTING_3_PARAMETERS_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_PARAMETER_SETTING_3)

log.info("==> Create OPTIMIZED_PARAMETERS_DATA data: %s ..." % (FOLDER_DATA_OUTPUT + FILENAME_OPTIMIZE_PARAMETER))
log.info('===============================================================================')
time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
print("%s ==> Create OPTIMIZED_PARAMETERS_DATA data: %s ..." % (time_stamp, FOLDER_DATA_OUTPUT + FILENAME_OPTIMIZE_PARAMETER))
print('===============================================================================')
# Create OPTIMIZED_PARAMETERS_DATA
OPTIMIZED_PARAMETERS_DATA = get_subset_data(DEFAULT_PARAMETERS_DATA, OPTIMIZE_PARAMETERS_LIST)

