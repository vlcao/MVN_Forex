'''
Created on Oct 2, 2017

@author: cao.vu.lam
'''
DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1
TIME_STAMP_FORMAT = '%Y.%m.%d_%H.%M.%S.%f'

# import glob
# import csv
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
# def combine_all_files_in_a_folder(folder_name, combined_file_name):    
#     ''' Combine all CSV files in a folder into 1 CSV file only '''
# 
#     # convert the back flash with forward flash (just in case)
#     folder_name = convert_backflash2forwardflash(folder_name)
#     allFiles = glob.glob(folder_name + '/*.csv')
#     
# #     combined_file = []
#     combined_file_name = convert_backflash2forwardflash(combined_file_name)
#     csv_combined_file_write = open(combined_file_name, "w")  # "w" indicates that you're writing strings to the file
#              
#     file_index = DEFAULT_NUMBER
#     for file_ in allFiles:
#         print("==> processing file {0}...".format(file_index))
#         
#         if (file_index % 10 == DEFAULT_NUMBER):
#             perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
#             print("... ==> processing {0}% of the data...".format(perc))
#           
#         # open the CSV file
#         ifile = open(file_, "rU")
#         reader = csv.reader(ifile, delimiter=",")
#           
#         for row in reader:
#             csv_combined_file_write.write(','. join([str(j) for j in row]) + "\n")
#               
#         ifile.close()
#         
#         file_index += DEFAULT_SECOND_NUMBER
#       
#     print("==> Completed {0} files!!!".format(file_index))
# #===============================================================================
# combine_all_files_in_a_folder('E:\EclipsePreferences-csse120-2011-06\Happy Forex\src\DataHandler\data\input\USDJPY\USDJPY_Ticks_May2009_Nov2016_Modified_2',
#                               'E:\EclipsePreferences-csse120-2011-06\Happy Forex\src\DataHandler\data\output\USDJPY\USDJPY_Ticks_May2009_May2010.csv')
# print("Completed!!!")
#
# #===============================================================================
from datetime import datetime
import time
from datetime import date
from DataHandler.hardcoded_data import convert_string_day2float, \
    convert_string_millisecond2float, convert_string_datetime2float

MARKET_TIME_STANDARD = '1970.01.01_00:00:00,000'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S,%f'
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
     
print('#===============================================================================')
hr_min_sec_ms = convert_string_millisecond2float('2009.05.01_04:30:02,624', MARKET_TIME_STANDARD, DATETIME_FORMAT)
print(hr_min_sec_ms)
 
# time = 16202624
milliseconds = hr_min_sec_ms % 1000
print("==> milliseconds = %s" % milliseconds)
 
hr_min_sec = int(hr_min_sec_ms / 1000) 
print("==> hr_min_sec = %s" % hr_min_sec)

hour = int(hr_min_sec / 3600)
print("==> hour = %s" % hour)

minute = int(hr_min_sec % 3600 / 60)
print("==> minute = %s" % minute)
 
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
# #===============================================================================
# from DataHandler.happyforex_Datahandler import DEFAULT_SECOND_NUMBER, \
#     DEFAULT_NUMBER, FOLDER_DATA_INPUT, SYMBOL, \
#     convert_backflash2forwardflash_change_output_folder
# import glob
# import csv
# 
# #===============================================================================
# def create_a_new_row(previous_row, row):
#     ''' Analyze the string separated by Space to get Date and Time '''
#     
#     # --> get the part BEFORE (Date) and AFTER (Time) the Space
#     split_space = previous_row[DEFAULT_SECOND_NUMBER].split(' ')
#     date_part = split_space[DEFAULT_NUMBER]
#     time_part = split_space[DEFAULT_SECOND_NUMBER] 
#     
#     # --> format the date time as expected
#     date_modified_part = (str(date_part[:4]) + '.' + str(date_part[4:6]) + '.' + str(date_part[6:8]) 
#                           + '_' + str(time_part))
#     
#     # --> create a new row for Tick data
#     new_row = (date_modified_part + ',' 
#                + str(previous_row[2]) + ',' 
#                + str(previous_row[3]) + ',' 
#                + str(row[2]) + ',' 
#                + str(row[3]) + '\n')
#     return new_row
# #     return [date_modified_part, previous_row[2], previous_row[3], row[2], row[3]]
# #===============================================================================
# 
# # def load_wholefolder2array():    
# allFiles = glob.glob(FOLDER_DATA_INPUT + SYMBOL + '/USDJPY_Ticks_May2009_Nov2016/*.csv')
# 
# file_index = DEFAULT_NUMBER
# for file_ in allFiles:
#     print("==> processing file {0}...".format(str(file_index)))
#     
#     file_name = str(convert_backflash2forwardflash_change_output_folder(file_))
#      
#     if (file_index % 10 == DEFAULT_NUMBER):
#         perc = round((float(file_index) / float(len(allFiles))) * float(100), 2)
#         print("... ==> processing {0}% of the data...".format(str(perc)))
#       
#     # write an array to a CSV file
#     csv_write = open(str(file_name), "w")  # "w" indicates that you're writing strings to the file
#           
#     # open the CSV file
#     ifile = open(file_, "rU")
#     reader = csv.reader(ifile, delimiter=",")
#     previous_row = reader.next()
#       
#     for row in reader:
#               
#         csv_write.write(create_a_new_row(previous_row, row))
#           
#         # --> save the current row
#         previous_row = row
#           
#     ifile.close()
#   
#     # write the last row
#     last_row = [0, 0, 0, 0]
#     csv_write.write(create_a_new_row(previous_row, last_row))
#   
#     file_index += DEFAULT_SECOND_NUMBER
#       
# print("==> Completed {0} files!!!".format(str(file_index)))


#      
# #====================================================================
# '''
# Shared memory: used only to transfer data from the master to the slaves!
# '''
# import numpy
# import sharedmem
# 
# from multiprocessing import cpu_count
# from multiprocessing import Pool
# 
# default_nprocs = cpu_count()
# 
# def distribute(nitems, nprocs=None):
#     if nprocs is None:
#         nprocs = default_nprocs
#     nitems_per_proc = (nitems + nprocs - 1) / nprocs
#     return [(i, min(nitems, i + nitems_per_proc)) 
#             for i in range(0, nitems, nitems_per_proc)]
# 
# def apply_sqrt(a, imin, imax):
#     a[imin:imax] = numpy.sqrt(a[imin:imax])
# 
# if __name__ == '__main__':
#     pool = Pool()
#     data = sharedmem.empty((100,), numpy.float)
#     data[:] = numpy.arange(len(data))
#     tasks = [pool.apply_async(apply_sqrt, (data, imin, imax))
#              for (imin, imax) in distribute(len(data))]
#     for t in tasks:
#         t.wait()
#     print data
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
