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
import glob
import shutil
import sys

from os import path, remove
from datetime import date

DATETIME_COL_INDEX = 0
DAY_COL_INDEX = 1
TIME_COL_INDEX = 2

SCR_DIR_PATH = os.path.dirname(os.getcwd())
FOLDER_DATA_OUTPUT = SCR_DIR_PATH + '/DataHandler/data/output/'
SYMBOL = 'EURUSD'
FILENAME_ORDER_CLOSED_HISTORY = 'order_closed_history.csv'


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
class Test(unittest.TestCase):

    #===============================================================================
    def test_combine_all_files_in_a_folder(self):
            print('')
            print('#============================== test_combine_all_files_in_a_folder ==============================')
            
            # Create an folder for storing all outputs in this section 
            symbol_folder_output = FOLDER_DATA_OUTPUT + SYMBOL
#             if os.path.exists(symbol_folder_output):
#                 shutil.rmtree(symbol_folder_output)
#             os.makedirs(symbol_folder_output)
            
            folder_output = symbol_folder_output + '/ind_1_outputs/'
#             if os.path.exists(folder_output):
#                 shutil.rmtree(folder_output)
#             os.makedirs(folder_output)
            
            # write out other data for reference
            file_name_out = symbol_folder_output + '/' + SYMBOL + '_ind_1_$84274.64_' + FILENAME_ORDER_CLOSED_HISTORY
            combine_all_files_in_a_folder(folder_output, file_name_out,
                                          '*_' + FILENAME_ORDER_CLOSED_HISTORY)
            
            # convert back the Date Time for output file
            converted_data = convert_datetime_back_whole_list(file_name_out)
            
            # create a new file name
            write_array2csv_with_delimiter_no_header(converted_data, file_name_out, ',')
            
            # testing
            file_exist_flag = False
            if os.path.isfile(file_name_out):
                file_exist_flag = True 
            self.assertTrue(file_exist_flag, "CANNOT write the array to the CSV file.")
               
            # testing
            file_size_flag = False
            statinfo = os.stat(file_name_out)
            if (statinfo.st_size > 0):
                file_size_flag = True
            self.assertTrue(file_size_flag, "CANNOT write any data of the array to the CSV file.")
    
          
#===============================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
