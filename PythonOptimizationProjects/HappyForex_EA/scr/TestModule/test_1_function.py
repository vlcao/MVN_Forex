'''
Created on Jan 31, 2018

@author: cao.vu.lam
'''
import unittest
from EAModule.happyforex_EA import HappyForexEA
from DataHandler.hardcoded_data import convert_string_millisecond2float

DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1
MARKET_TIME_STANDARD = '1970.01.01_00:00:00,000'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S,%f'

#===============================================================================
import _strptime
from datetime import datetime

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
class Test(unittest.TestCase):


    #===========================================================================
    def test_TimeMinute_3(self):
        print('#============================== test_TimeMinute_3 ==============================')
      
        happyforex_EA_instance = HappyForexEA()
        
        Time_04_30 = convert_string_millisecond2float('2009.05.01_06:30:02,624', MARKET_TIME_STANDARD, DATETIME_FORMAT)
        happyforex_EA_instance.current_time = Time_04_30
        print("==> Time_04_30 in numbers = %s" % Time_04_30)
        
        
        test_minute_tick = happyforex_EA_instance.TimeMinute_3()
        print("==> test_minute_tick: %s" % test_minute_tick)
           
        # testing
        defined_minute_tick = 30
        print("==> defined_minute_tick: %s" % defined_minute_tick)
           
        self.assertEquals(defined_minute_tick, test_minute_tick , "Function IS NOT correct.")
        
#===============================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
