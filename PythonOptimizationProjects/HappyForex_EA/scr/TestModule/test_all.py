'''
Created on Dec 13, 2017

@author: cao.vu.lam
'''
import unittest
import os
import pandas as pd

from StrategyTesterModule.happyforex_ST import HappyForexEA
from DataHandler.hardcoded_data import DEFAULT_NUMBER_INT, DEFAULT_SECOND_NUMBER_INT, \
    OP_BUY, OP_BUYLIMIT, MARKET_TIME_STANDARD, DATETIME_FORMAT, LOTS_COL_INDEX, \
    DATETIME_COL_INDEX, OP_SELL, PROFIT_COL_INDEX, ORDER_TYPE_COL_INDEX, \
    convert_backflash2forwardflash, number_after_decimal, display_an_dict_with_delimiter, float_checker, \
    integer_checker, get_subset_dataframe, write_wholedict2csv_no_header, \
    write_array2csv_with_delimiter_no_header, copy_string_array, \
    permutation_count, combination_count, display_an_array_with_delimiter, \
    merge_2parametes_array_data, point_of_symbol, digit_of_symbol, \
    is_time_earlier, convert_string_datetime2float_no_ms, convert_string_day2float, \
    convert_string_millisecond2float, write_value_of_dict2csv_no_header, \
    convert_string_second2float 

happyforex_EA_instance = HappyForexEA()

# class TestHappyForex_GA(unittest.TestCase):
# 
# 
#         #===========================================================================
#         def test_create_random_genes(self):
#             print('#============================== test_create_random_genes ==============================')
#             individual = Individual()
#             individual.create_random_genes()
#             display_an_array_with_delimiter(individual.genes, '=')
#               
#             # testing
#             predefine_len = len(OPTIMIZE_PARAMETERS_LIST)
#             print("==> predefine_len of OPTIMIZE_PARAMETERS_LIST: %s" % predefine_len)
#             self.assertEqual(predefine_len, len(individual.genes), "The new array DOESN'T have the same rows with the source array.")
#          
#         #===========================================================================
#         def test_create_uniqueID(self):
#             print('#============================== test_create_uniqueID ==============================')
#             individual = Individual()
#              
#             # testing
#             dictionary_IDlist = {}
#             individual.create_uniqueID(dictionary_IDlist)
#              
#             flag_individualID = False
#             if individual.individual_ID != DEFAULT_NUMBER_INT:
#                 flag_individualID = True
#              
#             self.assertTrue(flag_individualID, "CANNOT create an individual.")
#              
#         #===========================================================================
#         def test_cal_fitness(self):
#             print('#============================== test_cal_fitness ==============================')
#             individual = Individual()
#              
#             happyforex_EA_instance.net_profit = 123
#             happyforex_EA_instance.total_win = 30.15
#             '''
#             50 * (self.net_profit / NET_PROFIT 
#                              + self.total_win / MAX_WIN_TOTAL_TRADE)
#             '''
#              
#             # testing
#             individual.cal_fitness()
#             print("==> individual.fitness: %s" % individual.fitness)
#             predefinded_fitness = 67.08
#             print("==> predefinded_fitness: %s" % predefinded_fitness)
#              
#             self.assertEqual(predefinded_fitness, individual.fitness, "The cal_fitness ISNOT correct.")
#         
#         #===========================================================================
#         def test_create_manual_genes(self):
#             print('#============================== test_create_manual_genes ==============================')
#            
#             manual_parameters_list = ['1', '1', '3', '1', '6', '12', '-25', '0.01']
#             print("==> manual_parameters_list = ['1', '1', '3', '1', '6', '12', '-25', '0.01']")
#             
#             individual = Individual()
#             individual.create_manual_genes(manual_parameters_list)
#             display_an_array_with_delimiter(individual.genes, '=')
#               
#             # testing
#             count = DEFAULT_NUMBER_INT
#             flag_item = False
#             for item in manual_parameters_list:
#                 if item[count] == individual.genes[count][1]:
#                     flag_item = True
#                      
#             self.assertTrue(flag_item, "CANNOT create genes manually.")
#         
#         #===========================================================================
#         def test_flip_value(self):
#             print('#============================== test_flip_value ==============================')
#             individual = Individual()
#             individual.create_random_genes()
#              
#             manual_parameters_list = ['1', '1', '3', '0', '6', '12', '-25', '0.01']
#             print("==> manual_parameters_list = ['1', '1', '3', '0', '6', '12', '-25', '0.01']")
#             
#             
#             individual = Individual()
#             individual.create_manual_genes(manual_parameters_list)
#             dictionary_IDlist = {}
#             individual.create_uniqueID(dictionary_IDlist)
#  
#             print('===========================================================================')
#             print("==> individual[genes] BEFORE flip:")
#             display_an_array_with_delimiter(individual.genes, '=')
#             
#             # Flip value at the mutation_point
#             mutation_point = predefine_flip_value = DEFAULT_NUMBER_INT
#             print("==> mutation_point = %s" % mutation_point)
#             individual.flip_value(mutation_point)
#             
#             print('===========================================================================')
#             print("==> individual[genes] AFTER flip:")
#             display_an_array_with_delimiter(individual.genes, '=')
#             
#             
#             # testing
#             count = DEFAULT_NUMBER_INT
#             flag_item = False
#             if individual.genes[count][1] == str(predefine_flip_value):
#                 flag_item = True
#                      
#             self.assertTrue(flag_item, "CANNOT flip value.")
#             
#             
#             # Flip value at the mutation_point
#             mutation_point = 3
#             print("==> mutation_point = %s" % mutation_point)
#             individual.flip_value(mutation_point)
#             
#             print('===========================================================================')
#             print("==> individual[genes] AFTER flip:")
#             display_an_array_with_delimiter(individual.genes, '=')
#             
#             
#             # testing
#             count = 3
#             predefine_flip_value = '1'
#             flag_item = False
#             if individual.genes[count][1] == str(predefine_flip_value):
#                 flag_item = True
#                      
#             self.assertTrue(flag_item, "CANNOT flip value.")


################################################################################
##########################           CLASS           ###########################
################################################################################
class TestHappyForex_ST(unittest.TestCase):

    #===========================================================================
    def testName(self):
        pass
    
    #===========================================================================
    def test_OrderDelete_4(self):
        print('#============================== test_OrderDelete_4 ==============================')
      
        HEADER_ORDER_DICT = ['Date_Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']

        ORDER_TOTAL_DICT = {}
        ORDER_TOTAL_DICT[123456] = HEADER_ORDER_DICT
        ORDER_TOTAL_DICT[123457] = HEADER_ORDER_DICT
        ORDER_TOTAL_DICT[123458] = HEADER_ORDER_DICT
        ORDER_TOTAL_DICT[123459] = HEADER_ORDER_DICT
        ORDER_TOTAL_DICT[123460] = HEADER_ORDER_DICT
        ORDER_TOTAL_DICT[123461] = HEADER_ORDER_DICT
        print("==> length of dictionary before deleting 1 item: %s" % len(ORDER_TOTAL_DICT))
        
        flag_delete = (123458 in ORDER_TOTAL_DICT)
        print("==> flag_delete: %s" % flag_delete)
        
        # execute the function
        happyforex_EA_instance.OrderDelete_4(123458, ORDER_TOTAL_DICT)
        print("==> new length of dictionary after deleting 1 item: %s" % len(ORDER_TOTAL_DICT))
         
        # testing
        defined_new_len = 5
        print("==> defined_new_len: %s" % defined_new_len)
         
        self.assertEquals(defined_new_len, len(ORDER_TOTAL_DICT), "Function IS NOT correct.")

        # testing
        flag_delete = (123458 in ORDER_TOTAL_DICT)
        print("==> flag_delete: %s" % flag_delete)
        
        self.assertFalse(flag_delete, "Function IS NOT correct.")

    #===========================================================================
    def test_DeletePendingOrder19_3(self):
        print('#============================== test_DeletePendingOrder19_3 ==============================')
      
        # HEADER_ORDER_DICT = ['Date_Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']
        for key in happyforex_EA_instance.ORDER_OPENED_DICT.keys():
            del happyforex_EA_instance.ORDER_OPENED_DICT[key]
            
        happyforex_EA_instance.ORDER_OPENED_DICT[0] = [1106359662.0, 12805.0, 7662.0, 2.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 209.25, 0]
        happyforex_EA_instance.ORDER_OPENED_DICT[1] = [1106359662.0, 12805.0, 7662.0, 3.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 209.25, 0]
        happyforex_EA_instance.ORDER_OPENED_DICT[1] = [1106359662.0, 12805.0, 7662.0, 1.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 209.25, 0]
        display_an_dict_with_delimiter(happyforex_EA_instance.ORDER_OPENED_DICT, '    ')
        print("==> length of dictionary before function DeletePendingOrder19_3: %s" % len(happyforex_EA_instance.ORDER_OPENED_DICT))
        
        # execute the function DeletePendingOrder19_3 ==> delete OP_SELLLIMIT = 3.00
        happyforex_EA_instance.DeletePendingOrder19_3()
        print("==> new length of dictionary after function DeletePendingOrder19_3: %s" % len(happyforex_EA_instance.ORDER_OPENED_DICT))
         
        # testing
        defined_new_len = 2
        print("==> defined_new_len: %s" % defined_new_len)
         
        self.assertEquals(defined_new_len, len(happyforex_EA_instance.ORDER_OPENED_DICT), "Function IS NOT correct.")

    #===========================================================================
    def test_OrderAdd_4(self):
        print('#============================== test_OrderAdd_4 ==============================')
      
        HEADER_ORDER_DICT = ['Date_Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']

        ORDER_DICT = {}
        ORDER_DICT[123456] = HEADER_ORDER_DICT
        ORDER_DICT[123457] = HEADER_ORDER_DICT
        print("==> length of dictionary before deleting 1 item: %s" % len(ORDER_DICT))
        
        flag_add = (123458 in ORDER_DICT)
        print("==> flag_add: %s" % flag_add)
        
        # execute the function
        happyforex_EA_instance.OrderAdd_10(123458, HEADER_ORDER_DICT, ORDER_DICT)
        print("==> new length of dictionary after deleting 1 item: %s" % len(ORDER_DICT))
         
        # testing
        defined_new_len = 3
        print("==> defined_new_len: %s" % defined_new_len)
         
        self.assertEquals(defined_new_len, len(ORDER_DICT), "Function IS NOT correct.")

        # testing
        flag_add = (123458 in ORDER_DICT)
        print("==> flag_add: %s" % flag_add)
        
        self.assertTrue(flag_add, "Function IS NOT correct.")

    #===========================================================================
    def test_ProfitCheck_3(self):
        print('#============================== test_ProfitCheck_3 ==============================')
        
        happyforex_EA_instance.CurrentProfit = 320.15
        
        for key in happyforex_EA_instance.ORDER_CLOSED_DICT.keys():
            del happyforex_EA_instance.ORDER_CLOSED_DICT[key]
        
        for key in happyforex_EA_instance.ORDER_OPENED_DICT.keys():
            del happyforex_EA_instance.ORDER_OPENED_DICT[key]
        
        happyforex_EA_instance.ORDER_OPENED_DICT[123.00] = [1106359662.0, 12805.0, 7662.0, 1.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 209.25, 0]
        happyforex_EA_instance.ORDER_OPENED_DICT[456.00] = [1105920071.0, 12800.0, 71.0, 0.0, 1105920129.0, 0.01, 101.98, 102.14, 0.0, 0.0, 159.25, 0]
         
        CurrentProfit = happyforex_EA_instance.ProfitCheck_3()
        print("==> CurrentProfit: %s" % CurrentProfit)
           
        # testing
        defined_CurrentProfit = 320.15
        print("==> defined_CurrentProfit: %s" % defined_CurrentProfit)
           
        self.assertEquals(defined_CurrentProfit - CurrentProfit, float(DEFAULT_NUMBER_INT) ,
                          "Function IS NOT correct.")
          
    #===========================================================================
    def test_BrokerIs5Digit_0(self):
        print('#============================== test_BrokerIs5Digit_0 ==============================')
        
        happyforex_EA_instance.NDigits = 5
        print("==> DIGITS: %s" % happyforex_EA_instance.NDigits)
           
        flag_5Digit = happyforex_EA_instance.BrokerIs5Digit_0() 
        print(flag_5Digit)
           
        # testing
        self.assertTrue(flag_5Digit, "Function IS NOT correct.")

    #===========================================================================
    def test_AccountBalance_1(self):
        print('#============================== test_AccountBalance_1 ==============================')
        
        happyforex_EA_instance.balance = 112000.00
        
        for key in happyforex_EA_instance.ORDER_CLOSED_DICT.keys():
            del happyforex_EA_instance.ORDER_CLOSED_DICT[key]
        
        for key in happyforex_EA_instance.ORDER_OPENED_DICT.keys():
            del happyforex_EA_instance.ORDER_OPENED_DICT[key]
        
        # HEADER_ORDER_DICT: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
        happyforex_EA_instance.ORDER_CLOSED_DICT[123.00] = [1106359662.0, 12805.0, 7662.0, 1.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 209.25, 111475.75]
         
        balance = happyforex_EA_instance.AccountBalance_1()
        print("==> happyforex_EA_instance.balance: %s" % balance)
           
        # testing
        defined_balance = 112000.00
        print("==> defined_balance: %s" % defined_balance)
           
        self.assertEquals(defined_balance - balance, float(DEFAULT_NUMBER_INT) ,
                          "Function IS NOT correct.")

    #===========================================================================
    def test_OrderType_5(self):
        print('#============================== test_OrderType_5 ==============================')
        
        TEST_DICT = {}
        TEST_DICT_SND = {}
        
        # testing
        order_type = happyforex_EA_instance.OrderType_5(DEFAULT_NUMBER_INT, TEST_DICT)
        print("==> order_type: %s" % order_type)
           
        defined_order_type = -1.00
        print("==> defined_order_type: %s" % defined_order_type)
          
        # HEADER_ORDER_CLOSED_HISTORY = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
        TEST_DICT[DEFAULT_NUMBER_INT] = [1106359662.0, 12805.0, 7662.0, 1.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 209.25, 111475.75]
        TEST_DICT_SND[DEFAULT_NUMBER_INT] = [1105920071.0, 12800.0, 71.0, 0.0, 1105920129.0, 0.01, 101.98, 102.14, 0.0, 0.0, 159.25, 108756.25]
           
        # testing
        order_type = happyforex_EA_instance.OrderType_5(DEFAULT_NUMBER_INT, TEST_DICT)
        print("==> order_type: %s" % order_type)
           
        defined_order_type = 1.00
        print("==> defined_order_type: %s" % defined_order_type)
           
        self.assertEquals(defined_order_type, order_type, "Function IS NOT correct.")
       
        # testing
        order_type = happyforex_EA_instance.OrderType_5(DEFAULT_NUMBER_INT, TEST_DICT_SND)
        print("==> order_type: %s" % order_type)
           
        defined_order_type = 0.00
        print("==> defined_order_type: %s" % defined_order_type)
           
        self.assertEquals(defined_order_type, order_type, "Function IS NOT correct.")

    #===========================================================================
    def test_MaxOrders_9(self):
        print('#============================== test_MaxOrders_9 ==============================')
        
        happyforex_EA_instance.USE_ORDERSLIMIT = True
        
        for key in happyforex_EA_instance.ORDER_CLOSED_DICT.keys():
            del happyforex_EA_instance.ORDER_CLOSED_DICT[key]
        
        for key in happyforex_EA_instance.ORDER_OPENED_DICT.keys():
            del happyforex_EA_instance.ORDER_OPENED_DICT[key]
        
        happyforex_EA_instance.ords_in_a_day = 2
        print("==> happyforex_EA_instance.ords_in_a_day: %s" % happyforex_EA_instance.ords_in_a_day)
        
        # HEADER_ORDER_CLOSED_HISTORY = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
        happyforex_EA_instance.ORDER_OPENED_DICT[123.00] = [1106359662.0, 12805.0, 7662.0, 2.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 209.25, 0]
        print('happyforex_EA_instance.ORDER_OPENED_DICT')
        display_an_dict_with_delimiter(happyforex_EA_instance.ORDER_OPENED_DICT, ' ')
           
        # testing
        orderLimit = 2
        flag_orderLimit = happyforex_EA_instance.MaxOrders_9(orderLimit)
        print("==> orderLimit: %s" % orderLimit)
        print("==> happyforex_EA_instance.MaxOrders_9(orderLimit): %s" % flag_orderLimit)
           
        self.assertTrue(flag_orderLimit, "Function IS NOT correct.")
        print('#============================== end test 1 ==============================')
        
        # testing
        defined_num_of_opened_oder = DEFAULT_NUMBER_INT
        print("==> defined_num_of_opened_oder: %s" % defined_num_of_opened_oder)
        print("==> num_of_opened_oder: %s" % len(happyforex_EA_instance.ORDER_OPENED_DICT))
        print('happyforex_EA_instance.ORDER_OPENED_DICT')
        display_an_dict_with_delimiter(happyforex_EA_instance.ORDER_OPENED_DICT, ' ')
        
        self.assertEquals(defined_num_of_opened_oder, len(happyforex_EA_instance.ORDER_OPENED_DICT),
                          "Function IS NOT correct.")                               
        print('#============================== end test 2 ==============================')
        
        # testing
        orderLimit = 4
        flag_orderLimit = happyforex_EA_instance.MaxOrders_9(orderLimit)
        print("==> happyforex_EA_instance.MaxOrders_9(orderLimit): %s" % flag_orderLimit)
           
        self.assertFalse(happyforex_EA_instance.MaxOrders_9(orderLimit), "Function IS NOT correct.")
        print('#============================== end test 3 ==============================')
        
    #===========================================================================
    def test_MathMax_6(self):
        print('#============================== test_MathMax_6 ==============================')
        
        float_num_1 = 1.00
        float_num_2 = 5.35
        
        max_num = happyforex_EA_instance.MathMax_6(float_num_1, float_num_2)
        print("==> max_num: %s" % max_num)
        
        define_max_num = float_num_2
        print("==> define_max_num: %s" % define_max_num)
        
        # testing
        self.assertEquals(define_max_num, max_num, "Function IS NOT correct.")
        
    #===========================================================================
    def test_CreateUniqueOrderID_9(self):
        print('#============================== test_CreateUniqueOrderID_9 ==============================')
        
        # create the unique order ID which is the combination of all Values of parameters
        happyforex_EA_instance.current_date = '2018.01.17'
        happyforex_EA_instance.current_time = '09:21:00'
        happyforex_EA_instance.ords_in_a_day = 2
        print("==> happyforex_EA_instance.current_datetime: %s" % happyforex_EA_instance.current_datetime)
        
        new_id = happyforex_EA_instance.CreateUniqueOrderID_9(OP_BUY)
        print("==> new_id: %s" % new_id)
        
        # testing
        if (new_id > float(DEFAULT_NUMBER_INT)):
            flag_created = True
        else:
            flag_created = False
            
        self.assertTrue(flag_created, "Function IS NOT correct.")
        
    #===========================================================================
    def test_NormalizeDouble_9(self):
        print('#============================== test_NormalizeDouble_9 ==============================')
        
        float_num = 4.5687946
        digit_num = 2
        print("==> float_num: %s" % float_num)
        print("==> digit_num: %s" % digit_num)
        
        normalized_num = happyforex_EA_instance.NormalizeDouble_9(float_num, digit_num)
        print("==> normalized_num: %s" % normalized_num)
        print("==> float_checker(normalized_num): %s" % float_checker(normalized_num))
        
        # testing
        define_normalized_num = 4.5699999
        print("==> define_normalized_num: %s" % define_normalized_num)
        self.assertEquals(define_normalized_num - normalized_num, float(DEFAULT_NUMBER_INT), "Function IS NOT correct.")
        print('#============================== end test 1 ==============================')
        
        digit_num = 0
        print("==> float_num: %s" % float_num)
        print("==> digit_num: %s" % digit_num)
        
        normalized_num = happyforex_EA_instance.NormalizeDouble_9(float_num, digit_num)
        print("==> normalized_num: %s" % normalized_num)
        print("==> float_checker(normalized_num): %s" % float_checker(normalized_num))
        
        # testing
        define_normalized_num = 4.0000000
        print("==> define_normalized_num: %s" % define_normalized_num)
        self.assertEquals(define_normalized_num - normalized_num, float(DEFAULT_NUMBER_INT), "Function IS NOT correct.")
        print('#============================== end test 2 ==============================')

    #===========================================================================
    def test_BuyPendingOrder13_8(self):
        print('#============================== test_BuyPendingOrder13_8 ==============================')
    
        happyforex_EA_instance.bid_price = 1.35226
        happyforex_EA_instance.ask_price = 1.35251
        happyforex_EA_instance.ords_in_a_day = 1
        
        for key in happyforex_EA_instance.ORDER_OPENED_DICT.keys():
            del happyforex_EA_instance.ORDER_OPENED_DICT[key] 
        
        for key in happyforex_EA_instance.ORDER_CLOSED_DICT.keys():
            del happyforex_EA_instance.ORDER_CLOSED_DICT[key] 
        
        happyforex_EA_instance.BuyPendingOrder13_8()
        
        # testing
        defined_length_of_ORDER_OPENED_DICT = 1
        print("==> defined_length_of_ORDER_OPENED_DICT: %s" % defined_length_of_ORDER_OPENED_DICT)
        print("==> length of ORDER_OPENED_DICT: %s" % len(happyforex_EA_instance.ORDER_OPENED_DICT))
        display_an_dict_with_delimiter(happyforex_EA_instance.ORDER_OPENED_DICT, '    ')
        
        self.assertEqual(defined_length_of_ORDER_OPENED_DICT, len(happyforex_EA_instance.ORDER_OPENED_DICT),
                         "Function IS NOT correct.")
    
    #===========================================================================
    def test_ModifyPendingOrder_2(self):
        print('#============================== test_ModifyPendingOrder_2 ==============================')
        
        for key in happyforex_EA_instance.ORDER_OPENED_DICT.keys():
            del happyforex_EA_instance.ORDER_OPENED_DICT[key] 
        for key in happyforex_EA_instance.ORDER_CLOSED_DICT.keys():
            del happyforex_EA_instance.ORDER_CLOSED_DICT[key] 
       
        # HEADER_ORDER_CLOSED_HISTORY = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
        happyforex_EA_instance.ORDER_OPENED_DICT[1] = [1106359662.0, 12805.0, 7662.0, 2.0, 1106359680.0, 0.01, 1.458, 0, 0.0, 0.0, 209.25, 0]
        print('happyforex_EA_instance.ORDER_OPENED_DICT')
        display_an_dict_with_delimiter(happyforex_EA_instance.ORDER_OPENED_DICT, ' ')
        
        happyforex_EA_instance.ords_in_a_day = 1
        happyforex_EA_instance.OPENORDERSLIMITDAY = 3
        happyforex_EA_instance.bid_nexttick_price = 1.50048
        happyforex_EA_instance.balance = 1000.00
        happyforex_EA_instance.CurrentProfit = 0.00
        happyforex_EA_instance.Lots = 0.01
        
        happyforex_EA_instance.ModifyPendingOrder_2()
        print('happyforex_EA_instance.ORDER_OPENED_DICT after ModifyPendingOrder_1')
        display_an_dict_with_delimiter(happyforex_EA_instance.ORDER_OPENED_DICT, ' ')
        
        # testing
        defined_type = OP_BUY
        print("==> defined_type: %s" % defined_type)
        
        order_123 = happyforex_EA_instance.ORDER_OPENED_DICT[1]
        order_type = order_123[ORDER_TYPE_COL_INDEX]
        print("==> order_type: %s" % order_type)
           
        self.assertEqual(defined_type, order_type, "Function IS NOT correct.")
    
    #===========================================================================
    def test_CheckEnoughMoney_2(self):
        print('#============================== test_CheckEnoughMoney_2 ==============================')
        '''
        equity = self.balance + self.CurrentProfit
        margin = order[PRICE_COL_INDEX] * order[LOTS_COL_INDEX] * ONE_LOT_VALUE / LEVERAGE
        free_magin = equity - margin
        
        equity = 10,000 + 0 = 10,000
        margin = 102.92 * 0.01 * 100,0000 / 100 = 1027.10
        free_magin = 10,000 - 1,027.10 = 8,972.9
        
        if (free_magin >= margin):
            return True
        '''
        
        happyforex_EA_instance.balance = 10000.00
        happyforex_EA_instance.CurrentProfit = 0.00
        print("==> happyforex_EA_instance.balance: %s" % happyforex_EA_instance.balance)
        print("==> happyforex_EA_instance.CurrentProfit: %s" % happyforex_EA_instance.CurrentProfit)
        
        order_123 = [1106359662.0, 12805.0, 7662.0, 2.0, 1106359680.0, 0.01, 102.92, 102.71, 0.0, 0.0, 0, 0]
       
        # testing 1
        flag_enoughmoney = happyforex_EA_instance.CheckEnoughMoney_2(order_123)
        print("==> flag_enoughmoney: %s" % flag_enoughmoney)
        
        self.assertTrue(flag_enoughmoney, "Function IS NOT correct.")
        
        # testing 2
        happyforex_EA_instance.balance = 1000.00
        flag_enoughmoney = happyforex_EA_instance.CheckEnoughMoney_2(order_123)
        print("==> flag_enoughmoney: %s" % flag_enoughmoney)
        
        self.assertFalse(flag_enoughmoney, "Function IS NOT correct.")
        
    #===========================================================================
    def test_DayOfWeek_3(self):
        print('#============================== test_DayOfWeek_3 ==============================')
        
        Day_2009_05_01 = convert_string_day2float('2009.05.01_00:00:00', MARKET_TIME_STANDARD, DATETIME_FORMAT)
        happyforex_EA_instance.current_day = Day_2009_05_01
        print("==> Day_2009_05_01 in numbers = %s" % Day_2009_05_01)
        
        test_day_of_week = happyforex_EA_instance.DayOfWeek_3()
        print("==> test_day_of_week: %s" % test_day_of_week)
           
        # testing (0-Monday,1,2,3,4,5,6)
        defined_day_of_week = 4
        print("==> defined_day_of_week: %s" % defined_day_of_week)
           
        self.assertEquals(defined_day_of_week, test_day_of_week , "Function IS NOT correct.")
        
    #===========================================================================
    def test_TimeHour_4(self):
        print('#============================== test_TimeHour_4 ==============================')
        
        happyforex_EA_instance = HappyForexEA()
        
        Time_04_30 = convert_string_second2float('2009.05.01_06:30:02', MARKET_TIME_STANDARD, DATETIME_FORMAT)
        happyforex_EA_instance.current_time = Time_04_30
        print("==> Time_04:30 in numbers = %s" % Time_04_30)
        
        test_hour_tick = happyforex_EA_instance.TimeHour_4()
        print("==> test_hour_tick: %s" % test_hour_tick)
           
        # testing
        defined_hour_tick = 6
        print("==> defined_hour_tick: %s" % defined_hour_tick)
           
        self.assertEquals(defined_hour_tick, test_hour_tick , "Function IS NOT correct.")
       
    #===========================================================================
    def test_TimeMinute_3(self):
        print('#============================== test_TimeMinute_3 ==============================')
        
        happyforex_EA_instance = HappyForexEA()
        
        Time_04_30 = convert_string_second2float('2009.05.01_06:30:02', MARKET_TIME_STANDARD, DATETIME_FORMAT)
        happyforex_EA_instance.current_time = Time_04_30
        print("==> Time_04:30 in numbers = %s" % Time_04_30)
        
        test_minute_tick = happyforex_EA_instance.TimeMinute_3()
        print("==> test_minute_tick: %s" % test_minute_tick)
           
        # testing
        defined_minute_tick = 30
        print("==> defined_minute_tick: %s" % defined_minute_tick)
           
        self.assertEquals(defined_minute_tick, test_minute_tick , "Function IS NOT correct.") 
    
     
################################################################################
##########################           CLASS           ###########################
################################################################################
class TestHardcodedData(unittest.TestCase):

    def setUp(self):
        pass

    #===========================================================================
    def test_convert_backflash2forwardflash(self):
            
        # original path with back flash
        print('')
        print('#============================== test_convert_backflash2forwardflash ==============================')
        path_test = os.getcwd()
        print('before convert = %s' % path_test)
            
        backflash_count = DEFAULT_NUMBER_INT
            
        # convert to forward flash
        path_test = convert_backflash2forwardflash(path_test)
        for i in range(len(path_test)):
            if path_test[i] == '\\':
                backflash_count += DEFAULT_SECOND_NUMBER_INT
        print('after convert = %s' % path_test)
            
        # testing
        self.assertEqual(backflash_count, DEFAULT_NUMBER_INT, "Convert NOT Successful.")
           
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
        write_wholedict2csv_no_header(test_dict, file_name_dict)
                  
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
        if (statinfo.st_size > DEFAULT_NUMBER_INT):
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
        self.assertEqual(len(myArray[DEFAULT_NUMBER_INT]), len(new_array[DEFAULT_NUMBER_INT]),
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
         
        sdatetime_1 = '2018.01.07_11:22:12'
        sdatetime_2 = '2017.01.08_11:22:13'
        print('==> date time format = %s' % DATETIME_FORMAT)
        print('==> sdatetime_1 = %s' % sdatetime_1)
        print('==> sdatetime_2 = %s' % sdatetime_2)
        
        flag_early_date = is_time_earlier(sdatetime_1, sdatetime_2, MARKET_TIME_STANDARD, DATETIME_FORMAT)
        
        # testing
        self.assertFalse(flag_early_date, "The function IS NOT correct..") 
    
    #===========================================================================
    def test_convert_string_datetime2float_no_ms(self):
        print('')
        print('#============================== test_convert_string_datetime2float_no_ms ==============================')
        
        convert_datetime = '2018.01.07_11:22:12'
        std_datetime = MARKET_TIME_STANDARD
        print('==> date time format = %s' % DATETIME_FORMAT)
        print('==> convert_datetime = %s' % convert_datetime)
        print('==> std_datetime = %s' % std_datetime)
        
        float_datetime = convert_string_datetime2float_no_ms(convert_datetime, std_datetime, DATETIME_FORMAT)
        print('==> float_datetime = %s' % float_datetime)
        
        # testing
        defined_int_datetime = 1515324132.00
        print('==> defined_int_datetime = %.2f' % defined_int_datetime)
        self.assertEqual(defined_int_datetime - float_datetime, float(DEFAULT_NUMBER_INT), "The function IS NOT correct..") 
               
    #===========================================================================
    def test_convert_string_second2float(self):
        print('')
        print('#============================== test_convert_string_second2float ==============================')
        
        convert_datetime = '2018.01.07_00:01:20'
        std_datetime = MARKET_TIME_STANDARD
        print('==> date time format = %s' % DATETIME_FORMAT)
        print('==> convert_datetime = %s' % convert_datetime)
        print('==> std_datetime = %s' % std_datetime)
        
        float_milliseconds = convert_string_second2float(convert_datetime, std_datetime, DATETIME_FORMAT)
        print('==> float_milliseconds = %s' % float_milliseconds)
        
        # testing
        defined_milliseconds = 80.00
        print('==> defined_milliseconds = %s' % defined_milliseconds)
        self.assertEqual(defined_milliseconds - float_milliseconds, float(DEFAULT_NUMBER_INT), "The function IS NOT correct..") 

    
################################################################################
##########################           MAIN           ############################
################################################################################
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
#===============================================================================
