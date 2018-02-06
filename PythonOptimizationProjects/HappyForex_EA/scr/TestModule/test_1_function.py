'''
Created on Jan 31, 2018

@author: cao.vu.lam
'''
import unittest

DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1
MARKET_TIME_STANDARD = '1970.01.01_00:00:00,000'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S,%f'

#===============================================================================
import csv
import os

from os import path, remove

#===============================================================================
def display_an_dict_with_delimiter(dict_out, delimiter):
    ''' Display dictionary with the input delimiter (ex: '=' or ',' or '/' etc.) '''
    
    # display dictionary with iterating over items returning key, value tuples
    for key, value in dict_out.iteritems():  
        print('%s' % str(key) + delimiter + '%s' % str(value))

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
class Test(unittest.TestCase):


    #===========================================================================
    def test_write_value_of_dict2csv_no_header(self):
        print('')
        print('#============================== test_write_value_of_dict2csv_no_header ==============================')
           
        test_dict = {'value1': [10, 20, 20], 'value2': [50, 60, 10], 'value3': [40, 26, 80]}
        print('test_dict =  = {value1: 10, value2: 20, value3: 30}')
           
        # display dictionary with iterating over items returning key, value tuples
        display_an_dict_with_delimiter(test_dict, ':')
   
        file_name_dict = 'myDic_out.csv'
        write_value_of_dict2csv_no_header(test_dict, file_name_dict)
           
                  
        # testing
        file_exist_flag = False
        if os.path.isfile(file_name_dict):
            file_exist_flag = True 
        self.assertTrue(file_exist_flag, "CANNOT write the array to the CSV file.")
           
           
        # testing
        file_size_flag = False
        statinfo = os.stat(file_name_dict)
        if (statinfo.st_size > 0):
            file_size_flag = True
        self.assertTrue(file_size_flag, "CANNOT write any data of the array to the CSV file.")
               
#===============================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
