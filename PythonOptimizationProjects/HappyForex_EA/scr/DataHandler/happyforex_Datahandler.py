'''
Created on Dec 29, 2017

@author: cao.vu.lam
'''
import pandas as pd
import sys
import csv
import os
import logging
import glob

from datetime import datetime
from os import path, remove
from decimal import Decimal
from math import factorial as f

log = logging.getLogger(__name__)

#===============================================================================
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
def load_csv2dataframe(file_name_history_data):
    
    # convert the back flash with forward flash (just in case)
    file_name_history_data = convert_backflash2forwardflash(file_name_history_data)
    
    # create a data frame with CSV file
    DataFrame = pd.read_csv(file_name_history_data)
     
    return DataFrame

#===============================================================================
def load_wholefolder2array(folder_name):    

#     folder_name = os.getcwd() + "/tick"  # use your path
    allFiles = glob.glob(folder_name + "/*.csv")
    list_ = []
    for file_ in allFiles:
        # convert the back flash with forward flash (just in case)
        file_ = convert_backflash2forwardflash(file_)
            
        # open the CSV file
        ifile = open(file_, "rU")
        reader = csv.reader(ifile, delimiter=",")
        
        for row in reader:
            list_.append (row)
        
        ifile.close()
        
    return list_
   
#===============================================================================
def load_csv2array(file_name):    
    
    # convert the back flash with forward flash (just in case)
    file_name = convert_backflash2forwardflash(file_name)
    
    # open the CSV file
    ifile = open(file_name, "rU")
    reader = csv.reader(ifile, delimiter=",")

    # put the CSV into an array
    a = []

    for row in reader:
        a.append (row)
    
    ifile.close()
    return a

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
# point=1/pow(10,digits): definition from MetaTrader 4 Manager API 
def point_of_symbol(number):
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
    csv = open(str(file_name), "w")  # "w" indicates that you're writing strings to the file
    
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
''' Display dictionary with the input delimiter (ex: '=' or ',' or '/' etc.) '''
def display_an_dict_with_delimiter(dict_out, delimiter):

    # display dictionary with iterating over items returning key, value tuples
    for key, value in dict_out.iteritems():  
        print('%s' % str(key) + delimiter + '%s' % str(value))
        log.info('%s' % str(key) + delimiter + '%s' % str(value))

#===============================================================================
''' Compare 2 times with a standard time. '''
def is_time_earlier(early_timer, late_time, std_time, sformat):

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
    ''' Convert a string of date and time with its standard time and format into integer 
    which is sum of total days and total seconds. '''

    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
    
    # calculate difference between convert_datetime and std_date
    diff_time = convert_datetime - std_date
    
    # convert the different days and seconds into total integer
    return float(diff_time.seconds + diff_time.days)    
    
#===============================================================================
def convert_string_day2float(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into integer 
    which is sum of total days only '''

    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
    
    # calculate difference between convert_datetime and std_date
    diff_time = convert_datetime - std_date
    
    # convert the different days into total float
    return float(diff_time.days)    
    
#===============================================================================
def convert_string_time2float(convert_datetime, std_datetime, sformat):
    ''' Convert a string of date and time with its standard time and format into integer 
    which is sum of total days only '''

    convert_datetime = datetime.strptime(convert_datetime, sformat)  
    std_date = datetime.strptime(std_datetime, sformat)  # standard date
    
    # calculate difference between convert_datetime and std_date
    diff_time = convert_datetime - std_date
    
    # convert the different seconds into float
    return float(diff_time.seconds)    
    
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
def account_balance(self, row_index):
    ''' Return current balance of all orders '''

    if (HISTORY_DATA[row_index][BALANCE_COL_INDEX] != ""
        and float_checker(float(HISTORY_DATA[row_index][BALANCE_COL_INDEX]))):
            return float(HISTORY_DATA[row_index][BALANCE_COL_INDEX])
    else:
            return float(DEFAULT_NUMBER)
    
#===============================================================================
def max_order(self, num):
    ''' Return TRUE if the total numbers of a day equal the Orders Limit per Day '''

    if self.ords_in_a_day == num: 
        return(True)
    elif self.ords_in_a_day < num: 
        return(False)
    else:
        print("ERROR ==> The ords_in_a_day > OPENORDERSLIMITDAY")
        log.info("ERROR ==> The ords_in_a_day > OPENORDERSLIMITDAY")
        

#===============================================================================
DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1

DAYS_OF_AYEAR = 360
HOURS_OF_ADAY = 24
MINUTES_OF_ANHOUR = 60
SECONDS_OF_AMINUTE = 60

RUN_TIME = DAYS_OF_AYEAR

VALUE_COL_INDEX = 1

OP_BUY = 0.00
OP_SELL = 1.00
OP_BUYLIMIT = 2.00
OP_SELLLIMIT = 3.00
OP_BUYSTOP = 4.00
OP_SELLSTOP = 5.00
# OP_BUY_CLOSED_TOTAL_ORDERS = -10.00
# OP_BUY_CLOSED_TOTAL_ORDERS = -1.00
# OP_DELETED_BUYLIMIT_TOTAL_ORDERS = -2.00
# OP_DELETED_SELLLIMIT_TOTAL_ORDERS = -3.00
# OP_DELETED_BUYSTOP_TOTAL_ORDERS = -4.00
# OP_DELETED_SELLSTOP_TOTAL_ORDERS = -5.00

DEPOSIT = 1000.00
MAX_FITNESS = 100.00
MAX_LOTS = 0.10
NET_PROFIT = 360.00  # ==> $360
COMMISSION = 0.75
LEVERAGE = 100.00
ONE_LOT_VALUE = DEPOSIT * LEVERAGE

PERIOD = 'H1'
SYMBOL = 'GBPUSD'
QUOTE_CURRENCY = 'USD'

SCR_DIR_PATH = convert_backflash2forwardflash(str(os.path.dirname(os.getcwd())))
FOLDER_DATA_INPUT = SCR_DIR_PATH + '/DataHandler/data/input/'
FOLDER_DATA_OUTPUT = SCR_DIR_PATH + '/DataHandler/data/output/'


FILENAME_HISTORY_DATA = SYMBOL + '_M1_1y_2012-2013.csv'
FILENAME_BEST_PARAMETERS = SYMBOL + '_whole_best_parameters.csv'
FILENAME_PARAMETER = 'default_parameters.csv'
FILENAME_OPTIMIZE_PARAMETER = 'optimized_parameters.csv'
FILENAME_POPULATION_INITIAL = 'population_initial.csv'
FILENAME_POPULATION_FINAL = 'population_final.csv'
FILENAME_LOG = 'HappyForexEARun.log'
FILENAME_BEST_SOLUTION = 'fitness_best_solution.csv'
FILENAME_HIGHEST_FITNESS = 'fitness_highest_solution.csv'
FILENAME_ORDER_CLOSED_HISTORY = 'order_closed_history.csv'
FILENAME_ORDER_OPENED_HISTORY = 'order_opened_history.csv'
FILENAME_DATE_DICT = 'data_date_dict.csv'

MARKET_TIME_STANDARD = '01.01.1970_00:00:00'
DATETIME_FORMAT = '%d.%m.%Y_%H:%M:%S'
TIME_STAMP_FORMAT = '%Y.%m.%d_%H.%M.%S'
TIME_STAMP = str(datetime.now().strftime(TIME_STAMP_FORMAT))
HEADER_PARAMETER_FILE = ['Parameter', 'Value']
HEADER_ORDER_HISTORY = ['Date', 'Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance'] 
HEADER_HISTORY_DATA = ['Date', 'Time', 'Bid', 'Ask', 'Volume']
OPTIMIZE_PARAMETERS_LIST = ['FilterSpread', 'Friday', 'OpenOrdersLimitDay', 'Time_closing_trades', 'Time_of_closing_in_hours',
                       'Profit_all_orders', 'Arrangements_of_trades', 'Lots']

#===============================================================================
#===============================================================================

print('===============================================================================')
print("==> Load HISTORY_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_HISTORY_DATA))
log.info('===============================================================================')
log.info("==> Load HISTORY_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_HISTORY_DATA))
# Create HISTORY_DATA with CSV file
HISTORY_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_HISTORY_DATA)
display_an_array_with_delimiter(HISTORY_DATA, '    ')


print("==> Load DEFAULT_PARAMETERS_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_PARAMETER))
print('===============================================================================')
log.info("==> Load DEFAULT_PARAMETERS_DATA: %s ..." % (FOLDER_DATA_INPUT + FILENAME_PARAMETER))
log.info('===============================================================================')
# Create DEFAULT_PARAMETERS_DATA with CSV file
DEFAULT_PARAMETERS_DATA = load_csv2array(FOLDER_DATA_INPUT + FILENAME_PARAMETER)
display_an_array_with_delimiter(DEFAULT_PARAMETERS_DATA, '=')



print("==> Create optimized_parameters data: %s ..." % (FOLDER_DATA_OUTPUT + FILENAME_OPTIMIZE_PARAMETER))
print('===============================================================================')
log.info("==> Create optimized_parameters data: %s ..." % (FOLDER_DATA_OUTPUT + FILENAME_OPTIMIZE_PARAMETER))
log.info('===============================================================================')
# Create OPTIMIZED_PARAMETERS_DATA
OPTIMIZED_PARAMETERS_DATA = get_subset_data(DEFAULT_PARAMETERS_DATA, OPTIMIZE_PARAMETERS_LIST)
display_an_array_with_delimiter(OPTIMIZED_PARAMETERS_DATA, '=')


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

EXCHANGE_RATE_USD = {}
EXCHANGE_RATE_USD['USD'] = 1.00
EXCHANGE_RATE_USD['CAD'] = 0.803332
EXCHANGE_RATE_USD['GBP'] = 1.37452
EXCHANGE_RATE_USD['JPY'] = 0.00902088

#===============================================================================
#===============================================================================

# HEADER_ORDER_HISTORY = ['Date', 'Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance'] 
ORDER_TYPE_COL_INDEX = 2
ORDER_ID_COL_INDEX = 3
LOTS_COL_INDEX = 4
PRICE_COL_INDEX = 5
PROFIT_COL_INDEX = 8
BALANCE_COL_INDEX = 9

# HEADER_HISTORY_DATA = ['Date', 'Time', 'Bid', 'Ask', 'Volume']
DATE_COL_INDEX = 0
TIME_COL_INDEX = 1
BID_COL_INDEX = 2
ASK_COL_INDEX = 3
VOLUME_COL_INDEX = 4

DIGITS = digit_of_symbol(float(HISTORY_DATA[DEFAULT_NUMBER][BID_COL_INDEX]))
POINT = point_of_symbol(float(HISTORY_DATA[DEFAULT_NUMBER][BID_COL_INDEX]))
print('===============================================================================')
log.info('===============================================================================')

#===============================================================================
#===============================================================================

# name_ea_row_index = 0
# magic_row_index = 1
# filterspread_row_index = 2
# spreadmax_row_index = 3
# a_row_index = 4
# monday_row_index = 5
# tuesday_row_index = 6
# wednesday_row_index = 7
# thursday_row_index = 8
# friday_row_index = 9
# saturday_row_index = 10
# sunday_row_index = 11
# b_row_index = 12
# trading_24h_row_index = 13
# gmt_offset_row_index = 14
# hour_of_trading_from_row_index = 15
# hour_of_trading_to_row_index = 16
# use_orderslimit_row_index = 17
# openorderslimitday_row_index = 18
# c_row_index = 19
# time_closing_trades_row_index = 20
# time_of_closing_in_hours_row_index = 21
# time_of_closing_in_minutes_row_index = 22
# d_row_index = 23
# profit_row_index = 24
# profit_all_orders_row_index = 25
# e_row_index = 26
# openorderslimit_row_index = 27
# singleordersl_row_index = 28
# singleordertp_row_index = 29
# f_row_index = 30
# arrangements_of_trades_row_index = 31
# g_row_index = 32
# lots_row_index = 33
# slippage_row_index = 34
# h_row_index = 35
# set_up_of_loss_row_index = 36
# amount_of_loss_row_index = 37
# i_row_index = 38
# closing_of_all_trades_row_index = 39
# j_row_index = 40
# usenewsfilter_row_index = 41
# minsbeforenews_row_index = 42
# minsafternews_row_index = 43
# newsimpact_row_index = 44
# k_row_index = 45
# filtering_row_index = 46
# l_row_index = 47
# autoequitymanager_row_index = 48
# equitygainpercent_row_index = 49
# safeequitystopout_row_index = 50
# safeequityrisk_row_index = 51
#  
# 
# NAME_EA = str(DEFAULT_PARAMETERS_DATA[name_ea_row_index]
#               [VALUE_COL_INDEX])
# MAGIC = int(DEFAULT_PARAMETERS_DATA[magic_row_index]
#             [VALUE_COL_INDEX])
# FILTERSPREAD = bool(str(DEFAULT_PARAMETERS_DATA[filterspread_row_index]
#                         [VALUE_COL_INDEX]).title())
# SPREADMAX = float(DEFAULT_PARAMETERS_DATA[spreadmax_row_index]
#                   [VALUE_COL_INDEX])
# A = str(DEFAULT_PARAMETERS_DATA[a_row_index]
#           [VALUE_COL_INDEX])
# MONDAY = bool(str(DEFAULT_PARAMETERS_DATA[monday_row_index]
#                [VALUE_COL_INDEX]).title())
# TUESDAY = bool(str(DEFAULT_PARAMETERS_DATA[tuesday_row_index]
#                 [VALUE_COL_INDEX]).title())
# WEDNESDAY = bool(str(DEFAULT_PARAMETERS_DATA[wednesday_row_index]
#                   [VALUE_COL_INDEX]).title())
# THURSDAY = bool(str(DEFAULT_PARAMETERS_DATA[thursday_row_index]
#                  [VALUE_COL_INDEX]).title())
# FRIDAY = bool(str(DEFAULT_PARAMETERS_DATA[friday_row_index]
#                [VALUE_COL_INDEX]).title())
# SATURDAY = bool(str(DEFAULT_PARAMETERS_DATA[saturday_row_index
#                                          ][VALUE_COL_INDEX]).title())
# SUNDAY = bool(str(DEFAULT_PARAMETERS_DATA[sunday_row_index]
#                [VALUE_COL_INDEX]).title())
# B = str(DEFAULT_PARAMETERS_DATA[b_row_index]
#           [VALUE_COL_INDEX])
# TRADING_24H = bool(str(DEFAULT_PARAMETERS_DATA[trading_24h_row_index]
#                     [VALUE_COL_INDEX]).title())
# GMT_OFFSET = int(DEFAULT_PARAMETERS_DATA[gmt_offset_row_index]
#                  [VALUE_COL_INDEX])
# HOUR_OF_TRADING_FROM = int(DEFAULT_PARAMETERS_DATA[hour_of_trading_from_row_index]
#                            [VALUE_COL_INDEX])
# HOUR_OF_TRADING_TO = int(DEFAULT_PARAMETERS_DATA[hour_of_trading_to_row_index]
#                          [VALUE_COL_INDEX])
# USE_ORDERSLIMIT = bool(str(DEFAULT_PARAMETERS_DATA[use_orderslimit_row_index]
#                         [VALUE_COL_INDEX]).title())
# OPENORDERSLIMITDAY = int(DEFAULT_PARAMETERS_DATA[openorderslimitday_row_index]
#                            [VALUE_COL_INDEX])
# C = str(DEFAULT_PARAMETERS_DATA[c_row_index]
#           [VALUE_COL_INDEX])
# TIME_CLOSING_TRADES = bool(str(DEFAULT_PARAMETERS_DATA[time_closing_trades_row_index]
#                             [VALUE_COL_INDEX]).title())
# TIME_OF_CLOSING_IN_HOURS = int(DEFAULT_PARAMETERS_DATA[time_of_closing_in_hours_row_index]
#                                [VALUE_COL_INDEX])
# TIME_OF_CLOSING_IN_MINUTES = int(DEFAULT_PARAMETERS_DATA[time_of_closing_in_minutes_row_index]
#                                  [VALUE_COL_INDEX])
# D = str(DEFAULT_PARAMETERS_DATA[d_row_index]
#           [VALUE_COL_INDEX])
# PROFIT = bool(str(DEFAULT_PARAMETERS_DATA[profit_row_index]
#                [VALUE_COL_INDEX]).title())
# PROFIT_ALL_ORDERS = float(DEFAULT_PARAMETERS_DATA[profit_all_orders_row_index]
#                           [VALUE_COL_INDEX])
# E = str(DEFAULT_PARAMETERS_DATA[e_row_index]
#           [VALUE_COL_INDEX])
# OPENORDERSLIMIT = int(DEFAULT_PARAMETERS_DATA[openorderslimit_row_index]
#                         [VALUE_COL_INDEX])
# SINGLEORDERSL = float(DEFAULT_PARAMETERS_DATA[singleordersl_row_index]
#                       [VALUE_COL_INDEX])
# SINGLEORDERTP = float(DEFAULT_PARAMETERS_DATA[singleordertp_row_index]
#                       [VALUE_COL_INDEX])
# F = str(DEFAULT_PARAMETERS_DATA[f_row_index]
#           [VALUE_COL_INDEX])
# ARRANGEMENTS_OF_TRADES = float(DEFAULT_PARAMETERS_DATA[arrangements_of_trades_row_index]
#                                [VALUE_COL_INDEX])
# G = str(DEFAULT_PARAMETERS_DATA[g_row_index]
#           [VALUE_COL_INDEX])
# LOTS = float(DEFAULT_PARAMETERS_DATA[lots_row_index]
#              [VALUE_COL_INDEX])
# SLIPPAGE = float(DEFAULT_PARAMETERS_DATA[slippage_row_index]
#                  [VALUE_COL_INDEX])
# H = str(DEFAULT_PARAMETERS_DATA[h_row_index]
#           [VALUE_COL_INDEX])
# SET_UP_OF_LOSS = bool(str(DEFAULT_PARAMETERS_DATA[set_up_of_loss_row_index]
#                        [VALUE_COL_INDEX]).title())
# AMOUNT_OF_LOSS = float(DEFAULT_PARAMETERS_DATA[amount_of_loss_row_index]
#                        [VALUE_COL_INDEX])
# I = str(DEFAULT_PARAMETERS_DATA[i_row_index]
#           [VALUE_COL_INDEX])
# CLOSING_OF_ALL_TRADES = bool(str(DEFAULT_PARAMETERS_DATA[closing_of_all_trades_row_index]
#                               [VALUE_COL_INDEX]).title())
# J = str(DEFAULT_PARAMETERS_DATA[j_row_index]
#           [VALUE_COL_INDEX])
# USENEWSFILTER = bool(str(DEFAULT_PARAMETERS_DATA[usenewsfilter_row_index]
#                       [VALUE_COL_INDEX]).title())
# MINSBEFORENEWS = int(DEFAULT_PARAMETERS_DATA[minsbeforenews_row_index]
#                        [VALUE_COL_INDEX])
# MINSAFTERNEWS = int(DEFAULT_PARAMETERS_DATA[minsafternews_row_index]
#                       [VALUE_COL_INDEX])
# NEWSIMPACT = int(DEFAULT_PARAMETERS_DATA[newsimpact_row_index]
#                    [VALUE_COL_INDEX])
# K = str(DEFAULT_PARAMETERS_DATA[k_row_index]
#           [VALUE_COL_INDEX])
# FILTERING = bool(str(DEFAULT_PARAMETERS_DATA[filtering_row_index]
#                   [VALUE_COL_INDEX]).title())
# L = str(DEFAULT_PARAMETERS_DATA[l_row_index]
#           [VALUE_COL_INDEX])
# AUTOEQUITYMANAGER = bool(str(DEFAULT_PARAMETERS_DATA[autoequitymanager_row_index]
#                           [VALUE_COL_INDEX]).title())
# EQUITYGAINPERCENT = float(DEFAULT_PARAMETERS_DATA[equitygainpercent_row_index]
#                           [VALUE_COL_INDEX])
# SAFEEQUITYSTOPOUT = bool(str(DEFAULT_PARAMETERS_DATA[safeequitystopout_row_index]
#                           [VALUE_COL_INDEX]).title())
# SAFEEQUITYRISK = float(DEFAULT_PARAMETERS_DATA[safeequityrisk_row_index]
#                        [VALUE_COL_INDEX])
 
#===============================================================================
#===============================================================================

# print("==>  NAME_EA:  %s" % NAME_EA)
# print("==> MAGIC:  %s" % MAGIC)
# print("==> FILTERSPREAD:  %s" % FILTERSPREAD)
# print("==> SPREADMAX:  %s" % SPREADMAX)
# print("==> A:  %s" % A)
# print("==> MONDAY:  %s" % MONDAY)
# print("==> TUESDAY:  %s" % TUESDAY)
# print("==> WEDNESDAY:  %s" % WEDNESDAY)
# print("==> THURSDAY:  %s" % THURSDAY)
# print("==> FRIDAY:  %s" % FRIDAY)
# print("==> SATURDAY:  %s" % SATURDAY)
# print("==> SUNDAY:  %s" % SUNDAY)
# print("==> B:  %s" % B)
# print("==> TRADING_24H:  %s" % TRADING_24H)
# print("==> GMT_OFFSET:  %s" % GMT_OFFSET)
# print("==> HOUR_OF_TRADING_FROM:  %s" % HOUR_OF_TRADING_FROM)
# print("==> HOUR_OF_TRADING_TO:  %s" % HOUR_OF_TRADING_TO)
# print("==> USE_ORDERSLIMIT:  %s" % USE_ORDERSLIMIT)
# print("==> OPENORDERSLIMITDAY:  %s" % OPENORDERSLIMITDAY)
# print("==> C:  %s" % C)
# print("==> TIME_CLOSING_TRADES:  %s" % TIME_CLOSING_TRADES)
# print("==> TIME_OF_CLOSING_IN_HOURS:  %s" % TIME_OF_CLOSING_IN_HOURS)
# print("==> TIME_OF_CLOSING_IN_MINUTES:  %s" % TIME_OF_CLOSING_IN_MINUTES)
# print("==> D:  %s" % D)
# print("==> PROFIT:  %s" % PROFIT)
# print("==> PROFIT_ALL_ORDERS:  %s" % PROFIT_ALL_ORDERS)
# print("==> E:  %s" % E)
# print("==> OPENORDERSLIMIT:  %s" % OPENORDERSLIMIT)
# print("==> SINGLEORDERSL:  %s" % SINGLEORDERSL)
# print("==> SINGLEORDERTP:  %s" % SINGLEORDERTP)
# print("==> F:  %s" % F)
# print("==> ARRANGEMENTS_OF_TRADES:  %s" % ARRANGEMENTS_OF_TRADES)
# print("==> G:  %s" % G)
# print("==> LOTS:  %s" % LOTS)
# print("==> SLIPPAGE:  %s" % SLIPPAGE)
# print("==> H:  %s" % H)
# print("==> SET_UP_OF_LOSS:  %s" % SET_UP_OF_LOSS)
# print("==> AMOUNT_OF_LOSS:  %s" % AMOUNT_OF_LOSS)
# print("==> I:  %s" % I)
# print("==> CLOSING_OF_ALL_TRADES:  %s" % CLOSING_OF_ALL_TRADES)
# print("==> J:  %s" % J)
# print("==> USENEWSFILTER:  %s" % USENEWSFILTER)
# print("==> MINSBEFORENEWS:  %s" % MINSBEFORENEWS)
# print("==> MINSAFTERNEWS:  %s" % MINSAFTERNEWS)
# print("==> NEWSIMPACT:  %s" % NEWSIMPACT)
# print("==> K:  %s" % K)
# print("==> FILTERING:  %s" % FILTERING)
# print("==> L:  %s" % L)
# print("==> AUTOEQUITYMANAGER:  %s" % AUTOEQUITYMANAGER)
# print("==> EQUITYGAINPERCENT:  %s" % EQUITYGAINPERCENT)
# print("==> SAFEEQUITYSTOPOUT:  %s" % SAFEEQUITYSTOPOUT)
# print("==> SAFEEQUITYRISK:  %s" % SAFEEQUITYRISK)


