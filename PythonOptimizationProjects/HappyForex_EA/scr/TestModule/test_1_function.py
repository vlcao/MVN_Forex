'''
Created on Jan 31, 2018

@author: cao.vu.lam
'''
import unittest
from StrategyTesterModule.happyforex_ST import HappyForexEA

DEFAULT_NUMBER = 0
DEFAULT_SECOND_NUMBER = 1

AYS_OF_AYEAR = 360
HOURS_OF_ADAY = 24
MINUTES_OF_ANHOUR = 60
SECONDS_OF_AMINUTE = 60
SECONDS_OF_ADAY = 86400
SECONDS_OF_ANHOUR = 3600
MILLISECONDS_OF_ASECOND = 1000

MARKET_TIME_STANDARD = '1970.01.01_00:00:00,000'
DATETIME_FORMAT = '%Y.%m.%d_%H:%M:%S,%f'

#===============================================================================
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
    if (diff_time.seconds == DEFAULT_NUMBER):
        diff_time__milliseconds = float(MILLISECONDS_OF_ASECOND) + float(convert_datetime_milliseconds)
    else:
        diff_time__milliseconds = float(diff_time.seconds * MILLISECONDS_OF_ASECOND) + float(convert_datetime_milliseconds)
    
    return diff_time__milliseconds    

#===============================================================================
class Test(unittest.TestCase):

    #===========================================================================
    def test_convert_string_millisecond2float(self):
        print('')
        print('#============================== test_convert_string_millisecond2float ==============================')
         
        
        convert_datetime = '2018.01.07_00:00:00,46'
        std_datetime = MARKET_TIME_STANDARD
        print('==> date time format = %s' % DATETIME_FORMAT)
        print('==> convert_datetime = %s' % convert_datetime)
        print('==> std_datetime = %s' % std_datetime)
        
        float_milliseconds = convert_string_millisecond2float(convert_datetime, std_datetime, DATETIME_FORMAT)
        print('==> float_milliseconds = %s' % float_milliseconds)
        
        # testing
        defined_milliseconds = 1046.00
        print('==> defined_milliseconds = %s' % defined_milliseconds)
        self.assertEqual(defined_milliseconds - float_milliseconds, float(DEFAULT_NUMBER), "The function IS NOT correct..") 
            
          
#===============================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
