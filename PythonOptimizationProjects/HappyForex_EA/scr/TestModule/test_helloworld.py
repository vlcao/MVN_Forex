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


# #===============================================================================
# ''' suppress scientific notation '''
# a = 1.515324132e+12
# print('%f' % a)
# print('%.2f' % a)
# 
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


# --> format the date time as expected WITHOUT millisecond
MARKET_TIME_STANDARD = '1970.01.01_00:00:00'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S'
create_multiple_calendar_data_from_wholefolder_forexfactory_format(os.path.dirname(os.getcwd()) 
                                                              + '/DataHandler/data/input/economic_calendar_01Jan2007_18Apr2014_original')

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
