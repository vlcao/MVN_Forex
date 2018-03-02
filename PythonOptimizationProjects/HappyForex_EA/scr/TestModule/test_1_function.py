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

from decimal import Decimal


#===============================================================================
def float_checker(number):
     
    flag_float = isinstance(number, float)  # returns True if it's a float
     
    if (flag_float == False):
        print('This is NOT a float number')
         
    return flag_float


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
class Test(unittest.TestCase):

    #===========================================================================
    def test_point_of_symbol(self):
        print('')
        print('#============================== test_point_of_symbol ==============================')
           
        number = 107.544
        predefined_point = 1e-05
          
        point = point_of_symbol(number)
        print('point_of_symbol(%s) = %s' % (number, point))
          
        # testing
        self.assertEqual(predefined_point, point, "CANNOT get the point of the number.")
       
          
#===============================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
