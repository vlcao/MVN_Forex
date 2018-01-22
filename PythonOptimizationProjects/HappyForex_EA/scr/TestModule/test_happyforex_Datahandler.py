'''
Created on Dec 13, 2017

@author: cao.vu.lam
'''
import unittest
from DataHandler.happyforex_Datahandler import *

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        pass

    #===========================================================================
    def test_convert_backflash2forwardflash(self):
            
        # original path with back flash
        print('')
        print('#============================== test_convert_backflash2forwardflash ==============================')
        path_test = os.getcwd()
        print('before convert = %s' % path_test)
            
        backflash_count = DEFAULT_NUMBER
            
        # convert to forward flash
        path_test = convert_backflash2forwardflash(path_test)
        for i in range(len(path_test)):
            if path_test[i] == '\\':
                backflash_count += DEFAULT_SECOND_NUMBER
        print('after convert = %s' % path_test)
            
        # testing
        self.assertEqual(backflash_count, DEFAULT_NUMBER, "Convert NOT Successful.")
           
    #===========================================================================
    def test_float_checker(self):
        print('')
        print('#============================== test_float_checker ==============================')
           
        number = 0.5
           
        float_flag = float_checker(number)
        print('float_checker(%s) = %s' % (number, float_flag))
            
        # testing
        self.assertTrue(float_flag, "This is NOT a float number.")
           
    #===========================================================================
    def test_integer_checker(self):
        print('')
        print('#============================== test_integer_checker ==============================')
           
        number = 2
           
        int_flag = integer_checker(number)
        print('integer_checker(%s) = %s' % (number, int_flag))
            
        # testing
        self.assertTrue(int_flag, "This is NOT a integer number.")
           
    #===========================================================================
    def test_number_after_decimal(self):
        print('')
        print('#============================== test_number_after_decimal ==============================')
           
        number = 20.8807
           
        decimal_num = number_after_decimal(number)
        print('number_after_decimal(%s) = %s' % (number, decimal_num))
          
        # testing
        self.assertEqual(number - 20, decimal_num, "CANNOT get the number after decimal.")
           
    #===========================================================================
    def test_get_subset_dataframe(self):
        print('')
        print('#============================== test_get_subset_dataframe ==============================')
           
        cars = pd.DataFrame({"countryAbbr": ['US', 'AUS', 'JAP', 'IN', 'RU', 'MOR', 'EG'],
                             "cars_per_cap": [809, 731, 588 , 18, 200, 70, 45],
                             "country": ['United States', 'Australia', 'Japan', 'India', 'Russia', 'Morocco', 'Egypt'],
                             "drives_right": [True, False, False, False, True, True, True] })
        cars.index = ['US', 'AUS', 'JAP', 'IN', 'RU', 'MOR', 'EG']
        print('===> original data frame:')
        print(cars)
           
        subtract_list_string = ['AUS', 'JAP', 'RU']
        print('==> subtract_list_string:')
        print(subtract_list_string)
           
        subset_data = get_subset_dataframe(cars, subtract_list_string)
        print('===> get_subset_dataframe:')
        print(subset_data)
          
        # testing
        self.assertEqual(len(subtract_list_string), len(subset_data), "CANNOT get the same number of the required subset.")
           
    #===========================================================================
    def test_write_dic2csv(self):
        print('')
        print('#============================== test_write_dic2csv ==============================')
           
        test_dict = {'value1': 10, 'value2': 20, 'value3': 30}
        print('test_dict =  = {value1: 10, value2: 20, value3: 30}')
           
        # display dictionary with iterating over items returning key, value tuples
        display_an_dict_with_delimiter(test_dict, ':')
   
        file_name_dict = 'myDic_out.csv'
        write_dict2csv_no_header(test_dict, file_name_dict)
           
                  
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
           
    #===========================================================================
    def test_write_array2csv_with_delimiter(self):
        print('')
        print('#============================== test_write_array2csv_with_delimiter ==============================')
           
        myArray = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        print('myArray = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]')
        for i in range(len(myArray)):
            sMyArray = [str(j) for j in myArray[i]]
            print(" " . join(sMyArray))
           
        file_name_history_data = 'myArray_out.csv'
        write_array2csv_with_delimiter_no_header(myArray, file_name_history_data, ',')
           
                  
        # testing
        file_exist_flag = False
        if os.path.isfile(file_name_history_data):
            file_exist_flag = True 
        self.assertTrue(file_exist_flag, "CANNOT write the array to the CSV file.")
           
           
        # testing
        file_size_flag = False
        statinfo = os.stat(file_name_history_data)
        if (statinfo.st_size > DEFAULT_NUMBER):
            file_size_flag = True
        self.assertTrue(file_size_flag, "CANNOT write any data of the array to the CSV file.")
           
    #===========================================================================
    def test_copy_string_array(self):
        print('')
        print('#============================== test_copy_string_array ==============================')
           
        myArray = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        print('myArray = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]')
        for i in range(len(myArray)):
            sMyArray = [str(j) for j in myArray[i]]
            print(" " . join(sMyArray))
           
        new_array = copy_string_array(myArray)
        same_content_flag = True 
        print('new_array[] = ')
        for i in range(len(new_array)):
            sMyArray = [str(j) for j in myArray[i]]
            print(" " . join(sMyArray))
               
            for j in range(len(new_array[i])):
                if str(new_array[i][j]) != str(myArray[i][j]):
                    same_content_flag = False
                       
                  
        # testing
        self.assertEqual(len(myArray), len(new_array),
                         "The new array DOESN'T have the same rows with the source array.")
        self.assertEqual(len(myArray[DEFAULT_NUMBER]), len(new_array[DEFAULT_NUMBER]),
                         "The new array DOESN'T have the same columns with the source array.")
        self.assertTrue(same_content_flag,
                         "The new array DOESN'T have the same content with the source array.")
           
   
    #===========================================================================
    def test_permutation_count(self):
        print('')
        print('#============================== test_permutation_count ==============================')
           
        letters = 3
        digits = 2
                   
        perm = permutation_count(letters, digits)
        print('letters=%s, digits=%s ==> permutation_count(%s,%s) = %s' % (letters, digits, letters, digits, perm)
              + ' ==> Ex: permutations of 123 for 2 digits are 12, 13, 21, 23, 31, 32.')
            
        # testing
        predefine_perm = 6
        self.assertEqual(predefine_perm, perm, "The permutation function is NOT successful.")
           
    #===========================================================================
    def test_combination_count(self):
        print('')
        print('#============================== test_combination_count ==============================')
           
        letters = 3
        digits = 2
                   
        com = combination_count(letters, digits)
        print('letters=%s, digits=%s ==> combination_count(%s,%s) = %s' % (letters, digits, letters, digits, com)
              + ' ==> Ex: combinations of 123 for 2 digits are 12, 13, 23.')
            
        # testing
        predefine_com = 3
        self.assertEqual(predefine_com, com, "The combination function is NOT successful.")
          
    #===========================================================================
    def test_merge_2parametes_array_data(self):
        print('')
        print('#============================== test_merge_2parametes_array_data ==============================')
          
        myOldArray = [[1, 2], [4, 5], [7, 8]]
        print("==> myOldArray: " % myOldArray)
        display_an_array_with_delimiter(myOldArray, ' ')
          
        myNewArray = [[1, 3], [4, 9]]
        print("==> myNewArray: " % myNewArray)
        display_an_array_with_delimiter(myNewArray, ' ')
           
        myReplacedArray = merge_2parametes_array_data(myOldArray, myNewArray)
        print("==> myReplacedArray: " % myReplacedArray)
        display_an_array_with_delimiter(myReplacedArray, ' ')
          
        # testing
        predefine_length = 3 
        self.assertEqual(predefine_length, len(myReplacedArray), "The size of the Replaced array is NOT correct.")
  
    #===========================================================================
    def test_point_of_symbol(self):
        print('')
        print('#============================== test_point_of_symbol ==============================')
           
        number = 1.17687
        predefined_point = 1e-05
          
        point = point_of_symbol(number)
        print('point_of_symbol(%s) = %s' % (number, point))
          
        # testing
        self.assertEqual(predefined_point, point, "CANNOT get the point of the number.")
 
    #===========================================================================
    def test_digit_of_symbol(self):
        print('')
        print('#============================== test_digit_of_symbol ==============================')
          
        number = 0.4875
        predefined_digit = int(4)
          
        digit = digit_of_symbol(number)
        print('digit_of_symbol(%s) = %s' % (number, digit))
         
        # testing
        self.assertEqual(predefined_digit, digit, "CANNOT get the digit of the number.")
         
    #===========================================================================
    def test_is_time_earlier(self):
        print('')
        print('#============================== test_is_time_earlier ==============================')
         
        
        sformat = '%Y.%m.%d_%H:%M:%S'
        sdatetime_1 = '2018.01.07_11:22:12'
        sdatetime_2 = '2017.01.08_11:22:13'
        print('==> date time format = %s' % sformat)
        print('==> sdatetime_1 = %s' % sdatetime_1)
        print('==> sdatetime_2 = %s' % sdatetime_2)
        
        flag_early_date = is_time_earlier(sdatetime_1, sdatetime_2, MARKET_TIME_STANDARD, sformat)
        
        # testing
        self.assertFalse(flag_early_date, "The function IS NOT correct..") 
    
    #===========================================================================
    def test_convert_string_datetime2integer(self):
        print('')
        print('#============================== test_convert_string_datetime2integer ==============================')
         
        
        sformat = '%Y.%m.%d_%H:%M:%S'
        convert_datetime = '2018.01.07_11:22:12'
        std_datetime = MARKET_TIME_STANDARD
        print('==> date time format = %s' % sformat)
        print('==> convert_datetime = %s' % convert_datetime)
        print('==> std_datetime = %s' % std_datetime)
        
        int_datetime = convert_string_datetime2float(convert_datetime, std_datetime, sformat)
        print('==> int_datetime = %s' % int_datetime)
        
        # testing
        defined_int_datetime = 58470
        print('==> defined_int_datetime = %s' % defined_int_datetime)
        self.assertEqual(defined_int_datetime, int_datetime, "The function IS NOT correct..") 
            

#===========================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
#===============================================================================
