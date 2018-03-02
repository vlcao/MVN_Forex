'''
Created on Dec 12, 2017

@author: cao.vu.lam
'''
#!/usr/bin/env python

import cProfile
import random
import logging.handlers
import os
import glob
import shutil

from multiprocessing.dummy import Pool as ThreadPool
from os import path, remove
from datetime import datetime, date
from DataHandler.hardcoded_data import DEFAULT_NUMBER_INT, DEPOSIT, DEFAULT_SECOND_NUMBER_INT, \
    BALANCE_COL_INDEX, BID_COL_INDEX, ASK_COL_INDEX, FILENAME_LOG_EA, \
    ORDER_TYPE_COL_INDEX, LOTS_COL_INDEX, LEVERAGE, HOURS_OF_ADAY, \
    FOLDER_DATA_OUTPUT, FILENAME_ORDER_CLOSED_HISTORY, ONE_LOT_VALUE, COMMISSION, NET_PROFIT, \
    VALUE_COL_INDEX, OP_SELL, OP_BUY, OP_SELLLIMIT, OP_BUYLIMIT, DATETIME_COL_INDEX, PROFIT_COL_INDEX, \
    FILENAME_ORDER_DELETED_HISTORY, ORDER_ID_COL_INDEX, DATEOFFSET, \
    MILLISECONDS_OF_ASECOND, SECONDS_OF_ANHOUR, SECONDS_OF_AMINUTE, \
    DAY_COL_INDEX, TIME_COL_INDEX, PRICE_ENTRY_COL_INDEX, PRICE_EXIT_COL_INDEX, \
    FILENAME_PROFILE_EA, FOLDER_DATA_INPUT, TIME_STAMP_FORMAT, SYMBOL, FOLDER_TICK_DATA_MODIFIED, \
    write_value_of_dict2csv_no_header, load_csv2array, point_of_symbol, digit_of_symbol, \
    convert_backflash2forwardflash, combine_all_files_in_a_folder, \
    DEFAULT_NUMBER_FLOAT, DEFAULT_SECOND_NUMBER_FLOAT, TIME_FRAME, \
    DEFAULT_PARAMETERS_DATA, TP_COL_INDEX, CALENDAR_ALL_SYMBOLS_DATA, \
    CALENDAR_BASE_SYMBOL_DATA, CALENDAR_QUOTE_SYMBOL_DATA, IMPACT_COL_INDEX, \
    write_array2csv_with_delimiter_no_header, convert_datetime_back_whole_list
    
import multiprocessing
from astropy.units import day
    
log = logging.getLogger(__name__)


################################################################################
#########################           CLASS           ############################
################################################################################        
class HappyForexEA(object):
    '''
    classdocs
    '''
 
    #===============================================================================
    def __init__(self):
        '''
        Constructor
        '''
        # get the total parameters for running EA
        self.NAME_EA = ""
        self.MAGIC = DEFAULT_NUMBER_INT
        self.FILTERSPREAD = False
        self.SPREADMAX = DEFAULT_NUMBER_FLOAT
        self.A = ""
        self.MONDAY = False
        self.TUESDAY = False
        self.WEDNESDAY = False
        self.THURSDAY = False
        self.FRIDAY = False
        self.SATURDAY = False
        self.SUNDAY = False
        self.B = ""
        self.TRADING_24H = False
        self.GMT_OFFSET = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_FROM = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_TO = DEFAULT_NUMBER_INT
        self.USE_ORDERSLIMIT = False
        self.OPENORDERSLIMITDAY = DEFAULT_NUMBER_INT
        self.C = ""
        self.TIME_CLOSING_TRADES = False
        self.TIME_OF_CLOSING_IN_HOURS = DEFAULT_NUMBER_INT
        self.TIME_OF_CLOSING_IN_MINUTES = DEFAULT_NUMBER_INT
        self.D = ""
        self.PROFIT = False
        self.PROFIT_ALL_ORDERS = DEFAULT_NUMBER_FLOAT
        self.E = ""
        self.OPENORDERSLIMIT = DEFAULT_NUMBER_INT
        self.SINGLEORDERSL = DEFAULT_NUMBER_FLOAT
        self.SINGLEORDERTP = DEFAULT_NUMBER_FLOAT
        self.F = ""
        self.ARRANGEMENTS_OF_TRADES = DEFAULT_NUMBER_FLOAT
        self.G = ""
        self.LOTS = DEFAULT_NUMBER_FLOAT
        self.SLIPPAGE = DEFAULT_NUMBER_FLOAT
        self.H = ""
        self.SET_UP_OF_LOSS = False
        self.AMOUNT_OF_LOSS = DEFAULT_NUMBER_FLOAT
        self.I = ""
        self.CLOSING_OF_ALL_TRADES = False
        self.J = ""
        self.USENEWSFILTER = False
        self.MINSBEFORENEWS = DEFAULT_NUMBER_INT
        self.MINSAFTERNEWS = DEFAULT_NUMBER_INT
        self.NEWSIMPACT = DEFAULT_NUMBER_FLOAT
        self.K = ""
        self.FILTERING = False
        self.L = ""
        self.AUTOEQUITYMANAGER = False
        self.EQUITYGAINPERCENT = DEFAULT_NUMBER_FLOAT
        self.SAFEEQUITYSTOPOUT = False
        self.SAFEEQUITYRISK = DEFAULT_NUMBER_FLOAT

        # new variables which will be changed in the class
        self.total_win = DEFAULT_NUMBER_FLOAT 
        self.total_loss = DEFAULT_NUMBER_FLOAT
        self.net_profit = DEFAULT_NUMBER_FLOAT
        self.ords_in_a_day = DEFAULT_NUMBER_INT
        self.current_datetime = DEFAULT_NUMBER_FLOAT  # (year + month + day + hour + minute + second  in SECOND)
        self.current_day = DEFAULT_NUMBER_FLOAT  # (year + month + day in DAYS)
        self.current_time = DEFAULT_NUMBER_FLOAT  # (hour + minute + second in SECOND)
        self.current_datetime_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_day_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_time_nexttick = DEFAULT_NUMBER_FLOAT  
        self.bid_price = DEFAULT_NUMBER_FLOAT
        self.ask_price = DEFAULT_NUMBER_FLOAT
        self.bid_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.ask_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.mode_spread = DEFAULT_NUMBER_FLOAT
        self.order_ID_dict = {}  # a dictionary (as a hash-map) for storing ID
        
        self.SpreadMax = DEFAULT_NUMBER_FLOAT
        self.Hour_of_trading_from = DEFAULT_NUMBER_INT
        self.Hour_of_trading_to = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_hours = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_minutes = DEFAULT_NUMBER_INT
        self.Time_closing_trades = False
        self.Lots = DEFAULT_NUMBER_FLOAT
        self.Slippage = DEFAULT_NUMBER_FLOAT
        
        self.balance = DEPOSIT
        self.CurrentProfit = DEFAULT_NUMBER_FLOAT  # current profit of all Opened orders (OP_BUY & OP_SELL)
        self.equity = self.balance + self.CurrentProfit
        
        self.EVENTS_OF_CALENDAR_ALL_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_BASE_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS = []
        self. PARAMETERS_DATA = []
        
        # Create dictionaries for storing Closed, Deleted, and Opened/Pending orders with KEY is OrderID
        self.ORDER_CLOSED_DICT = {} 
        self.ORDER_OPENED_DICT = {} 
        self.ORDER_DELETED_DICT = {} 
        
        # Create a list for storing the Tick data
        self.TICK_DATA = []
        
        # old variables from EA
        self.NDigits = DEFAULT_SECOND_NUMBER_FLOAT
        self.PipValue = DEFAULT_SECOND_NUMBER_FLOAT
        self.my_point = DEFAULT_SECOND_NUMBER_FLOAT
        
        self.ATR_Period = 7.0
        self.ATRPeriod1 = 3.0
        self.ATRPeriod2 = 5.0 
        self.ATRUpLimit1 = 13.0
        self.ATRDnLimit1 = 7.0
        self.ATRUpLimit2 = 21.0 
        self.ATRDnLimit2 = 16.0
        self.ATRUpLimit3 = 28.0
        self.ATRDnLimit3 = 25.0
        self.DeletePOATR = True      
        self.DeleteOrderATR = False
        
        self.LF = "\n"  
        self.ObjCount = DEFAULT_NUMBER_INT  
        self.FirstTime33 = False
        self.FirstTime35 = False
        self.Today6 = -1
        self.Count32 = DEFAULT_NUMBER_INT
        self.dblProfit = DEFAULT_NUMBER_FLOAT
        self.ATR = ""
        self.Trading = ""
        self.OrderCounter = DEFAULT_NUMBER_INT  # total Opened and Pending orders
        self.SellOrderExists = False
        self.BuyOrderExists = False
        self.BuyPOExists = False
        self.SellPOExists = False
        self.Overide = False
        self.Hour1 = DEFAULT_SECOND_NUMBER_INT
        self.Minute1 = DEFAULT_NUMBER_INT
        self.MagicChange = ""
        self.RMStatus = ""
        
        self.clear = False
    
    #===============================================================================
    def reset(self):
        '''
        Constructor
        '''
        # get the total parameters for running EA
        self.NAME_EA = ""
        self.MAGIC = DEFAULT_NUMBER_INT
        self.FILTERSPREAD = False
        self.SPREADMAX = DEFAULT_NUMBER_FLOAT
        self.A = ""
        self.MONDAY = False
        self.TUESDAY = False
        self.WEDNESDAY = False
        self.THURSDAY = False
        self.FRIDAY = False
        self.SATURDAY = False
        self.SUNDAY = False
        self.B = ""
        self.TRADING_24H = False
        self.GMT_OFFSET = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_FROM = DEFAULT_NUMBER_INT
        self.HOUR_OF_TRADING_TO = DEFAULT_NUMBER_INT
        self.USE_ORDERSLIMIT = False
        self.OPENORDERSLIMITDAY = DEFAULT_NUMBER_INT
        self.C = ""
        self.TIME_CLOSING_TRADES = False
        self.TIME_OF_CLOSING_IN_HOURS = DEFAULT_NUMBER_INT
        self.TIME_OF_CLOSING_IN_MINUTES = DEFAULT_NUMBER_INT
        self.D = ""
        self.PROFIT = False
        self.PROFIT_ALL_ORDERS = DEFAULT_NUMBER_FLOAT
        self.E = ""
        self.OPENORDERSLIMIT = DEFAULT_NUMBER_INT
        self.SINGLEORDERSL = DEFAULT_NUMBER_FLOAT
        self.SINGLEORDERTP = DEFAULT_NUMBER_FLOAT
        self.F = ""
        self.ARRANGEMENTS_OF_TRADES = DEFAULT_NUMBER_FLOAT
        self.G = ""
        self.LOTS = DEFAULT_NUMBER_FLOAT
        self.SLIPPAGE = DEFAULT_NUMBER_FLOAT
        self.H = ""
        self.SET_UP_OF_LOSS = False
        self.AMOUNT_OF_LOSS = DEFAULT_NUMBER_FLOAT
        self.I = ""
        self.CLOSING_OF_ALL_TRADES = False
        self.J = ""
        self.USENEWSFILTER = False
        self.MINSBEFORENEWS = DEFAULT_NUMBER_INT
        self.MINSAFTERNEWS = DEFAULT_NUMBER_INT
        self.NEWSIMPACT = DEFAULT_NUMBER_FLOAT
        self.K = ""
        self.FILTERING = False
        self.L = ""
        self.AUTOEQUITYMANAGER = False
        self.EQUITYGAINPERCENT = DEFAULT_NUMBER_FLOAT
        self.SAFEEQUITYSTOPOUT = False
        self.SAFEEQUITYRISK = DEFAULT_NUMBER_FLOAT

        # new variables which will be changed in the class
        self.total_win = DEFAULT_NUMBER_FLOAT 
        self.total_loss = DEFAULT_NUMBER_FLOAT
        self.net_profit = DEFAULT_NUMBER_FLOAT
        self.ords_in_a_day = DEFAULT_NUMBER_INT
        self.current_datetime = DEFAULT_NUMBER_FLOAT  # (year + month + day + hour + minute + second + millisecond in MILLISECOND)
        self.current_day = DEFAULT_NUMBER_FLOAT  # (year + month + day in DAYS)
        self.current_time = DEFAULT_NUMBER_FLOAT  # (hour + minute + second + millisecond in MILLISECOND)
        self.current_datetime_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_day_nexttick = DEFAULT_NUMBER_FLOAT  
        self.current_time_nexttick = DEFAULT_NUMBER_FLOAT  
        self.bid_price = DEFAULT_NUMBER_FLOAT
        self.ask_price = DEFAULT_NUMBER_FLOAT
        self.bid_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.ask_nexttick_price = DEFAULT_NUMBER_FLOAT
        self.mode_spread = DEFAULT_NUMBER_FLOAT
        self.order_ID_dict = {}  # a dictionary (as a hash-map) for storing ID
            
        self.SpreadMax = DEFAULT_NUMBER_FLOAT
        self.Hour_of_trading_from = DEFAULT_NUMBER_INT
        self.Hour_of_trading_to = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_hours = DEFAULT_NUMBER_INT
        self.Time_of_closing_in_minutes = DEFAULT_NUMBER_INT
        self.Time_closing_trades = False
        self.Lots = DEFAULT_NUMBER_FLOAT
        self.Slippage = DEFAULT_NUMBER_FLOAT
        
        self.balance = DEPOSIT
        self.CurrentProfit = DEFAULT_NUMBER_FLOAT  # current profit of all Opened orders (OP_BUY & OP_SELL)
        self.equity = self.balance + self.CurrentProfit
        
        self.EVENTS_OF_CALENDAR_ALL_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_BASE_SYMBOLS = []
        self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS = []
        self. PARAMETERS_DATA = []
        
        # Create a dictionary (as a hash-map) for storing Closed, Deleted, and Opened/Pending orders with KEY is OrderID
        self.ORDER_CLOSED_DICT = {} 
        self.ORDER_OPENED_DICT = {} 
        self.ORDER_DELETED_DICT = {} 
       
        # Create a list for storing the Tick data
        self.TICK_DATA = []
        
        # old variables from EA
        self.NDigits = DEFAULT_SECOND_NUMBER_FLOAT
        self.PipValue = DEFAULT_SECOND_NUMBER_FLOAT
        self.my_point = DEFAULT_SECOND_NUMBER_FLOAT
        
        self.ATR_Period = 7.0
        self.ATRPeriod1 = 3.0
        self.ATRPeriod2 = 5.0 
        self.ATRUpLimit1 = 13.0
        self.ATRDnLimit1 = 7.0
        self.ATRUpLimit2 = 21.0 
        self.ATRDnLimit2 = 16.0
        self.ATRUpLimit3 = 28.0
        self.ATRDnLimit3 = 25.0
        self.DeletePOATR = True      
        self.DeleteOrderATR = False
        
        self.LF = "\n"  
        self.ObjCount = DEFAULT_NUMBER_INT  
        self.FirstTime33 = False
        self.FirstTime35 = False
        self.Today6 = -1
        self.Count32 = DEFAULT_NUMBER_INT
        self.dblProfit = DEFAULT_NUMBER_FLOAT
        self.ATR = ""
        self.Trading = ""
        self.OrderCounter = DEFAULT_NUMBER_INT  # total Opened and Pending orders
        self.SellOrderExists = False
        self.BuyOrderExists = False
        self.BuyPOExists = False
        self.SellPOExists = False
        self.Overide = False
        self.Hour1 = DEFAULT_SECOND_NUMBER_INT
        self.Minute1 = DEFAULT_NUMBER_INT
        self.MagicChange = ""
        self.RMStatus = ""
        
        self.clear = False

    #===============================================================================
    def BrokerIs5Digit_0(self):
        ''' Return TRUE if the Broker is the 5 Digits Broker '''
    
        if (self.NDigits == 5 or self.NDigits == 3): 
            return(True)
        else:
            return(False)

    #===============================================================================
    def CalculateProfit_5(self, entry_price, exit_price, lots, order_type):
        ''' Calculates the profit or loss of a position in the home currency of the account. 
        1/When you go long, you enter the market at the ASK price and exit the market at BID price.
        2/When you go short, you enter the market at the BID price and exit at the ASK price.
        3/Pip Value = Pip in decimal places / Market Price * Trade Size
        For QUOTE_CURRENCY = 'USD', Pip Value will be multiple to Market Price 1 more time
        
        ==> Pip in decimal places = 0.0001 since 1/10,000th is a pip for all pairs (except JPY pairs)
                              = 0.01 for a JPY pair.
        ==> In all pairs involving the Japanese Yen (JPY), a pip is the 1/100th place -- 2 places to the right of the decimal. 
        In all other currency pairs, a pip is the 1/10,000 the place -- 4 places to the right of the decimal.
        '''
        
#         OLD CODES (17/01/2018_17:00:00)
#         result = DEFAULT_NUMBER_FLOAT
#     
#         if  (order_type == OP_BUY): 
#             result = ((exit_price - entry_price) * self.Lots * (1 / self.my_point) 
#                       * (PIP_VALUE_DICT[SYMBOL] * self.Lots / EXCHANGE_RATE_USD[QUOTE_CURRENCY]))
#         
#         
#         elif (order_type == OP_SELL):
#             result = ((entry_price - exit_price) * self.Lots * (1 / self.my_point) 
#                       * (PIP_VALUE_DICT[SYMBOL] * self.Lots / EXCHANGE_RATE_USD[QUOTE_CURRENCY]))
#         
#         return result
     
        result = DEFAULT_NUMBER_FLOAT
     
        if  (order_type == OP_BUY): 
            result = (exit_price - entry_price) * lots * ONE_LOT_VALUE - COMMISSION
         
        elif (order_type == OP_SELL):
            result = (entry_price - exit_price) * lots * ONE_LOT_VALUE - COMMISSION
        
        return round(float(result), self.NDigits)
        
    #===============================================================================
    def CreateUniqueOrderID_9(self, order_type):
        '''Create the unique order ID. Return -1 when cannot generate an order ID. '''
        
        # create the unique order ID which is the combination of all Values of parameters
        new_id = self.current_datetime + float(datetime.now().second)
        
        # keep create an individual while the ID is not unique
        while (new_id in self.order_ID_dict):
            new_id = self.current_datetime + float(datetime.now().second)
        
        # save new ID into the ID dictionary
        self.order_ID_dict[new_id] = order_type
        
        return new_id
    
    #===============================================================================
    def MaxOrders_9(self, num):
        ''' Return TRUE if the total number of orders in a day equal the Orders limit per day
            and delete all pending order in Opened and Pending orders pool when max orders reached '''
        
        ords = self.ords_in_a_day
        
        if (self.USE_ORDERSLIMIT == False): 
            return False
        
#         # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
#         # get all Opened and Pending orders in the pool
#         for order_id in self.ORDER_OPENED_DICT.keys():
#             # --> get the date-time of the opened/pending orders
#             opened_order = self.ORDER_OPENED_DICT[order_id]
#             order_type = opened_order[ORDER_TYPE_COL_INDEX]
#             OrderOpenTime = opened_order[DAY_COL_INDEX]
#             
#             # --> count orders when orders are BUY/SELL and in the current day (replace for: iBarShift(NULL,PERIOD_D1,OrderOpenTime())==0)
#             if (order_type < 2.00 and OrderOpenTime == self.current_day):
#                 ords += DEFAULT_SECOND_NUMBER_INT
#         
#         # get all Closed orders in the pool
#         for order_id in self.ORDER_CLOSED_DICT.keys():
#             # --> get the date-time of the closed/deleted orders and current date-time
#             closed_order = self.ORDER_CLOSED_DICT[order_id]
#             order_type = closed_order[ORDER_TYPE_COL_INDEX]
#             OrderClosedTime = float(closed_order[DAY_COL_INDEX])
#             
#             # --> count orders when orders are BUY/SELL and in the current day (replace for: iBarShift(NULL,PERIOD_D1,OrderOpenTime())==0)
#             if (order_type < 2.00 and OrderClosedTime == self.current_day):
#                 ords += DEFAULT_SECOND_NUMBER_INT
        
        # delete all pending order in Opened and Pending orders pool when max orders reached
        if (ords >= num):
            # get all Opened and Pending orders in the pool
            for order_id in self.ORDER_OPENED_DICT.keys():
               
                order = self.ORDER_OPENED_DICT[order_id]
                order_type = order[ORDER_TYPE_COL_INDEX]
            
                if (order_type > 1.00):
                    # --> delete orders when they are BUYLIMIT/SELLLIMIT
                    self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)
                    
                    # --> save this deleted orders in the Deleted orders pool
                    self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
    
            # max number of orders reached
            return True  
        else:
            return False
        
    #===============================================================================
    def ProfitCheck_3(self):
        ''' Return Profit of all closed trades following the '''
    
        net_profit = DEFAULT_NUMBER_FLOAT
        
        # get all the profits from Opened and Pending orders pool
        for order_id in self.ORDER_OPENED_DICT.keys():  # The order of the k's is not defined
            order = self.ORDER_OPENED_DICT[order_id]
            net_profit += order[PROFIT_COL_INDEX]
        
        return net_profit
        
    #===============================================================================
    def AccountBalance_1(self):
        ''' Return current balance of all orders '''
    
        account_bal = self.balance
        
#         if (len(self.ORDER_OPENED_DICT) == DEFAULT_NUMBER_INT and len(self.ORDER_CLOSED_DICT) == DEFAULT_NUMBER_INT):
#             return account_bal
#         else:
#             # get all the balance from Closed orders pool
#             for order_id in self.ORDER_CLOSED_DICT.keys():  # The order of the k's is not defined
# 
#                 order = self.ORDER_CLOSED_DICT[order_id]
#                 if (order[BALANCE_COL_INDEX] > account_bal):
#                     account_bal = order[BALANCE_COL_INDEX]
#     
#             # get all the balance from Opened and Pending orders pool
#             for order_id in self.ORDER_OPENED_DICT.keys():  # The order of the k's is not defined
# 
#                 order = self.ORDER_OPENED_DICT[order_id]
#                 if (order[BALANCE_COL_INDEX] > account_bal):
#                     account_bal = order[BALANCE_COL_INDEX]

        return account_bal
    
    #===============================================================================
    def DayOfWeek_3(self):
        ''' Return the current zero-based day of the week (0-Monday,1,2,3,4,5,6) 
        for the Tick data. '''
        
        # get back the date from number
        scurrentday = date.fromordinal(DATEOFFSET + int(self.current_day))
        
        # slit date into year, month, and day
        dividend = str(scurrentday).split('-')
        year = dividend[DEFAULT_NUMBER_INT]
        month = dividend[DEFAULT_SECOND_NUMBER_INT]
        day = dividend[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
        
        # get the day of the week from selected date
        day_of_week = date(int(year), int(month), int(day)).weekday()
        
        return day_of_week
    
    #===============================================================================
    def TimeHour_4(self):
        ''' Return the Hour(s) of the Tick data. '''
    
        hour_minute_second = int(self.current_time) 
        
        hour_tick = int(hour_minute_second / SECONDS_OF_ANHOUR)
        
        return hour_tick
    
    #===============================================================================
    def TimeMinute_3(self):
        ''' Return the Minute(s) of the Tick data. '''
        
        hour_minute_second = int(self.current_time) 
        
        minute_tick = int(hour_minute_second % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
        
        return minute_tick
    
    #===============================================================================
    def TimeHour_4_WithMilliSecondFormat(self):
        ''' Return the Hour(s) of the Tick data. '''
    
        # hr_min_sec_ms = self.current_time
        hour_minute_second = int(self.current_time / MILLISECONDS_OF_ASECOND) 
        
        hour_tick = int(hour_minute_second / SECONDS_OF_ANHOUR)
        
        return hour_tick
    
    #===============================================================================
    def TimeMinute_3_WithMilliSecondFormat(self):
        ''' Return the Minute(s) of the Tick data. '''
        
        # hr_min_sec_ms = self.current_time
        hour_minute_second = int(self.current_time / MILLISECONDS_OF_ASECOND) 
        
        minute_tick = int(hour_minute_second % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
        
        return minute_tick
    
    #===============================================================================
    def TimeSecond_3_WithMilliSecondFormat(self):
        ''' Return the Second(s) of the Tick data. '''
        
        # hr_min_sec_ms = self.current_time
        hour_minute_second = int(self.current_time / MILLISECONDS_OF_ASECOND) 
        
        second_tick = int(hour_minute_second % SECONDS_OF_ANHOUR % SECONDS_OF_AMINUTE)
        
        return second_tick
    
    #===============================================================================
    def TimeMilliSecond_3_WithMilliSecondFormat(self):
        ''' Return the MilliSecond(s) of the Tick data. '''
        
        return int(self.current_time % MILLISECONDS_OF_ASECOND)
    
    #===============================================================================
    def MODE_SPREAD_1(self, bid_price, ask_price):
        ''' Return spread of one record in TICK_DATA. '''
    
        spread = abs(bid_price - ask_price)
        
        for i in range(self.NDigits):
            spread *= float(10)
        
        return spread
    
    #===============================================================================
    def OrderType_5(self, order_id, dict_data):
        ''' Return order type of a record in the data. 
            OP_BUY          = 0.00
            OP_SELL         = 1.00
            OP_BUYLIMIT     = 2.00
            OP_SELLLIMIT    = 3.00
            OP_BUYSTOP      = 4.00
            OP_SELLSTOP     = 5.00 '''
        
        order_type = -1
        
        if (len(dict_data) != DEFAULT_NUMBER_INT):
            order = dict_data[order_id]
            order_type = float(order[ORDER_TYPE_COL_INDEX])
        else:
            log.info("There is NO data. Data size = 0")
                
        return order_type
    
    #===============================================================================
    def OrderDelete_4(self, order_id, dict_data):
        ''' Delete s specific order in data. '''
    
        # delete the order if it's existed in the data
        if (order_id in dict_data):
            del dict_data[order_id]
            return True
        else:
            log.info("There's NO %s in data. Data is the same as before deleting." % order_id)
            return False
        
    #===============================================================================
    def OrderAdd_10(self, order_id, order, dict_data):
        ''' Add a specific order in data. '''
    
        # add the order if it's NOT existed in the data
        if (order_id in dict_data):
            log.info("There's the oder %s in data already." % order_id)
            return False
        else:
            # add order to the data
            dict_data[order_id] = order
            return True
        
    #===============================================================================
    def OrderClose_4(self, order, order_id, order_type):
        ''' Close a specific old_opended_order in data by:
        * deleting this order in the Opened and Pending orders pool 
        * update the new values for this order from Opened to Close position
        * and save this deleted order in the Closed orders pools'''
        
        flag_order_closed = True
        
        # get the specific order
        new_closed_order = order
         
        if (order_type == OP_BUY or order_type == OP_SELL):
            # ORDER_OPENED_DICT[] = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
            # delete this order in the Opened and Pending orders pool
            if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                 
                # update the new values for this order from Opened to Close position
                profit = new_closed_order[PROFIT_COL_INDEX]
                self.balance = self.balance + profit
                                                 
                new_closed_order[DATETIME_COL_INDEX] = self.current_datetime
                new_closed_order[DAY_COL_INDEX] = self.current_day
                new_closed_order[TIME_COL_INDEX] = self.current_time
                new_closed_order[BALANCE_COL_INDEX] = self.balance 
                 
                # save this NEW Closed order in the Closed orders pool
                flag_order_closed = self.OrderAdd_10(order_id, new_closed_order, self.ORDER_CLOSED_DICT)    
                
            else:
                flag_order_closed = False
        
        # inform the result after placing the pending order OP_SELLLIMIT
        if (flag_order_closed):
#             print("Successfully Close the Opened order %s." % order_id)
            log.info("Successfully Close the Opened order %s." % order_id)
        else:
#             print("Error when closing the Opened order %s." % order_id)
            log.info("Error when closing the Opened order %s." % order_id)

        return flag_order_closed
         
    #===============================================================================
    def DeletePendingOrder19_3(self):
        ''' Delete an order OP_SELLLIMIT in the Opened and Pending order pool. '''
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
                
            # when the order is OP_SELLLIMIT
            if (order_type == OP_SELLLIMIT):
                # --> delete this OP_SELLLIMIT in the Opened and Pending orders pool
                if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                    # --> update date time and save this deleted OP_SELLLIMIT in the Deleted orders pool
                    order[DATETIME_COL_INDEX] = self.current_datetime
                    order[DAY_COL_INDEX] = self.current_day
                    order[TIME_COL_INDEX] = self.current_time
                    self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
        
    #===============================================================================
    def DeletePendingOrder18_3(self):
        ''' Delete an order OP_BUYLIMIT in the Opened and Pending order pool. '''
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # when the order is OP_BUYLIMIT
            if (order_type == OP_BUYLIMIT):
                # --> delete this OP_BUYLIMIT in the Opened and Pending orders pool
                if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                    # --> update date time and save this deleted OP_BUYLIMIT in the Deleted orders pool
                    order[DATETIME_COL_INDEX] = self.current_datetime
                    order[DAY_COL_INDEX] = self.current_day
                    order[TIME_COL_INDEX] = self.current_time
                    self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
        
    #===============================================================================
    def CheckLastOrderType33_4(self):
        ''' Check the last order and delete the pending OP_SELLLIMIT order when the last order was OP_SELL. '''
        
        orderType = -1.00
        lastCloseTime = DEFAULT_NUMBER_FLOAT

        # get all Closed orders in the pool
        # ORDER_CLOSED_DICT = {order_id:['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_CLOSED_DICT.keys():

            closed_order = self.ORDER_CLOSED_DICT[order_id]
            OrderCloseTime = closed_order[DATETIME_COL_INDEX]
            
            if (lastCloseTime < OrderCloseTime):
                lastCloseTime = OrderCloseTime
                orderType = closed_order[ORDER_TYPE_COL_INDEX]
        
        # delete the opened OP_SELLLIMIT orders when the last order was OP_SELL
        if (orderType == OP_SELL or self.FirstTime33):
            self.FirstTime33 = False
            self.DeletePendingOrder19_3()
    
    #===============================================================================
    def MathMax_6(self, float_num_1, float_num_2):
        max_number = DEFAULT_NUMBER_FLOAT
    
        if float_num_1 >= float_num_2:
            max_number = float_num_1
        else:
            max_number = float_num_2
                
        return max_number
    
    #===============================================================================
    def NormalizeDouble_9(self, float_num, digit_num):
        
        list_normalized_num = str_num = list(str(float_num))
            
        for i in range(len(str_num)):
            if (str_num[i] == '.'):
                # only normalize when numbers of digit numbers after decimal point matching input digit
                if (len(str_num) - i > i + digit_num):
                    # get all digits from float number until the expected digit number after decimal point
                    for j in range(i + digit_num):
                        list_normalized_num[j] = str_num[j]
                    
                    # assign the rest of the expected float number
                    k = len(str_num) - DEFAULT_SECOND_NUMBER_INT
                    while (k > i + digit_num):
                        if (digit_num == DEFAULT_NUMBER_INT):
                            list_normalized_num[k] = '0'
                        else:
                            list_normalized_num[k] = '9'
                        k -= DEFAULT_SECOND_NUMBER_INT    
                    
                break
        
        str_normalized_num = ''.join(list_normalized_num)
        
        return float(str_normalized_num)
        
    #===============================================================================
    def OrderSend_9(self, order_id, order_type, order_lots, order_price, order_slippage, order_sl, order_tp):
        ''' In this EA, this function is to place a Pending order OP_BUYLIMIT or OP_SELLLIMIT. 
        * return False when the order is not a Pending order.
        * order_slippage: Maximum price slippage (for buy or sell orders only). 
        * order_expire: Order expiration time (for pending orders only).'''

        # calculate slippage_in_decimal
        slippage_in_decimal = order_slippage
        for i in range(self.NDigits):
            slippage_in_decimal /= float(10)

        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        
        if (order_type != OP_BUYLIMIT and order_type != OP_SELLLIMIT):
            # print("This is not a Pending order OP_BUYLIMIT or OP_SELLLIMIT. Its type is %s." % (order_id, order_type))
            log.info("This is not a Pending order OP_BUYLIMIT or OP_SELLLIMIT. Its type is %s." % (order_id, order_type))
            return False
        # create a pending order OP_BUYLIMIT or OP_SELLLIMIT
        else:
            if (order_type == OP_BUYLIMIT):
                entry_price = order_price + slippage_in_decimal
                
            elif (order_type == OP_SELLLIMIT):
                entry_price = order_price - slippage_in_decimal
            
            order = [self.current_datetime,
                     self.current_day,
                     self.current_time,
                     order_type,
                     order_id,
                     order_lots,
                     round(entry_price, self.NDigits),
                     DEFAULT_NUMBER_FLOAT,
                     order_sl,
                     order_tp,
                     DEFAULT_NUMBER_FLOAT,
                     DEFAULT_NUMBER_FLOAT]
           
            # save this order in the Opened and Pending orders pool
            flag_added = self.OrderAdd_10(order_id, order, self.ORDER_OPENED_DICT)
            
            if (flag_added):
                return True
            
    #===============================================================================
    def BuyPendingOrder13_8(self):
        ''' Buy Pending Order OP_BUYLIMIT. '''
        
        # exit when reaching maximum orders per day
        if (self.MaxOrders_9(self.OPENORDERSLIMITDAY)):
            return
        
        # calculate all variables for placing an order
        price = (self.NormalizeDouble_9(self.ask_price, self.NDigits) 
                 + (self.ARRANGEMENTS_OF_TRADES * self.PipValue) * self.my_point)
        
        # calculate Stop Loss (SL) and Take Profit (TP_
        SL = price - (self.SINGLEORDERSL * self.PipValue * self.my_point)
        if (self.SINGLEORDERSL == DEFAULT_NUMBER_FLOAT):
            SL = DEFAULT_NUMBER_FLOAT
        
        TP = price + (self.SINGLEORDERTP * self.PipValue * self.my_point)
        if (self.SINGLEORDERTP == DEFAULT_NUMBER_FLOAT):
            TP = DEFAULT_NUMBER_FLOAT
           
        # place the pending order OP_BUYLIMIT
        order_id = self.CreateUniqueOrderID_9(OP_BUYLIMIT)
        ticket = self.OrderSend_9(order_id, OP_BUYLIMIT, self.Lots, price, self.SLIPPAGE, SL, TP)
        
        # inform the result after placing the pending order OP_BUYLIMIT
        if (ticket == False):
#             print("OrderSend_9() error for OP_BUYLIMIT %s" % order_id)
            log.info("OrderSend_9() error for OP_BUYLIMIT %s" % order_id)
        else:
#             print("Successfully placed the Pending order OP_BUYLIMIT %s." % order_id)
            log.info("Successfully placed the Pending order OP_BUYLIMIT %s." % order_id)
            
    #===============================================================================
    def SellPendingOrder14_8(self):
        ''' Sell Pending Order OP_SELLLIMIT. '''
        
        # exit when reaching maximum orders per day
        if (self.MaxOrders_9(self.OPENORDERSLIMITDAY)):
            return
        
        # calculate all variables for placing an order
        price = (self.NormalizeDouble_9(self.ask_price, self.NDigits) 
                 - (self.ARRANGEMENTS_OF_TRADES * self.PipValue) * self.my_point)
        
        # calculate Stop Loss (SL) and Take Profit (TP_
        SL = price + (self.SINGLEORDERSL * self.PipValue * self.my_point)
        if (self.SINGLEORDERSL == DEFAULT_NUMBER_FLOAT):
            SL = DEFAULT_NUMBER_FLOAT
        
        TP = price - (self.SINGLEORDERTP * self.PipValue * self.my_point)
        if (self.SINGLEORDERTP == DEFAULT_NUMBER_FLOAT):
            TP = DEFAULT_NUMBER_FLOAT
        
        # place the pending order OP_SELLLIMIT
        order_id = self.CreateUniqueOrderID_9(OP_SELLLIMIT)
        ticket = self.OrderSend_9(order_id, OP_SELLLIMIT, self.Lots, price, self.SLIPPAGE, SL, TP)
        
        # inform the result after placing the pending order OP_SELLLIMIT
        if (ticket == False):
#             print("OrderSend_9() error for OP_SELLLIMIT %s" % order_id)
            log.info("OrderSend_9() error for OP_SELLLIMIT %s" % order_id)
        else:
#             print("Successfully placed the Pending order OP_SELLLIMIT %s." % order_id)
            log.info("Successfully placed the Pending order OP_SELLLIMIT %s." % order_id)
            
    #===============================================================================
    def IfSellOrderDoesNotExist4_7(self, Mode):
        ''' Check whether the order OP_SELL existed in the Opened and Pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_SELL
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_SELL:
                self.SellOrderExists = True
                exists = True
            else:
                self.SellOrderExists = False
                
        if (exists == False and Mode == DEFAULT_SECOND_NUMBER_INT):
            self.BuyPendingOrder13_8()
        
        if (exists == True and Mode == 2):
            self.DeletePendingOrder18_3();
    
    #===============================================================================
    def IfBuyOrderDoesNotExist6_7(self, Mode):
        ''' Check whether the order OP_BUY existed in the Opened and Pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_BUY
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_BUY:
                self.BuyOrderExists = True
                exists = True
            else:
                self.BuyOrderExists = False
                
        if (exists == False and Mode == DEFAULT_SECOND_NUMBER_INT):
            self.SellPendingOrder14_8()
        
        if (exists == True and Mode == 2):
            self.DeletePendingOrder19_3();
    
    #===============================================================================
    def IfOrderDoesNotExist11_6(self):
        ''' Check whether the order OP_BUYLIMIT existed in the opned and pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_BUYLIMIT
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_BUYLIMIT:
                self.BuyPOExists = True
                exists = True
            else:
                self.BuyPOExists = False
                
        if (exists == False):
            self.IfSellOrderDoesNotExist4_7(1)
        
        if (exists == True):
            self.IfSellOrderDoesNotExist4_7(2);
        
    #===============================================================================
    def IfOrderDoesNotExist12_6(self):
        ''' Check whether the order OP_SELLLIMIT existed in the opned and pending order pool. '''
        exists = False
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            # when the order is OP_SELLLIMIT
            if self.OrderType_5(order_id, self.ORDER_OPENED_DICT) == OP_SELLLIMIT:
                self.SellPOExists = True
                exists = True
            else:
                self.SellPOExists = False
                
        if (exists == False):
            self.IfBuyOrderDoesNotExist6_7(1)
        
        if (exists == True):
            self.IfBuyOrderDoesNotExist6_7(2);
        
    #===============================================================================
    def ATRFilter_5(self):
        ''' ATRFilter_5. '''
        
        atr = [DEFAULT_NUMBER_FLOAT for i in range(int(self.MathMax_6(self.ATRPeriod1, self.ATRPeriod2) + self.ATR_Period))]
        atr_pips = [DEFAULT_NUMBER_FLOAT for i in range(int(self.MathMax_6(self.ATRPeriod1, self.ATRPeriod2) + self.ATR_Period))]
         
        # TODO: Work out the iATR and ATRPips function in Python
#         for i in range(self.MathMax_6(self.ATRPeriod1, self.ATRPeriod2) + self.ATR_Period):
#             # iATR(): Calculates the Average True Range indicator and returns its value.
#             atr[i] = iATR(Symbol(),PERIOD_M15,self.ATR_Period,i)
#          
#         ATRPips(atr, atr_pips, self.MathMax_6(self.ATRPeriod1,self.ATRPeriod2)+self.ATR_Period, self.my_point)
         
        atr_p = atr_pips[DEFAULT_NUMBER_INT]
        ATRPrePips1 = atr_pips[int(self.ATRPeriod1)]
        ATRPrePips2 = atr_pips[int(self.ATRPeriod2)]
         
        if ((((ATRPrePips1 >= self.ATRDnLimit1 and ATRPrePips1 <= self.ATRUpLimit1 and ATRPrePips2 >= self.ATRDnLimit1 and ATRPrePips2 <= self.ATRUpLimit1 and atr_p >= self.ATRDnLimit1 and atr_p <= self.ATRUpLimit1) 
              or (ATRPrePips1 >= self.ATRDnLimit2 and ATRPrePips1 <= self.ATRUpLimit2 and ATRPrePips2 >= self.ATRDnLimit2 and ATRPrePips2 <= self.ATRUpLimit2 and atr_p >= self.ATRDnLimit2 and atr_p <= self.ATRUpLimit2) 
              or (ATRPrePips1 >= self.ATRDnLimit3 and ATRPrePips1 <= self.ATRUpLimit3 and ATRPrePips2 >= self.ATRDnLimit3 and ATRPrePips2 <= self.ATRUpLimit3 and atr_p >= self.ATRDnLimit3 and atr_p <= self.ATRUpLimit3)) 
             and(self.FILTERING == True)) or (self.SellOrderExists == True) or (self.BuyOrderExists == True)):
     
            ATR = "Not ATR filtering!"
            self.IfOrderDoesNotExist11_6()
            self.IfOrderDoesNotExist12_6()
        
        # TODO: DEMO --> START here: 2 functions lead to placing Pending orders 
        elif (ATRPrePips1 == DEFAULT_NUMBER_FLOAT and ATRPrePips2 == DEFAULT_NUMBER_FLOAT):
            ATR = "Not ATR filtering!"
            self.IfOrderDoesNotExist11_6()
            self.IfOrderDoesNotExist12_6()
        # DEMO --> END here
        else:
            ATR = "ATR Filtering!"
            if((self.DeletePOATR == True) and (self.FILTERING == True)):
                self.DeletePendingOrder18_3()
                self.DeletePendingOrder19_3()
             
            if((self.DeleteOrderATR == True) and (self.FILTERING == True)):
                self.CloseOrder16_3()
                self.CloseOrder17_3()
            
        if (self.FILTERING == False):  
            ATR = ""
            self.IfOrderDoesNotExist11_6()
            self.IfOrderDoesNotExist12_6()
        
    #===============================================================================
    def LimitOpenOrders28_4(self):
        ''' Count all the number in the Opened and Pending order pool. '''
    
        count = DEFAULT_NUMBER_INT
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        
        # TODO: function leads to place Pending orders
        if (len(self.ORDER_OPENED_DICT) == DEFAULT_NUMBER_INT or self.OPENORDERSLIMIT == DEFAULT_NUMBER_INT):
            self.ATRFilter_5()
        else:
            for i in self.ORDER_OPENED_DICT.keys():
                count += DEFAULT_SECOND_NUMBER_INT
                
                # TODO: function leads to place Pending orders
                if (count < self.OPENORDERSLIMIT) or (self.OPENORDERSLIMIT == DEFAULT_NUMBER_INT):
                    self.ATRFilter_5()  
                           
                if (self.SellOrderExists == False) and (self.BuyOrderExists == False):
                    count = DEFAULT_NUMBER_INT
                    self.OrderCounter = count
                else:
                    count = count - DEFAULT_SECOND_NUMBER_INT
                    self.OrderCounter = count
                
    #===============================================================================
    def CheckLastOrderType35_4(self):
        ''' Check the last order and delete the pending OP_BUYLIMIT order when the last order was OP_BUY. '''
        
        orderType = -1.00
        lastCloseTime = DEFAULT_NUMBER_FLOAT

        # get all Closed orders in the pool
        # ORDER_CLOSED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_CLOSED_DICT.keys():
            
            closed_order = self.ORDER_CLOSED_DICT[order_id]
            OrderCloseTime = closed_order[DATETIME_COL_INDEX]
            
            if (lastCloseTime < OrderCloseTime):
                lastCloseTime = OrderCloseTime
                orderType = closed_order[ORDER_TYPE_COL_INDEX]
        
        # delete the opened OP_BUYLIMIT orders when the last order was OP_BUY
        if (orderType == OP_BUY or self.FirstTime35):
            self.FirstTime35 = False
            self.DeletePendingOrder18_3()

    #===============================================================================
    def get_previous_event_minute(self, current_minute, list_data):   
        ''' Get the previous minute of Calendar data comparing with Tick Data '''
             
        previous_event_minute = DEFAULT_NUMBER_INT
        
        for row_index in range(len(list_data)):
            time = int(list_data[row_index][TIME_COL_INDEX])
            minute_calendar = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
            
            # stop when minute of Calendar data is greater than current minute of Tick data
            if (minute_calendar > current_minute
                and row_index != DEFAULT_NUMBER_INT):
                
                # get previous_event_minute
                previous_time = int(list_data[row_index][TIME_COL_INDEX])
                previous_event_minute = int(previous_time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)   
        
        return previous_event_minute
    
    #===============================================================================
    def get_next_event_minute(self, current_minute, list_data):        
        ''' Get the next minute and its index of Calendar data comparing with Tick Data '''
        
        next_event_minute = DEFAULT_NUMBER_INT
        next_event_minute_index = -1
        
        for row_index in range(len(list_data)):
            time = int(list_data[row_index][TIME_COL_INDEX])
            minute_calendar = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
            
            # stop when minute of Calendar data is less than current minute of Tick data
            if (minute_calendar > current_minute
                and row_index != DEFAULT_NUMBER_INT):
                
                # get next_event_minute
                next_event_minute = minute_calendar
                next_event_minute_index = row_index   
        
        return [next_event_minute, next_event_minute_index]
    
    #===============================================================================
    def NewsTime_4(self):
        ''' NewsTime_4. '''
        
        News = False
        PrevMinute = -1
        
        # set default values
        minutesSincePrevEvent = DEFAULT_NUMBER_INT
        minutesUntilNextEvent = DEFAULT_NUMBER_INT
        impactOfNextEvent = DEFAULT_NUMBER_INT
        
        if (self.TimeMinute_3() != PrevMinute):     
            
            PrevMinute = self.TimeMinute_3()
            
            # Check the Calendar Event of ALL SYMBOLS
            if (self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT] != DEFAULT_NUMBER_INT):
                # get minutesSincePrevEvent
                previous_event_minute = self.get_previous_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT])
                minutesSincePrevEvent = PrevMinute - previous_event_minute 
            
                # get nminutesUntilNextEvent
                [next_event_minute, next_event_minute_index] = self.get_next_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT]) 
                minutesUntilNextEvent = next_event_minute - PrevMinute
                
                # get value of News impact
                if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                     or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                    and next_event_minute_index != -1):
                    
                    next_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_NUMBER_INT]
                    impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                    if (impactOfNextEvent >= self.NEWSIMPACT): 
                        News = True
            else:
                # get minutesSincePrevEvent
                if (self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    previous_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
                    time = int(previous_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                    previous_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                else:
                    previous_event_minute = DEFAULT_NUMBER_INT
                    
                minutesSincePrevEvent = PrevMinute - previous_event_minute 
            
                # get nminutesUntilNextEvent
                if (self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    next_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                    time = int(next_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                    next_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                else:
                    next_event_minute = DEFAULT_NUMBER_INT
                
                next_event_minute_index = DEFAULT_NUMBER_INT 
                minutesUntilNextEvent = next_event_minute - PrevMinute
                
                # get value of News impact
                if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                     or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                    and next_event_minute_index != -1):
                    
                    next_events_list = self.EVENTS_OF_CALENDAR_ALL_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                    impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                    if (impactOfNextEvent >= self.NEWSIMPACT): 
                        News = True
            
            # Check the Calendar Event of BASE SYMBOL
            if (News == False):
                if (self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    # get minutesSincePrevEvent
                    previous_event_minute = self.get_previous_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT])
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    [next_event_minute, next_event_minute_index] = self.get_next_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT]) 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                         or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
                else:
                    # get minutesSincePrevEvent
                    if (self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        previous_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
                        time = int(previous_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        previous_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        previous_event_minute = DEFAULT_NUMBER_INT
                        
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    if (self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        next_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        time = int(next_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        next_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        next_event_minute = DEFAULT_NUMBER_INT
                    
                    next_event_minute_index = DEFAULT_NUMBER_INT 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if ((minutesUntilNextEvent <= self.MINSBEFORENEWS 
                         or minutesSincePrevEvent <= self.MINSAFTERNEWS) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_BASE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
             
            # Check the Calendar Event of QUOTE SYMBOL
            if (News == False):
                if (self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT] != DEFAULT_NUMBER_INT):
                    # get minutesSincePrevEvent
                    previous_event_minute = self.get_previous_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT])
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    [next_event_minute, next_event_minute_index] = self.get_next_event_minute(PrevMinute, self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT]) 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if (((minutesUntilNextEvent <= self.MINSBEFORENEWS) 
                         or (minutesSincePrevEvent <= self.MINSAFTERNEWS)) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
                    
                else:
                    # get minutesSincePrevEvent
                    if (self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        previous_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT + DEFAULT_SECOND_NUMBER_INT]
                        time = int(previous_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        previous_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        previous_event_minute = DEFAULT_NUMBER_INT
                        
                    minutesSincePrevEvent = PrevMinute - previous_event_minute 
                
                    # get nminutesUntilNextEvent
                    if (self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT] != DEFAULT_NUMBER_INT):
                        next_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        time = int(next_events_list[DEFAULT_NUMBER_INT][TIME_COL_INDEX])
                        next_event_minute = int(time % SECONDS_OF_ANHOUR / SECONDS_OF_AMINUTE)
                    else:
                        next_event_minute = DEFAULT_NUMBER_INT
                    
                    next_event_minute_index = DEFAULT_NUMBER_INT 
                    minutesUntilNextEvent = next_event_minute - PrevMinute
                    
                    # get value of News impact
                    if ((minutesUntilNextEvent <= self.MINSBEFORENEWS 
                         or minutesSincePrevEvent <= self.MINSAFTERNEWS) 
                        and next_event_minute_index != -1):
                        
                        next_events_list = self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS[DEFAULT_SECOND_NUMBER_INT]
                        impactOfNextEvent = float(next_events_list[next_event_minute_index][IMPACT_COL_INDEX])
                        if (impactOfNextEvent >= self.NEWSIMPACT): 
                            News = True
                        
        return News

    #===============================================================================
    def HoursFilter22_3(self):
        ''' HoursFilter22_3. '''
    
        # get the Hour of local time/system time
        hour0 = self.TimeHour_4()
        
        if (self.NewsTime_4() == False 
            and (((self.Hour_of_trading_from < self.Hour_of_trading_to and hour0 >= self.Hour_of_trading_from and hour0 < self.Hour_of_trading_to) 
                  or (self.Hour_of_trading_from > self.Hour_of_trading_to and (hour0 < self.Hour_of_trading_to or hour0 >= self.Hour_of_trading_from))) and (self.TRADING_24H == False))):
             
            self.Trading = "Trading!"
            if (self.FILTERSPREAD and self.mode_spread > self.SpreadMax):
                # print("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                log.info("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                return
 
            self.CheckLastOrderType33_4()
            self.LimitOpenOrders28_4()
            self.CheckLastOrderType35_4()
        else:
            if (self.TRADING_24H == False) and (self.SellOrderExists == False) and (self.BuyOrderExists == False):
                self.Trading = "Not Trading!"
                self.DeletePendingOrder18_3()
                self.DeletePendingOrder19_3()
            else:
                self.Trading = "Override Hour/Day Filter"
                if  (self.FILTERSPREAD == True and self.mode_spread > self.SpreadMax):
                    # print("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    log.info("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    return
                    
                self.CheckLastOrderType33_4()
                self.LimitOpenOrders28_4()
                self.CheckLastOrderType35_4()
                
        if (self.TRADING_24H == True):
            if (self.Overide == True):
                self.Trading = "Override Hour/Day Filter"
            else:
                self.Trading = "Trading 24h"
                 
                if (self.FILTERSPREAD == True) and (self.mode_spread > self.SpreadMax):
                    # print("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    log.info("Comment: Spread too high! Max spread: %s - Current spread: %s. Date: %s" % (self.SpreadMax, self.mode_spread, self.current_datetime))
                    return
                 
                self.CheckLastOrderType33_4()
                self.LimitOpenOrders28_4()
                self.CheckLastOrderType35_4()
    
    #===============================================================================
    def WeekdayFilter23_2(self):
        ''' WeekdayFilter23_2  '''
            
        # (0 - Monday, 1, 2, 3, 4, 5, 6)
        if ((self.MONDAY and self.DayOfWeek_3() == 0) 
            or (self.TUESDAY and self.DayOfWeek_3() == 1) 
            or (self.WEDNESDAY and self.DayOfWeek_3() == 2) 
            or (self.THURSDAY and self.DayOfWeek_3() == 3) 
            or (self.FRIDAY and self.DayOfWeek_3() == 4) 
            or (self.SATURDAY and self.DayOfWeek_3() == 5) 
            or (self.SUNDAY and self.DayOfWeek_3() == 6)):
            
            self.Overide = False
            self.HoursFilter22_3()
        
        else:
            if (self.SellOrderExists == False) and (self.BuyOrderExists == False):
                self.Trading = "Not Trading!"
                self.DeletePendingOrder18_3()
                self.DeletePendingOrder19_3()
            else:
                self.Overide = True
                self.HoursFilter22_3()
        
    #===============================================================================
    def CloseOrder17_3(self):
        ''' Close OP_BUY and delete OP_BUYLIMIT in Opened and Pending order pool. '''
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # close orders when they are OP_BUY orders
            if  (order_type == OP_BUY):
                # --> Close a specific old_opended_order in data by deleting this OP_BUY in the Opened and Pending orders pool 
                # and return new value of order from Opened position to Close position
                self.OrderClose_4(order, order_id, order_type)
        
        self.DeletePendingOrder18_3()         
        
    #===============================================================================
    def CloseOrder16_3(self):
        ''' Close OP_SELL and delete OP_SELLLIMIT in Opened and Pending order pool. '''
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # close orders when they are OP_SELL orders
            if  (order_type == OP_SELL):
                # --> Close a specific old_opended_order in data by deleting this OP_SELL in the Opened and Pending orders pool 
                # and return new value of order from Opened position to Close position
                self.OrderClose_4(order, order_id, order_type)
                
        self.DeletePendingOrder19_3()   
        
    #===============================================================================
    def CloseOrderIf21_2(self):
        ''' Close all orders in Opened orders pool when satisfied conditions. '''
        
        dblProfit = DEFAULT_NUMBER_FLOAT
    
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            order = self.ORDER_OPENED_DICT[order_id]
            OrderProfit = float(order[PROFIT_COL_INDEX])
            dblProfit += OrderProfit
        
        if  ((self.PROFIT and dblProfit >= self.PROFIT_ALL_ORDERS) 
             or (dblProfit <= self.AMOUNT_OF_LOSS and self.SET_UP_OF_LOSS == True) 
             or self.CLOSING_OF_ALL_TRADES == True):
        
            for order_id in self.ORDER_OPENED_DICT.keys():
                self.CloseOrder16_3()
                self.CloseOrder17_3()
        
    #===============================================================================
    def AtCertainTime6_2(self):
        ''' Return  '''
    
        # get the Hour of local time/system time
        hour0 = self.TimeHour_4()
        minute0 = self.TimeMinute_3()
        
        if ((self.DayOfWeek_3() != self.Today6 and hour0 > self.Time_of_closing_in_hours and minute0 > self.Time_of_closing_in_minutes) 
            and (self.Time_closing_trades == True) 
            and  self.ProfitCheck_3() > DEFAULT_NUMBER_FLOAT):

            self.Today6 = self.DayOfWeek_3();
            self.CloseOrder17_3();
            self.CloseOrder16_3();
        
    #===============================================================================
    def OnEveryTick24_1(self):
        ''' Actions for every tick  '''
        
        # functions for placing Pending orders
        self.WeekdayFilter23_2()
        self.AtCertainTime6_2()
        
        # TODO: Extra Functions for having Open/Market orders: 
        self.ModifyPendingOrder_2()
        
        # function for closing orders
        self.CloseOrderIf21_2()
                
    #===============================================================================
    def CloseDeleteAll_1(self):
        ''' Close all orders  '''
        
        flag_close_delete_all = True
        
        # get all Opened and Pending orders in the pool
        # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
        for order_id in self.ORDER_OPENED_DICT.keys():
            
            order = self.ORDER_OPENED_DICT[order_id]
            order_type = order[ORDER_TYPE_COL_INDEX]
            
            # when the order is OP_BUY or OP_SELL
            if  (order_type == OP_BUY or order_type == OP_SELL):
                # --> Close a specific old_opended_order in data by deleting this OP_BUY in the Opened and Pending orders pool 
                # and return new value of order from Opened position to Close position
                flag_close_delete_all = self.OrderClose_4(order, order_id, order_type)
                
                if (flag_close_delete_all == False):
                    return flag_close_delete_all
            
            # when the order is OP_BUYLIMIT or OP_SELLLIMIT
            if  (order_type == OP_BUYLIMIT or order_type == OP_SELLLIMIT):
                
                # --> delete this OP_BUYLIMIT or OP_SELLLIMIT oder in the Opened and Pending orders pool
                flag_close_delete_all = self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)
               
                if (flag_close_delete_all):
                    # --> update date time and save this deleted OP_BUYLIMIT or OP_SELLLIMIT oder in the Deleted orders pool
                    order[DATETIME_COL_INDEX] = self.current_datetime
                    order[DAY_COL_INDEX] = self.current_day
                    order[TIME_COL_INDEX] = self.current_time
                    flag_close_delete_all = self.OrderAdd_10(order_id, order, self.ORDER_DELETED_DICT)
            
                    if (flag_close_delete_all == False):
                        return flag_close_delete_all
            
        return flag_close_delete_all
            
    #===============================================================================
    def CheckEnoughMoney_2(self, order):
        ''' Check if there are enough money in the account for open an order by calculating Equity. '''
        
        self.CurrentProfit = self.ProfitCheck_3()
        
        # EQUITY = BALANCE + PROFIT
        equity = self.balance + self.CurrentProfit
            
        # MARGIN = ENTRY PRICE * SIZE /LEVERAGE 
        margin = order[PRICE_ENTRY_COL_INDEX] * order[LOTS_COL_INDEX] * ONE_LOT_VALUE / LEVERAGE
        
        # FREE MARGIN = EQUITY - MARGIN
        free_magin = equity - margin
        
        if (free_magin >= margin):
            return True
        else:
            # print("There are not enough money in account to open order %s" % order[ORDER_ID_COL_INDEX])
            log.info("There are not enough money in account to open order %s" % order[ORDER_ID_COL_INDEX])
            return False
        
    #===============================================================================
    def ModifyPendingOrder_2(self):
        ''' If there are enough money in the account for opening a pending order, this pending order will 
        be modified into a market one (opened). '''
        
        if (self.ords_in_a_day >= self.OPENORDERSLIMITDAY):
#             print("Cannot modify this Pending order due to reaching maximum %s orders per day." % self.OPENORDERSLIMITDAY)
            log.info("Cannot modify this Pending order due to reaching maximum %s orders per day." % self.OPENORDERSLIMITDAY)
        else:
            # get all Opened and Pending orders in the pool
            # ORDER_OPENED_DICT = {order_id: ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']}
            for order_id in self.ORDER_OPENED_DICT.keys():
                order = self.ORDER_OPENED_DICT[order_id]
                order_type = order[ORDER_TYPE_COL_INDEX]
                    
                # check if it can be modified to become an Open order or not when this order is OP_BUYLIMIT or OP_BUYLIMIT 
                if  (order_type == OP_BUYLIMIT or order_type == OP_SELLLIMIT):
                    
                    entry_price = order[PRICE_ENTRY_COL_INDEX]
                    exit_price = DEFAULT_NUMBER_FLOAT
                    flag_modified = False
                    message = ""
                    
                    # compare entry price with exit price from next tick
                    if (order_type == OP_BUYLIMIT):
                        exit_price = self.bid_nexttick_price
                        message = "Modified the Pending order OP_BUYLIMIT " + str(order_id) + " to Open order OP_BUY."
                        
                        if (entry_price <= exit_price
                            and exit_price != DEFAULT_NUMBER_FLOAT):
                            flag_modified = True
                        else:
                            flag_modified = False
#                             print("Cannot modify order OP_BUYLIMIT %s due to entry_price <= exit_price." % order_id)
                            log.info("Cannot modify order OP_BUYLIMIT %s due to entry_price <= exit_price." % order_id)
                            
                    # compare entry price with exit price from next tick
                    elif (order_type == OP_SELLLIMIT):
                        exit_price = self.ask_nexttick_price
                        message = "Modified the Pending order OP_SELLLIMIT " + str(order_id) + " to Open order OP_SELL."
                        
                        if (entry_price >= exit_price
                            and exit_price != DEFAULT_NUMBER_FLOAT):
                            flag_modified = True
                        else:
                            flag_modified = False
#                             print("Cannot modify order OP_SELLLIMIT %s due to entry_price >= exit_price." % order_id)
                            log.info("Cannot modify order OP_SELLLIMIT %s due to entry_price >= exit_price." % order_id)
                            
                    # when this Pending order can be modified
                    if (flag_modified):
                        # modified this Pending order to become Open order when having enough money
                        if (self.CheckEnoughMoney_2(order)):  
                            # delete this order in the Opened and Pending orders pool
                            if (self.OrderDelete_4(order_id, self.ORDER_OPENED_DICT)):
                                '''When you go long, you enter the market at the ASK price and exit the market at BID price.
                                When you go short, you enter the market at the BID price and exit at the ASK price.'''
                                # ORDER_OPENED_DICT[] = ['Date_Time', 'Day', 'Time', 'Type', 'OrderID', 'Size', 'EntryPrice', 'ExitPrice', 'SL', 'TP', 'Profit', 'Balance']
                                
                                # update the new type for this Pending order 
                                new_order_type = order_type
                                if (order_type == OP_BUYLIMIT):
                                    new_order_type = OP_BUY
                                    
                                elif (order_type == OP_SELLLIMIT):
                                    new_order_type = OP_SELL
                                    
                                # calculate the new profit   
                                lots = order[LOTS_COL_INDEX]
                                profit = self.CalculateProfit_5(entry_price, exit_price, lots, new_order_type)
                                self.net_profit = self.net_profit + profit
                                                
                                order[DATETIME_COL_INDEX] = self.current_datetime_nexttick
                                order[DAY_COL_INDEX] = self.current_day_nexttick
                                order[TIME_COL_INDEX] = self.current_time_nexttick
                                order[ORDER_TYPE_COL_INDEX] = new_order_type
                                order[PRICE_ENTRY_COL_INDEX] = entry_price
                                order[PRICE_EXIT_COL_INDEX] = exit_price
                                order[PROFIT_COL_INDEX] = profit
                                if (profit < DEFAULT_NUMBER_FLOAT):
                                    order[TP_COL_INDEX] = DEFAULT_SECOND_NUMBER_FLOAT
                                        
                                # save back this deleted order in the Opened and Pending orders pool with updated values
                                # and update the numbers of Open orders per day
                                if (self.OrderAdd_10(order_id, order, self.ORDER_OPENED_DICT)):
                                    self.ords_in_a_day += DEFAULT_SECOND_NUMBER_INT
#                                     print(message)
                                    log.info(message)
                        else:
#                             print("There are NOT enough money to modify this Pending order %s to Open order." % order_id)
                            log.info("There are NOT enough money to modify this Pending order %s to Open order." % order_id)

    #===============================================================================
    def initilize(self, PARAMETERS_COMPLETED, DIGITS, POINT):
    
        # get the total parameters for running EA
        name_ea_row_index = 0
        magic_row_index = 1
        filterspread_row_index = 2
        spreadmax_row_index = 3
        a_row_index = 4
        monday_row_index = 5
        tuesday_row_index = 6
        wednesday_row_index = 7
        thursday_row_index = 8
        friday_row_index = 9
        saturday_row_index = 10
        sunday_row_index = 11
        b_row_index = 12
        trading_24h_row_index = 13
        gmt_offset_row_index = 14
        hour_of_trading_from_row_index = 15
        hour_of_trading_to_row_index = 16
        use_orderslimit_row_index = 17
        openorderslimitday_row_index = 18
        c_row_index = 19
        time_closing_trades_row_index = 20
        time_of_closing_in_hours_row_index = 21
        time_of_closing_in_minutes_row_index = 22
        d_row_index = 23
        profit_row_index = 24
        profit_all_orders_row_index = 25
        e_row_index = 26
        openorderslimit_row_index = 27
        singleordersl_row_index = 28
        singleordertp_row_index = 29
        f_row_index = 30
        arrangements_of_trades_row_index = 31
        g_row_index = 32
        lots_row_index = 33
        slippage_row_index = 34
        h_row_index = 35
        set_up_of_loss_row_index = 36
        amount_of_loss_row_index = 37
        i_row_index = 38
        closing_of_all_trades_row_index = 39
        j_row_index = 40
        usenewsfilter_row_index = 41
        minsbeforenews_row_index = 42
        minsafternews_row_index = 43
        newsimpact_row_index = 44
        k_row_index = 45
        filtering_row_index = 46
        l_row_index = 47
        autoequitymanager_row_index = 48
        equitygainpercent_row_index = 49
        safeequitystopout_row_index = 50
        safeequityrisk_row_index = 51
        
        self.NAME_EA = str(PARAMETERS_COMPLETED[name_ea_row_index]
                           [VALUE_COL_INDEX])
        self.MAGIC = int(PARAMETERS_COMPLETED[magic_row_index]
                         [VALUE_COL_INDEX])
        self.FILTERSPREAD = bool(str(PARAMETERS_COMPLETED[filterspread_row_index]
                                     [VALUE_COL_INDEX]).title())
        self.SPREADMAX = float(PARAMETERS_COMPLETED[spreadmax_row_index]
                               [VALUE_COL_INDEX])
        self.A = str(PARAMETERS_COMPLETED[a_row_index]
                     [VALUE_COL_INDEX])
        self.MONDAY = bool(str(PARAMETERS_COMPLETED[monday_row_index]
                               [VALUE_COL_INDEX]).title())
        self.TUESDAY = bool(str(PARAMETERS_COMPLETED[tuesday_row_index]
                                [VALUE_COL_INDEX]).title())
        self.WEDNESDAY = bool(str(PARAMETERS_COMPLETED[wednesday_row_index]
                                  [VALUE_COL_INDEX]).title())
        self.THURSDAY = bool(str(PARAMETERS_COMPLETED[thursday_row_index]
                                 [VALUE_COL_INDEX]).title())
        self.FRIDAY = bool(str(PARAMETERS_COMPLETED[friday_row_index]
                               [VALUE_COL_INDEX]).title())
        self.SATURDAY = bool(str(PARAMETERS_COMPLETED[saturday_row_index]
                                 [VALUE_COL_INDEX]).title())
        self.SUNDAY = bool(str(PARAMETERS_COMPLETED[sunday_row_index]
                               [VALUE_COL_INDEX]).title())
        self.B = str(PARAMETERS_COMPLETED[b_row_index]
                     [VALUE_COL_INDEX])
        self.TRADING_24H = bool(str(PARAMETERS_COMPLETED[trading_24h_row_index]
                                    [VALUE_COL_INDEX]).title())
        self.GMT_OFFSET = int(PARAMETERS_COMPLETED[gmt_offset_row_index][VALUE_COL_INDEX])
        self.HOUR_OF_TRADING_FROM = int(PARAMETERS_COMPLETED[hour_of_trading_from_row_index]
                                        [VALUE_COL_INDEX])
        self.HOUR_OF_TRADING_TO = int(PARAMETERS_COMPLETED[hour_of_trading_to_row_index]
                                      [VALUE_COL_INDEX])
        self.USE_ORDERSLIMIT = bool(str(PARAMETERS_COMPLETED[use_orderslimit_row_index]
                                        [VALUE_COL_INDEX]).title())
        self.OPENORDERSLIMITDAY = int(PARAMETERS_COMPLETED[openorderslimitday_row_index]
                                      [VALUE_COL_INDEX])
        self.C = str(PARAMETERS_COMPLETED[c_row_index]
                     [VALUE_COL_INDEX])
        self.TIME_CLOSING_TRADES = bool(str(PARAMETERS_COMPLETED[time_closing_trades_row_index]
                                            [VALUE_COL_INDEX]).title())
        self.TIME_OF_CLOSING_IN_HOURS = int(PARAMETERS_COMPLETED[time_of_closing_in_hours_row_index]
                                            [VALUE_COL_INDEX])
        self.TIME_OF_CLOSING_IN_MINUTES = int(PARAMETERS_COMPLETED[time_of_closing_in_minutes_row_index]
                                              [VALUE_COL_INDEX])
        self.D = str(PARAMETERS_COMPLETED[d_row_index]
                     [VALUE_COL_INDEX])
        self.PROFIT = bool(str(PARAMETERS_COMPLETED[profit_row_index]
                               [VALUE_COL_INDEX]).title())
        self.PROFIT_ALL_ORDERS = float(PARAMETERS_COMPLETED[profit_all_orders_row_index]
                                       [VALUE_COL_INDEX])
        self.E = str(PARAMETERS_COMPLETED[e_row_index]
                     [VALUE_COL_INDEX])
        self.OPENORDERSLIMIT = int(PARAMETERS_COMPLETED[openorderslimit_row_index]
                                   [VALUE_COL_INDEX])
        self.SINGLEORDERSL = float(PARAMETERS_COMPLETED[singleordersl_row_index]
                                   [VALUE_COL_INDEX])
        self.SINGLEORDERTP = float(PARAMETERS_COMPLETED[singleordertp_row_index]
                                   [VALUE_COL_INDEX])
        self.F = str(PARAMETERS_COMPLETED[f_row_index]
                     [VALUE_COL_INDEX])
        self.ARRANGEMENTS_OF_TRADES = float(PARAMETERS_COMPLETED[arrangements_of_trades_row_index]
                                            [VALUE_COL_INDEX])
        self.G = str(PARAMETERS_COMPLETED[g_row_index]
                     [VALUE_COL_INDEX])
        self.LOTS = float(PARAMETERS_COMPLETED[lots_row_index]
                          [VALUE_COL_INDEX])
        self.SLIPPAGE = float(PARAMETERS_COMPLETED[slippage_row_index]
                              [VALUE_COL_INDEX])
        self.H = str(PARAMETERS_COMPLETED[h_row_index]
                     [VALUE_COL_INDEX])
        self.SET_UP_OF_LOSS = bool(str(PARAMETERS_COMPLETED[set_up_of_loss_row_index]
                                       [VALUE_COL_INDEX]).title())
        self.AMOUNT_OF_LOSS = float(PARAMETERS_COMPLETED[amount_of_loss_row_index]
                                    [VALUE_COL_INDEX])
        self.I = str(PARAMETERS_COMPLETED[i_row_index]
                     [VALUE_COL_INDEX])
        self.CLOSING_OF_ALL_TRADES = bool(str(PARAMETERS_COMPLETED[closing_of_all_trades_row_index]
                                              [VALUE_COL_INDEX]).title())
        self.J = str(PARAMETERS_COMPLETED[j_row_index]
                     [VALUE_COL_INDEX])
        self.USENEWSFILTER = bool(str(PARAMETERS_COMPLETED[usenewsfilter_row_index]
                                      [VALUE_COL_INDEX]).title())
        self.MINSBEFORENEWS = int(PARAMETERS_COMPLETED[minsbeforenews_row_index]
                                  [VALUE_COL_INDEX])
        self.MINSAFTERNEWS = int(PARAMETERS_COMPLETED[minsafternews_row_index]
                                 [VALUE_COL_INDEX])
        self.NEWSIMPACT = float(PARAMETERS_COMPLETED[newsimpact_row_index]
                              [VALUE_COL_INDEX])
        self.K = str(PARAMETERS_COMPLETED[k_row_index]
                     [VALUE_COL_INDEX])
        self.FILTERING = bool(str(PARAMETERS_COMPLETED[filtering_row_index]
                                  [VALUE_COL_INDEX]).title())
        self.L = str(PARAMETERS_COMPLETED[l_row_index]
                     [VALUE_COL_INDEX])
        self.AUTOEQUITYMANAGER = bool(str(PARAMETERS_COMPLETED[autoequitymanager_row_index]
                                          [VALUE_COL_INDEX]).title())
        self.EQUITYGAINPERCENT = float(PARAMETERS_COMPLETED[equitygainpercent_row_index]
                                       [VALUE_COL_INDEX])
        self.SAFEEQUITYSTOPOUT = bool(str(PARAMETERS_COMPLETED[safeequitystopout_row_index]
                                          [VALUE_COL_INDEX]).title())
        self.SAFEEQUITYRISK = float(PARAMETERS_COMPLETED[safeequityrisk_row_index]
                                    [VALUE_COL_INDEX])
        
        # set up all other parameters
        self.SpreadMax = self.SPREADMAX
        self.Hour_of_trading_from = self.HOUR_OF_TRADING_FROM
        self.Hour_of_trading_to = self.HOUR_OF_TRADING_TO
        self.Time_of_closing_in_hours = self.TIME_OF_CLOSING_IN_HOURS
        self.Time_of_closing_in_minutes = self.TIME_OF_CLOSING_IN_MINUTES
        self.Time_closing_trades = self.TIME_CLOSING_TRADES
        self.Lots = self.LOTS
        self.Slippage = self.SLIPPAGE
        self.NDigits = DIGITS
        self.my_point = POINT
        
        # Adjust for 4/5 digit brokers
        if self.BrokerIs5Digit_0(): 
            self.PipValue = float(10)
            self.my_point *= float(10)
            self.SpreadMax *= float(10)
        
        # Adjust the time following local time
        self.Hour_of_trading_from += self.GMT_OFFSET
        if(self.Hour_of_trading_from >= HOURS_OF_ADAY):
            self.Hour_of_trading_from -= HOURS_OF_ADAY
        if(self.Hour_of_trading_from < DEFAULT_NUMBER_INT):
            self.Hour_of_trading_from += HOURS_OF_ADAY 
                
        self.Hour_of_trading_to += self.GMT_OFFSET
        if(self.Hour_of_trading_to >= HOURS_OF_ADAY):
            self.Hour_of_trading_to -= HOURS_OF_ADAY
        if(self.Hour_of_trading_to < DEFAULT_NUMBER_INT):
            self.Hour_of_trading_to += HOURS_OF_ADAY 
        
        self.Time_of_closing_in_hours += self.GMT_OFFSET
        if(self.Time_of_closing_in_hours >= HOURS_OF_ADAY):
            self.Time_of_closing_in_hours -= HOURS_OF_ADAY
        if(self.Time_of_closing_in_hours < DEFAULT_NUMBER_INT):
            self.Time_of_closing_in_hours += HOURS_OF_ADAY

    #===============================================================================
    def get_event_in_a_day(self, current_day, list_data):
        ''' Get all events happen in a specific day '''
        
        event_in_current_day = []
        event_in_next_day = []
        event_in_previous_day = []
        flag_event = False

        for event_index in range(len(list_data)):
            day = float(list_data[event_index][DAY_COL_INDEX])

            # get all event in the same day            
            if (day == current_day):
                event_in_current_day.append(list_data[event_index])
                flag_event = True 
            # when there is no same day
            else:
                if (flag_event):
                    break
                else:
                    if (day > current_day):
                        next_day_index = event_index
                        previous_day_index = event_index - DEFAULT_SECOND_NUMBER_INT
                        
                        # get all events of the next available day
                        current_day = day
                        while (day == current_day and next_day_index < len(list_data)):
                            event_in_next_day.append(list_data[next_day_index])
                            next_day_index += DEFAULT_SECOND_NUMBER_INT
                            day = float(list_data[next_day_index][DAY_COL_INDEX])
                            
                        # get all events of the previous available day
                        day = float(list_data[previous_day_index][DAY_COL_INDEX])
                        current_day = day
                        while (day == current_day and previous_day_index > DEFAULT_NUMBER_INT):
                            event_in_previous_day.append(list_data[previous_day_index])
                            previous_day_index -= DEFAULT_SECOND_NUMBER_INT
                            day = float(list_data[previous_day_index][DAY_COL_INDEX])
                            
                        break
                    else:
                        pass
                    
        return [event_in_current_day, event_in_next_day, event_in_previous_day]
    
    #===============================================================================
    def analised_tick_data(self, PARAMETERS_DATA, folder_output, file_):
        
        # get the file name
        file_name = convert_backflash2forwardflash(file_)
        file_basename = str(os.path.basename(file_))
        
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==> Loading TICK DATA from file: {0}...".format(file_basename))
        print("{0} ==> Loading TICK DATA from file: {1}...".format(time_stamp, file_basename))
        
        # Create TICK_DATA from the Modified CSV file
        TICK_DATA = load_csv2array(file_name)
        DIGITS = digit_of_symbol(float(TICK_DATA[DEFAULT_NUMBER_INT][BID_COL_INDEX]))
        POINT = point_of_symbol(float(TICK_DATA[DEFAULT_NUMBER_INT][BID_COL_INDEX]))
        
        # set up all the total parameters for running EA
        self.reset()
        self.initilize(PARAMETERS_DATA, DIGITS, POINT)
        
        fprevious_day = float(TICK_DATA[DEFAULT_NUMBER_INT][DAY_COL_INDEX])
        
        # get all events of the CALENDAR_DATA
        self.EVENTS_OF_CALENDAR_ALL_SYMBOLS = self.get_event_in_a_day(fprevious_day, CALENDAR_ALL_SYMBOLS_DATA)
        self.EVENTS_OF_CALENDAR_BASE_SYMBOLS = self.get_event_in_a_day(fprevious_day, CALENDAR_BASE_SYMBOL_DATA)
        self.EVENTS_OF_CALENDAR_QUOTE_SYMBOLS = self.get_event_in_a_day(fprevious_day, CALENDAR_QUOTE_SYMBOL_DATA)
        
        current_tick = next_tick = DEFAULT_NUMBER_INT
        while (current_tick < len(TICK_DATA) - DEFAULT_SECOND_NUMBER_INT):
            
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            if (current_tick == DEFAULT_NUMBER_INT):
                log.info("... ==> start processing the data...")
                print("%s... ==> start processing the data..." % time_stamp)
            
            # get the values from the current tick
            self.current_datetime = float(TICK_DATA[current_tick][DATETIME_COL_INDEX])
            self.current_day = float(TICK_DATA[current_tick][DAY_COL_INDEX])
            self.current_time = float(TICK_DATA[current_tick][TIME_COL_INDEX])
            self.bid_price = float(TICK_DATA[current_tick][BID_COL_INDEX])
            self.ask_price = float(TICK_DATA[current_tick][ASK_COL_INDEX])
            
            self.mode_spread = self.MODE_SPREAD_1(self.bid_price, self.ask_price)

            # save the previous date when going to a new date 
            if (fprevious_day != self.current_day):
                
                ''' For EA running by itself '''
                time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
                log.info("==> current_tick: %s" % current_tick)
                log.info("==> checking date %s" % self.current_datetime)
                print("{0} ==> current_tick: {1}".format(time_stamp, current_tick))
                print("{0} ==> checking date {1}".format(time_stamp, self.current_datetime))
                 
                run_percentage = round((float(current_tick) / float(len(TICK_DATA))) * float(100), 2)
                 
#                 log.info("==> current_tick: %s" % current_tick)
                log.info("... ==> processing {0}% of the data, date {1}...".format(run_percentage, self.current_datetime))
                time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
#                 print("{0} ==> current_tick: {1}".format(time_stamp, current_tick))
                print("{0}... ==> processing {1}% of the data...".format(time_stamp, run_percentage, self.current_datetime))
                
                # save the old date
                fprevious_day = self.current_day
                
                # reset the Maximum Open orders per day
                self.ords_in_a_day = DEFAULT_NUMBER_INT
              
            # find the next tick following the input Time Frame
            while next_tick < range(len(TICK_DATA) - current_tick):
                self.current_day_nexttick = float(TICK_DATA[next_tick][DAY_COL_INDEX])
                self.current_time_nexttick = float(TICK_DATA[next_tick][TIME_COL_INDEX])
                
                # get the values from the next tick
                diff_time = (self.current_day_nexttick + self.current_time_nexttick) - (self.current_day + self.current_time) 
                
                if (self.current_day != self.current_day_nexttick):
                    self.current_day_nexttick = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][DAY_COL_INDEX])
                    self.current_time_nexttick = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][TIME_COL_INDEX])
                    self.current_datetime_nexttick = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][DATETIME_COL_INDEX])
                    self.bid_nexttick_price = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][BID_COL_INDEX])
                    self.ask_nexttick_price = float(TICK_DATA[next_tick - DEFAULT_SECOND_NUMBER_INT][ASK_COL_INDEX])
            
                    # move to next tick
                    current_tick = next_tick
                    next_tick += DEFAULT_SECOND_NUMBER_INT
                    break
                elif (diff_time >= TIME_FRAME
                    or next_tick == len(TICK_DATA) - DEFAULT_SECOND_NUMBER_INT):
                    
                    self.current_datetime_nexttick = float(TICK_DATA[next_tick][DATETIME_COL_INDEX])
                    self.bid_nexttick_price = float(TICK_DATA[next_tick][BID_COL_INDEX])
                    self.ask_nexttick_price = float(TICK_DATA[next_tick][ASK_COL_INDEX])
            
                    # move to next tick
                    current_tick = next_tick
                    next_tick += DEFAULT_SECOND_NUMBER_INT
                    break
                else:
                    next_tick += DEFAULT_SECOND_NUMBER_INT
                
            # check if reaching maximum orders and delete the pending orders            
            if (self.MaxOrders_9(self.OPENORDERSLIMITDAY)):
                continue
            else:
                if (self.clear):                       
                    if (self.CloseDeleteAll_1()):
                        self.clear = False
                    else:
                        return
                            
                # check total profit at the moment
                self.CurrentProfit = self.ProfitCheck_3()
                
                # check total balance at the moment
                self.balance = self.AccountBalance_1()  # uzavrete obchody
                    
                # --> SAFEEQUITYSTOPOUT and AUTOEQUITYMANAGER
                if (self.SAFEEQUITYSTOPOUT 
                    and (self.SAFEEQUITYRISK / float(100)) * self.balance < self.CurrentProfit * float(-1) 
                    and self.CloseDeleteAll_1() == False):
                            self.clear = True
                            return 
                
                if (self.AUTOEQUITYMANAGER 
                    and (self.EQUITYGAINPERCENT / float(100)) * self.balance < self.CurrentProfit 
                    and self.CloseDeleteAll_1() == False):
                            self.clear = True
                            return
               
                # Original Function from original EA
                self.OnEveryTick24_1()
        
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Completed running tick data file: {0} with profit {1}!".format(file_basename, self.net_profit))
        print("{0} ==>  Completed running tick data file: {1} with profit {2}!".format(time_stamp, file_basename, self.net_profit))
                        
        # Write out other data for reference
        file_basename = file_basename.split('.')[DEFAULT_NUMBER_INT]
        write_value_of_dict2csv_no_header(self.ORDER_CLOSED_DICT, folder_output + file_basename + '_' + FILENAME_ORDER_CLOSED_HISTORY)
        write_value_of_dict2csv_no_header(self.ORDER_DELETED_DICT, folder_output + file_basename + '_' + FILENAME_ORDER_DELETED_HISTORY)
                
        return self.net_profit

    #===============================================================================
    def run_testing(self):
        ''' Randomly create values of NetProfit for testing only '''
    
        return (random.random() * NET_PROFIT)
        
    #===============================================================================
    def run(self, PARAMETERS_DATA, individual_ID):
        ''' EA running '''
        
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Start calculating fitness for individual {0}!".format(individual_ID))
        print("{0} ==>  Start calculating fitness for individual {1}!".format(time_stamp, individual_ID))
            
        total_profit = DEFAULT_NUMBER_FLOAT 
#         self.PARAMETERS_DATA = copy_string_array(PARAMETERS_DATA)
        
        # Create an folder for storing all outputs in this section 
        folder_output = FOLDER_DATA_OUTPUT + SYMBOL + '_ind_' + str(individual_ID) + '_outputs/'
        if os.path.exists(folder_output):
            shutil.rmtree(folder_output)
        os.makedirs(folder_output)
        
        # Access the input folder to get the Tick Data
        folder_name = convert_backflash2forwardflash(FOLDER_DATA_INPUT + SYMBOL + FOLDER_TICK_DATA_MODIFIED)
        allFiles = glob.glob(folder_name + '/*.csv')
        
        ''' SINGLETHREADING 
        for file_ in allFiles:
            total_profit += HappyForexEA().analised_tick_data(PARAMETERS_DATA, folder_output, file_,)
        '''
        
        ''' MULTITHREADING '''
        # make the Pool of workers
        pool_size = multiprocessing.cpu_count()
        
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Pool size of ThreadPool: {0}!".format(pool_size))
        print("{0} ==>  Pool size of ThreadPool: {1}!".format(time_stamp, pool_size))
         
#        # Another Multi_threading method
#         results = ea_pool.map(self.analised_tick_data, allFiles)
#         ea_pool.close() 
#         ea_pool.join()
#         
#         for profit_ in results:
#             total_profit += float(profit_)
        
        ea_pool = ThreadPool(pool_size)
        
        # Running EA process
        results = [ea_pool.apply_async(HappyForexEA().analised_tick_data, (PARAMETERS_DATA, folder_output, file_,))
                   for file_ in allFiles]
         
        # --> proxy.get() waits for task completion and returns the result
        profits = [r.get() for r in results]  
         
        # close the pool and wait for the work to finish 
        ea_pool.close() 
        
        # get the total profit after running all the Tick data
        for profit_ in profits:
            total_profit += float(profit_)
            
        # write out other data for reference
        file_name_out = FOLDER_DATA_OUTPUT + SYMBOL + '/ind_' + str(individual_ID) + '_$' + str(round(total_profit, 2)) + '_' + FILENAME_ORDER_CLOSED_HISTORY
        combine_all_files_in_a_folder(folder_output, file_name_out,
                                      '*_' + FILENAME_ORDER_CLOSED_HISTORY)
        
        # convert back the Date Time for output file
        converted_data = convert_datetime_back_whole_list(file_name_out)
        
        # create a new file name
        write_array2csv_with_delimiter_no_header(converted_data, file_name_out, ',')
    
        # delete output folder after writing out the order history 
        if os.path.exists(folder_output):
            shutil.rmtree(folder_output)
            
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log.info("==>  Completed calculating fitness for individual {0} with profit {1}!".format(individual_ID, round(total_profit, 2)))
        print("{0} ==>  Completed calculating fitness for individual {1} with profit {2}!".format(time_stamp, individual_ID, round(total_profit, 2)))
            
        return total_profit

################################################################################
##########################           MAIN           ############################
################################################################################        


#===============================================================================
if __name__ == "__main__":
    
#     # create an instance EA for running 
#     happyforex_EA_instance = HappyForexEA()
#            
#     # running EA
#     happyforex_EA_instance.run(DEFAULT_PARAMETERS_DATA, 1)
    
    ''' RUNNING WITH LOG AND PROFILE '''
    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile(FOLDER_DATA_OUTPUT + FILENAME_LOG_EA):
        remove(FOLDER_DATA_OUTPUT + FILENAME_LOG_EA)
         
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", FOLDER_DATA_OUTPUT + FILENAME_LOG_EA))
     
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
     
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
     
    try:
              
        # create an instance EA for running 
        happyforex_EA_instance = HappyForexEA()
        
        # running EA
        cProfile.run('happyforex_EA_instance.run(DEFAULT_PARAMETERS_DATA, 1)', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_EA)
#         happyforex_EA_instance.run(DEFAULT_PARAMETERS_DATA, 1)
        
    except Exception:
        logging.exception("Exception in main")
        exit(1) 

