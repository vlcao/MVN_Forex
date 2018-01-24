'''
Created on Dec 22, 2017

@author: cao.vu.lam
'''

import logging
import random
import sys
from DataHandler.happyforex_Datahandler import DEFAULT_NUMBER, MAX_LOTS, NET_PROFIT, MAX_FITNESS, \
                                    OPTIMIZED_PARAMETERS_DATA, OPTIMIZE_PARAMETERS_LIST, \
                                    VALUE_COL_INDEX, DEFAULT_SECOND_NUMBER, DEFAULT_PARAMETERS_DATA, \
                                    copy_string_array, permutation_count, merge_2parametes_array_data
from EAModule.happyforex_EA import HappyForexEA

log = logging.getLogger(__name__)

################################################################################
##########################           CLASS           ###########################
################################################################################
class Individual(object):
    '''
    classdocs
    '''
    
    #===============================================================================
    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        
        # default attributes
        self.net_profit = DEFAULT_NUMBER
        self.total_win = DEFAULT_NUMBER
        self.fitness = DEFAULT_NUMBER
        self.individual_ID = str(DEFAULT_NUMBER)
       
        # copy optimize-needed and default parameters for each individual to become its genes
        self.genes = copy_string_array(OPTIMIZED_PARAMETERS_DATA)
        self.genes_completed = copy_string_array(DEFAULT_PARAMETERS_DATA)
        
        # Create a dictionary (as a hash-map) for storing Closed and Deleted orders with KEY is OrderID
        self.ORDER_CLOSED_DICT = {} 
        
        # Create a dictionary (as a hash-map) for storing Opened and Pending orders with KEY is OrderID
        self.ORDER_OPENED_DICT = {} 
        
        # Create a dictionary (as a hash-map) for storing Opened and Pending orders with KEY is OrderID
        self.DATE_DATA_DICT = {} 
        
    #===============================================================================
    def create_random_genes(self):
        # reset genes randomly for each individual
        row = DEFAULT_NUMBER
        col = 1
        
        # --> FilterSpread ==> random 1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER, sys.maxint) % 2  
        row += 1
        # --> Friday ==> random 1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER, sys.maxint) % 2  
        row += 1
        # --> OpenOrdersLimitDay ==> random 1 to 3
        self.genes[row][col] = random.randint(DEFAULT_NUMBER + 1, int(self.genes[row][col]))  
        row += 1
        # --> Time_closing_trades ==> random 1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER, sys.maxint) % 2  
        # --> only change value of Time_of_closing_in_hours ==> random 5 or 6 when Time_closing_trades==True
        if self.genes[row][col] == '1':
            row += 1
            self.genes[row][col] = random.randint(int(self.genes[row][col]), int(self.genes[row][col]) + 1) 
        else:
            row += 2
        # --> Profit_all_orders ==> random 1 to 12 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER + 1, int(self.genes[row][col]))  
        row += 1
        # --> Arrangements_of_trades ==> random 1 or 25
        random_num = random.randint(DEFAULT_NUMBER + 1, abs(int(self.genes[row][col])))
        self.genes[row][col] = random_num * (-1)  
        row += 1
        # --> Lots ==> random 0.01 to 0.1
        random_num = random.uniform(float(self.genes[row][col]), MAX_LOTS)
        self.genes[row][col] = round(random_num, 2)  
        
        
        # create the whole completed parameters for running EA
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
    
    #===============================================================================
    '''
    manual_parameters_list = ['FilterSpread', 'Friday', 'OpenOrdersLimitDay', 'Time_closing_trades', 'Time_of_closing_in_hours',
                       'Profit_all_orders', 'Arrangements_of_trades', 'Lots']
    '''
    def create_manual_genes(self, manual_parameters_list):
        # reset genes randomly for each individual
        row = DEFAULT_NUMBER
        col = 1
        
        # --> FilterSpread
        self.genes[row][col] = manual_parameters_list[row] 
        row += 1
        # --> Friday
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> OpenOrdersLimitDay
        self.genes[row][col] = manual_parameters_list[row]   
        row += 1
        # --> Time_closing_trades
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> Time_of_closing_in_hours
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> Profit_all_orders
        self.genes[row][col] = manual_parameters_list[row]   
        row += 1
        # --> Arrangements_of_trades
        self.genes[row][col] = manual_parameters_list[row]  
        row += 1
        # --> Lots
        self.genes[row][col] = manual_parameters_list[row]   
    
    
        # create the whole completed parameters for running EA
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
    
    #===============================================================================
    def create_ind_uniqueID(self, dictionary_IDlist):

        # create the individual's ID which is the combination of all Values of parameters
        col_index_value = 1
        new_id = '_' . join([str(row[col_index_value]) for row in self.genes])
        
        # keep create an individual while the ID is not unique
        while (new_id in dictionary_IDlist == True):
            self.create_random_genes()
            new_id = '_' . join([str(row[col_index_value]) for row in self.genes])
        
        # assign the new ID to an individual
        self.individual_ID = new_id
           
        return new_id
    
    #===============================================================================
    def flip_value(self, mutation_point):
        
        key_col_index = DEFAULT_NUMBER
         
        # Flip values at the mutation point
        # --> FilterSpread=true (default) ==> 1/0
        if self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_SECOND_NUMBER):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER)
         
        # --> Friday=true (default) ==> 1/0
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_SECOND_NUMBER):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_SECOND_NUMBER)
         
        # --> OpenOrdersLimitDay ==> 1 to 3
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(DEFAULT_NUMBER + 1,
                                                                             int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
        
        # --> Time_closing_trades=false ==> 1/0
        # Check the special variable of Time_of_closing_in_hours 
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_NUMBER):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_SECOND_NUMBER)
                
                # --> only change value of Time_of_closing_in_hours ==> random 5 or 6 when Time_closing_trades==True/1
                self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(5, 6) 
                
                if self.genes[mutation_point + 1][VALUE_COL_INDEX] == '5':
                    self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(int(self.genes[mutation_point + 1][VALUE_COL_INDEX]),
                                                                                     int(self.genes[mutation_point + 1][VALUE_COL_INDEX]) + 1) 
                elif self.genes[mutation_point + 1][VALUE_COL_INDEX] == '6':
                    self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(int(self.genes[mutation_point + 1][VALUE_COL_INDEX] - 1),
                                                                                     int(self.genes[mutation_point + 1][VALUE_COL_INDEX]))
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER)
    
        # --> Profit_all_orders ==> 1 to 12
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(DEFAULT_NUMBER + 1,
                                                                             int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
        
        # --> Arrangements_of_trades ==> 1 to 25
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) + 1,
                                                                             DEFAULT_NUMBER - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
    
        # --> Lots ==> 0.01 to 0.1
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.uniform(float(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) * 2,
                                                                             MAX_LOTS)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
    
    
        # create the whole completed parameters for running EA
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
    
    #===============================================================================
    # Calculate fitness
    # TODO: CUSTOMISE THIS FUNCTION, in the meantime ==> randomly pick the value of HAPPY FOREX EA
    def cal_fitness(self):
        self.fitness = DEFAULT_NUMBER
        
        ''' 
        OLD CODE:
            # divide the total fitness (100) to 2 part (50/50)
            (self.net_profit, self.total_win) = happyforex_EA_instance.run()
            
            # adjust the net_profit & total_win
            if self.net_profit > NET_PROFIT:
                self.net_profit = NET_PROFIT
            
            if self.total_win > MAX_WIN_TOTAL_TRADE:
                self.total_win = MAX_WIN_TOTAL_TRADE
                
            self.fitness = round(50 * (self.net_profit / NET_PROFIT 
                                 + self.total_win / MAX_WIN_TOTAL_TRADE), 2)
        '''
        
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
        happyforex_EA_instance = HappyForexEA(self.genes_completed)
        
#         self.net_profit = happyforex_EA_instance.run_nothing()     # for testing only: randomly pick the value of HAPPYFOREX EA
        self.net_profit = happyforex_EA_instance.run()
        self.ORDER_CLOSED_DICT = happyforex_EA_instance.ORDER_CLOSED_DICT
        self.ORDER_OPENED_DICT = happyforex_EA_instance.ORDER_OPENED_DICT
        self.DATE_DATA_DICT = happyforex_EA_instance.DATE_DATA_DICT
        
        
        # calculate fitness for the HappyForex EA
        if self.net_profit > NET_PROFIT:
            self.net_profit = MAX_FITNESS
        else:
            self.fitness = round(100 * abs(self.net_profit) / NET_PROFIT, 2)
        
        
################################################################################
##########################           CLASS           ###########################
################################################################################
class Population(object):
    '''
    classdocs
    '''
    #===============================================================================
    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        
        # TODO: For testing only
        self.popSize = 5
        
        # TODO: UNCOMMENT when finishing testing
#         # reduce 1 for size of permutation due to the condition True/False of Time_closing_trades
#         letters = digits = len(OPTIMIZE_PARAMETERS_LIST) - 1  
#         self.popSize = permutation_count(letters, digits)

        self.fittest = DEFAULT_NUMBER
        self.individuals = [Individual()] * self.popSize
        self.individuals_ID_dict = {}  # a dictionary (as a hash-map) for storing ID
        
    #===============================================================================
    # Initialize population
    def initialize_population(self):
        for i in range(self.popSize):
            # create the individual with its attributes
            an_individual = Individual()
            an_individual.create_random_genes()
            new_id = an_individual.create_ind_uniqueID(self.individuals_ID_dict)

            # assign the individual with unique ID into population
            self.individuals[i] = an_individual
            self.individuals_ID_dict[new_id] = i 
            
    #===============================================================================
    # Get the highest fitness individual
    def get_fittest(self):
        max_fit = -sys.maxint - 1
        max_fit_index = DEFAULT_NUMBER
        
        for i in range(len(self.individuals)):
            if max_fit <= self.individuals[i].fitness:
                max_fit_index = i
                max_fit = self.individuals[i].fitness
        
        self.fittest = max_fit
        
        highest_fitness_ind = Individual()
        highest_fitness_ind.individual_ID = self.individuals[max_fit_index].individual_ID
        highest_fitness_ind.net_profit = self.individuals[max_fit_index].net_profit
        highest_fitness_ind.total_win = self.individuals[max_fit_index].total_win
        highest_fitness_ind.fitness = self.individuals[max_fit_index].fitness
        highest_fitness_ind.genes = copy_string_array(self.individuals[max_fit_index].genes)
        highest_fitness_ind.genes_completed = copy_string_array(self.individuals[max_fit_index].genes_completed)
        
        return highest_fitness_ind     
        
    #===============================================================================
    # Get the second most highest fitness individual
    def get_second_fittest(self):
        max_fit_1 = max_fit_2 = DEFAULT_NUMBER
        
        for i in range(len(self.individuals)):
            if self.individuals[i].fitness > self.individuals[max_fit_1].fitness:
                max_fit_2 = max_fit_1
                max_fit_1 = i
            elif self.individuals[i].fitness > self.individuals[max_fit_2].fitness:
                max_fit_2 = i
        
        highest_second_fitness_ind = Individual()
        highest_second_fitness_ind.individual_ID = self.individuals[max_fit_2].individual_ID
        highest_second_fitness_ind.net_profit = self.individuals[max_fit_2].net_profit
        highest_second_fitness_ind.total_win = self.individuals[max_fit_2].total_win
        highest_second_fitness_ind.fitness = self.individuals[max_fit_2].fitness
        highest_second_fitness_ind.genes = copy_string_array(self.individuals[max_fit_2].genes)
        highest_second_fitness_ind.genes_completed = copy_string_array(self.individuals[max_fit_2].genes_completed)
        
        return highest_second_fitness_ind 
    
    #===============================================================================
    # Get index of the least fitness individual
    def get_least_fittest(self):
        min_fitness = sys.maxint
        min_fitness_index = DEFAULT_NUMBER
        
        for i in range(len(self.individuals)):
            if min_fitness >= self.individuals[i].fitness:
                min_fitness = self.individuals[i].fitness
                min_fitness_index = i
        
        return min_fitness_index
    
    #===============================================================================
    # Get index of least fittest individual
    def calculate_fittest(self):
        for i in range(len(self.individuals)):
            self.individuals[i].cal_fitness()

    #===============================================================================
    
 
################################################################################
##########################           CLASS           ###########################
################################################################################
class HappyForexGenericAlgorithm(object):
    '''
    classdocs
    '''
 
    #===============================================================================
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.generationCount = DEFAULT_NUMBER
        self.population = Population()
        self.fittest_ind = Individual()
        self.second_fittest_ind = Individual()
        self.least_fittest_ind = Individual()
        self.added_offstring_ind = Individual()
        
    #===============================================================================
    # Selection
    def selection(self):
        # Select the most highest fitness individual 
        self.fittest_ind = self.population.get_fittest()
        
        # Select the second most highest fitness individual
        self.second_fittest_ind = self.population.get_second_fittest()
        
        
    #===============================================================================
    # Crossover
    def crossover(self):
        # Select a random crossover point, from 0 to 6 (make sure less than the length of OPTIMIZE_PARAMETERS_LIST)
        cross_over_point = random.randint(DEFAULT_NUMBER, len(OPTIMIZE_PARAMETERS_LIST) - 2);
        print("cross_over_point: %s" % cross_over_point)
        log.info("cross_over_point: %s" % cross_over_point)
        
        # Swap values among parents
        i = DEFAULT_NUMBER
        while i <= cross_over_point:
            temp = self.fittest_ind.genes[i]
            self.fittest_ind.genes[i] = self.second_fittest_ind.genes[i]
            self.second_fittest_ind.genes[i] = temp
            i += 1
        
        # Check the special variable of Time_of_closing_in_hours 
        # --> only change value of Time_of_closing_in_hours ==> random 5 or 6 when Time_closing_trades==True/1
        row_time_closing_index = 3
        row_time_of_closing_inhour_index = 4
        
        # In father's genes
        if self.fittest_ind.genes[row_time_closing_index][VALUE_COL_INDEX] == '1':
            if self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '5': 
                self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]),
                                                                                                     int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]) + 1) 
            elif self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '6':
                self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] - 1),
                                                                                                       int(self.fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]))
        # In mother's genes
        if self.second_fittest_ind.genes[row_time_closing_index][VALUE_COL_INDEX] == '1':
            if self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '5':
                self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]),
                                                                                                       int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]) + 1) 
            elif self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] == '6':
                self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] = random.randint(int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX] - 1),
                                                                                                    int(self.second_fittest_ind.genes[row_time_of_closing_inhour_index][VALUE_COL_INDEX]))

        # update individual ID
        new_id_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.fittest_ind.genes])
        self.fittest_ind.individual_ID = new_id_fittest
        
        new_id_second_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.second_fittest_ind.genes])
        self.second_fittest_ind.individual_ID = new_id_second_fittest
        
        
        # create the whole completed parameters for running EA
        self.fittest_ind.genes_completed = merge_2parametes_array_data(self.fittest_ind.genes_completed, self.fittest_ind.genes)
        self.second_fittest_ind.genes_completed = merge_2parametes_array_data(self.second_fittest_ind.genes_completed, self.second_fittest_ind.genes)
    

    #===============================================================================
    # Mutation
    def mutation(self):
        row_Time_of_closing_in_hours = 4
        
        # Select a random mutation point for fittest_ind  from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
        mutation_point_fittest = random.randint(DEFAULT_NUMBER, len(OPTIMIZE_PARAMETERS_LIST) - 1);
        
        # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
        if mutation_point_fittest == row_Time_of_closing_in_hours:
            mutation_point_fittest -= 1
        print("mutation_point_fittest: %s" % mutation_point_fittest) 
        log.info("mutation_point_fittest: %s" % mutation_point_fittest) 
        
        # Flip values at the mutation point
        self.fittest_ind.flip_value(mutation_point_fittest)
        
        # create the individual's ID which is the combination of all Values of parameters
        id_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.fittest_ind.genes])
        
        # keep create an individual while the ID is not unique
        while (id_fittest in self.population.individuals_ID_dict == True):
            # Select a random mutation point from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
            mutation_point_fittest = random.randint(DEFAULT_NUMBER, len(OPTIMIZE_PARAMETERS_LIST) - 1);
            
            # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
            if mutation_point_fittest == row_Time_of_closing_in_hours:
                mutation_point_fittest -= 1
            print("mutation_point_fittest in loops: %s" % mutation_point_fittest) 
            log.info("mutation_point_fittest in loops: %s" % mutation_point_fittest) 
            
            # Flip values at the mutation point
            self.fittest_ind.flip_value(mutation_point_fittest)
            
            id_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.fittest_ind.genes])
        
        # update individual ID
        self.fittest_ind.individual_ID = id_fittest
    
        
        # Select a random mutation point for second_fittest_ind from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
        mutation_point_second_fittest = random.randint(DEFAULT_NUMBER, len(OPTIMIZE_PARAMETERS_LIST) - 1);
        
        # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
        if mutation_point_second_fittest == row_Time_of_closing_in_hours:
            mutation_point_second_fittest -= 1
        print("mutation_point_second_fittest: %s" % mutation_point_second_fittest) 
        log.info("mutation_point_second_fittest: %s" % mutation_point_second_fittest) 
            
        # Flip values at the mutation point
        self.second_fittest_ind.flip_value(mutation_point_second_fittest)
    
        # create the individual's ID which is the combination of all Values of parameters
        id_second_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.second_fittest_ind.genes])
        
        # keep create an individual while the ID is not unique
        while (id_second_fittest in self.population.individuals_ID_dict == True):
            # Select a random mutation point from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
            mutation_point_second_fittest = random.randint(DEFAULT_NUMBER, len(OPTIMIZE_PARAMETERS_LIST) - 1);
            
            # Change Time_of_closing_in_hours row into Time_closing_trades row for satisfying the condition of Time_closing_trades row 
            if mutation_point_second_fittest == row_Time_of_closing_in_hours:
                mutation_point_second_fittest -= 1
            print("mutation_point_second_fittest in loops: %s" % mutation_point_second_fittest) 
            log.info("mutation_point_second_fittest in loops: %s" % mutation_point_second_fittest) 
            
            # Flip values at the mutation point
            self.second_fittest_ind.flip_value(mutation_point_second_fittest)
            
            id_second_fittest = '_' . join([str(row[VALUE_COL_INDEX]) for row in self.second_fittest_ind.genes])
        
        
        # update individual ID
        self.second_fittest_ind.individual_ID = id_second_fittest
        
        
    #===============================================================================
    # Get the highest fitness offspring
    def get_fittest_offspring(self):
        if self.fittest_ind.fitness > self.second_fittest_ind.fitness:
            return self.fittest_ind
        
        return self.second_fittest_ind
    
    #===============================================================================
    # Replace least fitness individual from most highest fitness offspring
    def add_fittest_offspring(self):
        # Update fitness values of offspring (after crossover and mutation)
        self.fittest_ind.cal_fitness()
        self.second_fittest_ind.cal_fitness()
        
        # Get index of least fit individual
        least_fittest_index = self.population.get_least_fittest()
        
        # Retrieve the least fitness and the highest fitness offspring
        self.least_fittest_ind = self.population.individuals[least_fittest_index]
        self.added_offstring_ind = self.get_fittest_offspring()
       
        # Replace least fitness individual by the highest fitness offspring
        self.population.individuals[least_fittest_index] = self.added_offstring_ind
        
        # update individuals_ID_dict
        value_least_fittest_ind = self.population.individuals_ID_dict[self.least_fittest_ind.individual_ID]
        del self.population.individuals_ID_dict[self.least_fittest_ind.individual_ID]
        self.population.individuals_ID_dict[self.added_offstring_ind.individual_ID] = value_least_fittest_ind

