'''
Created on Jan 4, 2018

@author: cao.vu.lam
'''
import unittest

from DataHandler.happyforex_Datahandler import DIGITS, DEFAULT_SECOND_NUMBER, DEFAULT_NUMBER, ORDER_TOTAL_HISTORY, ORDER_CLOSED_HISTORY, \
    display_an_array_with_delimiter, ORDER_OPENED_HISTORY
from EAModule.happyforex_EA import happyforex_EA_instance, BrokerIs5Digit_0

class Test(unittest.TestCase):

    #===========================================================================
    def testName(self):
        pass

    #===========================================================================
    def test_ProfitCheck(self):
        print('#============================== test_ProfitCheck ==============================')
      
        # HEADER_ORDER_HISTORY: ['Date', 'Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']
        ORDER_TOTAL_HISTORY[DEFAULT_SECOND_NUMBER] = ['1', '', '1', '', '', '', '', '', '-10', '990']
        ORDER_TOTAL_HISTORY[DEFAULT_SECOND_NUMBER + DEFAULT_SECOND_NUMBER] = ['2', '', '1', '', '', '', '', '', '40', '950']
         
        happyforex_EA_instance.CurrentProfit = happyforex_EA_instance.profit_check()
        print("==> happyforex_EA_instance.CurrentProfit: %s" % happyforex_EA_instance.CurrentProfit)
         
        # testing
        defined_CurrentProfit = float(30)
        print("==> defined_CurrentProfit: %s" % defined_CurrentProfit)
         
        self.assertEquals(defined_CurrentProfit - happyforex_EA_instance.CurrentProfit, float(DEFAULT_NUMBER) ,
                          "Function IS NOT correct.")
        
    #===========================================================================
    def test_BrokerIs5Digit(self):
        print('#============================== test_BrokerIs5Digit ==============================')
      
        print("==> DIGITS: %s" % DIGITS)
         
        flag_5Digit = happyforex_EA_instance.BrokerIs5Digit_0() 
        print(flag_5Digit)
         
        # testing
        self.assertTrue(flag_5Digit, "Function IS NOT correct.")
     
    #===========================================================================
    def test_MaxOrders(self):
        print('#============================== test_MaxOrders ==============================')
      
        happyforex_EA_instance.ords_in_a_day = 3
        print("==> ords_in_a_day: %s" % happyforex_EA_instance.ords_in_a_day)
         
         
        # testing
        orderLimit = 3
        print("==> orderLimit: %s" % orderLimit)
         
        flag_MaxOrder = False
        if happyforex_EA_instance.MaxOrders_9(orderLimit):
            flag_MaxOrder = True
        self.assertTrue(flag_MaxOrder, "Function IS NOT correct.")
        print('#============================== end 1 test ==============================')
      
        # testing
        orderLimit = 2
        print("==> orderLimit: %s" % orderLimit)
         
        flag_MaxOrder = False
        if happyforex_EA_instance.MaxOrders_9(orderLimit):
            flag_MaxOrder = True
        self.assertFalse(flag_MaxOrder, "Function IS NOT correct.")
        print('#============================== end 1 test ==============================')
      
        # testing
        happyforex_EA_instance.ords_in_a_day = 1
        print("==> ords_in_a_day=: %s" % happyforex_EA_instance.ords_in_a_day)
         
        flag_MaxOrder = False
        if happyforex_EA_instance.MaxOrders_9(orderLimit):
            flag_MaxOrder = True
        self.assertFalse(flag_MaxOrder, "Function IS NOT correct.")
     
    #===========================================================================
    def test_AccountBalance(self):
        print('#============================== test_AccountBalance ==============================')
      
        # HEADER_ORDER_HISTORY: ['Date', 'Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']
        ORDER_CLOSED_HISTORY[DEFAULT_SECOND_NUMBER] = ['1', '', '1', '', '', '', '', '', '-10', '990']
        ORDER_CLOSED_HISTORY[DEFAULT_SECOND_NUMBER + DEFAULT_SECOND_NUMBER] = ['2', '', '1', '', '', '', '', '', '40', '950']
         
        happyforex_EA_instance.balance = happyforex_EA_instance.AccountBalance_1(2)
        print("==> happyforex_EA_instance.balance: %s" % happyforex_EA_instance.balance)
         
        # testing
        defined_balance = float(950)
        print("==> defined_balance: %s" % defined_balance)
         
        self.assertEquals(defined_balance - happyforex_EA_instance.balance, float(DEFAULT_NUMBER) ,
                          "Function IS NOT correct.")
     
    #===========================================================================
    def test_DayOfWeek(self):
        print('#============================== test_DayOfWeek ==============================')
      
        today_date = happyforex_EA_instance.DayOfWeek_3()
        print("==> happyforex_EA_instance.DayOfWeek_3: %s" % today_date)
         
        # testing
        # TODO: CHANGE THE defined_date TO REFLECT THE CURRENT HOUR OF SYSTEM TIME
        defined_date = 3
        print("==> defined_date: %s" % defined_date)
         
        self.assertEquals(defined_date, today_date , "Function IS NOT correct.")
        
    #===========================================================================
    def test_TimeHour(self):
        print('#============================== test_TimeHour ==============================')
      
        today_hour = happyforex_EA_instance.TimeHour_4()
        print("==> happyforex_EA_instance.TimeLocal: %s" % today_hour)
         
        # testing
        # TODO: CHANGE THE defined_hour TO REFLECT THE CURRENT HOUR OF SYSTEM TIME
        defined_hour = 15
        print("==> defined_date: %s" % defined_hour)
         
        self.assertEquals(defined_hour, today_hour , "Function IS NOT correct.")
     
    #===========================================================================
    def test_TimeMinute(self):
        print('#============================== test_TimeMinute ==============================')
      
        today_minute = happyforex_EA_instance.TimeMinute_3()
        print("==> happyforex_EA_instance.TimeLocal: %s" % today_minute)
         
        # testing
        # TODO: CHANGE THE defined_minute TO REFLECT THE CURRENT HOUR OF SYSTEM TIME
        defined_minute = 9
        print("==> defined_date: %s" % defined_minute)
         
        self.assertEquals(defined_minute, today_minute , "Function IS NOT correct.")
     
    #===========================================================================
    def test_MODE_SPREAD(self):
        print('#============================== test_MODE_SPREAD ==============================')
      
        # HEADER_HISTORY_DATA = ['Date', 'Time', 'Bid', 'Ask', 'Volume']
        # HISTORY_DATA[DEFAULT_NUMBER] = [2018.01.09, 11:22:12, 1.19445, 1.19457, 1350]
        MODE_SPREAD_1 = happyforex_EA_instance.MODE_SPREAD_1(DEFAULT_NUMBER)
        print("==> happyforex_EA_instance.MODE_SPREAD_1: %s" % MODE_SPREAD_1)
         
        # testing
        defined_spread = abs(1.19457 - 1.19445) * 100000
        print("==> defined_spread: %s" % defined_spread)
         
        self.assertEquals(defined_spread - MODE_SPREAD_1, float(DEFAULT_NUMBER) ,
                          "Function IS NOT correct.")
        
    #===========================================================================
    def test_OrdersHistoryTotal(self):
        print('#============================== test_OrdersHistoryTotal ==============================')
      
        # HEADER_ORDER_CLOSED_HISTORY = ['Date', 'Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']
        ORDER_CLOSED_HISTORY[DEFAULT_SECOND_NUMBER] = ['1', '', '1', '', '', '', '', '', '-10', '990']
        ORDER_CLOSED_HISTORY[DEFAULT_SECOND_NUMBER + DEFAULT_SECOND_NUMBER] = ['2', '', '1', '', '', '', '', '', '40', '950']
         
        cnt = happyforex_EA_instance.OrdersHistoryTotal()
         
        print("==> total close orders: %s" % cnt)
         
        # testing
        defined_total_closed_orders = 655
        print("==> defined_total_closed_orders: %s" % defined_total_closed_orders)
         
        self.assertEquals(defined_total_closed_orders, cnt, "Function IS NOT correct.")
     
    #===========================================================================
    def test_OrderType(self):
        print('#============================== test_OrderType ==============================')
      
        # HEADER_ORDER_CLOSED_HISTORY = ['Date', 'Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']
        ORDER_CLOSED_HISTORY[DEFAULT_SECOND_NUMBER] = ['1', '', '1', '', '', '', '', '', '-10', '990']
        ORDER_CLOSED_HISTORY[DEFAULT_SECOND_NUMBER + DEFAULT_SECOND_NUMBER] = ['2', '', '1', '', '', '', '', '', '40', '950']
         
        order_type = happyforex_EA_instance.OrderType_5(DEFAULT_SECOND_NUMBER, ORDER_CLOSED_HISTORY)
        print("==> order_type: %s" % order_type)
         
        # testing
        defined_order_type = 1.00
        print("==> defined_order_type: %s" % defined_order_type)
         
        self.assertEquals(defined_order_type, order_type, "Function IS NOT correct.")
     
    #===========================================================================
    def test_OrderDelete(self):
        print('#============================== test_OrderDelete ==============================')
     
        # HEADER_ORDER_OPENED_HISTORY = ['Date', 'Time', 'Type', 'OrderID', 'Size', 'Price', 'SL', 'TP', 'Profit', 'Balance']
        ORDER_OPENED_HISTORY[DEFAULT_SECOND_NUMBER] = ['1', '', '1', '', '', '', '', '', '-10', '990']
        ORDER_OPENED_HISTORY[DEFAULT_SECOND_NUMBER + DEFAULT_SECOND_NUMBER] = ['2', '', '1', '', '', '', '', '', '40', '950']
        print("==> before deleting row [1]:")
        display_an_array_with_delimiter(ORDER_OPENED_HISTORY, '    ')
        print("==> length of array: %s" % len(ORDER_OPENED_HISTORY))
        
        
        del ORDER_OPENED_HISTORY[DEFAULT_SECOND_NUMBER]
        print("==> after deleting row [1]:")
        display_an_array_with_delimiter(ORDER_OPENED_HISTORY, '    ')
        print("==> new length of array: %s" % len(ORDER_OPENED_HISTORY))
        
        # testing
        defined_new_len = 655
        print("==> defined_new_len: %s" % defined_new_len)
        
        self.assertEquals(defined_new_len, len(ORDER_OPENED_HISTORY), "Function IS NOT correct.")
    
#===========================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
#===========================================================================
