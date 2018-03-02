'''
Created on Jan 31, 2018

@author: cao.vu.lam
'''
import unittest

DEFAULT_NUMBER_INT = 0
DEFAULT_SECOND_NUMBER_INT = 1

AYS_OF_AYEAR = 360
HOURS_OF_ADAY = 24
MINUTES_OF_ANHOUR = 60
SECONDS_OF_AMINUTE = 60
SECONDS_OF_ADAY = 86400
SECONDS_OF_ANHOUR = 3600
MILLISECONDS_OF_ASECOND = 1000

MARKET_TIME_STANDARD = '1970.01.01_00:00:00'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S'
DATEOFFSET = 719163  # total days from '0001.01.01_00:00:00,000' to '1970.01.01_00:00:00,000' (MARKET_TIME_STANDARD)

import csv
import os
from os import path, remove

DATETIME_COL_INDEX = 0
DAY_COL_INDEX = 1
TIME_COL_INDEX = 2

from datetime import date


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
def convert_datetime_back_whole_list(file_name_out):
    ''' Convert back Date Time from float to normal format. '''
    
    # load data from input file
    data_converted = load_csv2array(file_name_out)
    display_an_array_with_delimiter(data_converted, ',')
    
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
        hour_minute_second = int(data_converted[i][TIME_COL_INDEX]) 
        
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
class Test(unittest.TestCase):

    #===========================================================================
    def test_convert_datetime_back_whole_list(self):
        print('')
        print('#============================== test_convert_datetime_back_whole_list ==============================')
        
        # convert back the Date Time for output file
        file_name_out = 'datetime_converted_testdata.csv'
        data_converted = convert_datetime_back_whole_list(file_name_out)
        display_an_array_with_delimiter(data_converted, ',    ')
        
        # create a new file name
        new_file_name_out = file_name_out.replace('.csv', '_dattime_converted.csv')
        write_array2csv_with_delimiter_no_header(data_converted, new_file_name_out, ',')
        
        '''
        2005.01.03_01:48:05,    2005.01.03,    01:48:05,    102.54,    102.58
        2005.01.03_01:53:42,    2005.01.03,    01:53:42,    102.54,    102.58
        '''
        
        # testing
        datetime_converted = data_converted[DEFAULT_NUMBER_INT][DATETIME_COL_INDEX]
        print('==> datetime_converted = %s' % datetime_converted)
        
        defined_datetime_coverted = '2005.01.03_01:48:05'
        print('==> defined_datetime_coverted = %s' % defined_datetime_coverted)
        
        if (datetime_converted == defined_datetime_coverted):
            flag_datetime = True
        else:
            flag_datetime = False
            
        self.assertTrue(flag_datetime, "The function IS NOT correct..") 
       
          
#===============================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
