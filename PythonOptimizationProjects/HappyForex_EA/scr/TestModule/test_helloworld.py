'''
Created on Oct 2, 2017

@author: cao.vu.lam
'''
#===============================================================================
def display_an_array_with_delimiter(array_out, delimiter):
    out_length = len(array_out)
    
    if out_length <= 100:
        for i in range(out_length):
            sMyArray = [str(j) for j in array_out[i]]
            print(delimiter . join(sMyArray))
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
        print('[%s rows x %s columns]' % (out_length, len(array_out[0])))
        
#====================================================================
def create_a_new_row(previous_row, row):
    ''' Analyze the string separated by Space to get Date and Time '''
    
    # --> get the part BEFORE (Date) and AFTER (Time) the Space
    split_space = previous_row[DEFAULT_SECOND_NUMBER].split(' ')
    date_part = split_space[DEFAULT_NUMBER]
    time_part = split_space[DEFAULT_SECOND_NUMBER] 
    
    # --> format the date time as expected
    date_modified_part = (str(date_part[:4]) + ':' + str(date_part[4:6]) + ':' + str(date_part[6:8]) 
                          + '_' + str(time_part))
    
    # --> create a new row for Tick data
    return [date_modified_part, previous_row[2], previous_row[3], row[2], row[3]]

#====================================================================
import glob
import csv
import os

DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S.%f'
DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1

folder_name = os.path.dirname(os.getcwd()) + "/DataHandler/data/input/USDJPY_Ticks_May2009_Nov2016"  # use your path
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
    
display_an_array_with_delimiter(list_, ',')



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
