'''
Created on Dec 22, 2017

@author: cao.vu.lam
'''
#!/usr/bin/env python

import random
import sys
import logging.handlers
import shutil
import os
from datetime import datetime
from os import path, remove
from StrategyTesterModule.happyforex_ST import HappyForexEA
from multiprocessing.dummy import Pool as ThreadPool

from DataHandler.hardcoded_data import MAX_LOTS, NET_PROFIT, MAX_FITNESS, \
                                    OPTIMIZED_PARAMETERS_DATA, OPTIMIZE_PARAMETERS_LIST, \
                                    VALUE_COL_INDEX, DEFAULT_SECOND_NUMBER_INT, DEFAULT_PARAMETERS_DATA, \
                                    copy_string_array, permutation_count, merge_2parametes_array_data, \
                                    DEFAULT_NUMBER_INT, FOLDER_DATA_OUTPUT, SYMBOL, \
                                    FILENAME_HIGHEST_FITNESS, FILENAME_BEST_SOLUTION, FILENAME_BEST_PARAMETERS, \
                                    FILENAME_POPULATION_INITIAL, FILENAME_POPULATION_FINAL, \
                                    FILENAME_ORDER_CLOSED_HISTORY, FILENAME_ORDER_OPENED_HISTORY, \
                                    FILENAME_HIGHEST_PARAMETERS, TIME_STAMP_FORMAT, \
                                    FILENAME_LOG_BACKTEST, FILENAME_PROFILE_BACKTEST, FILENAME_ORDER_DELETED_HISTORY, \
                                    write_wholedict2csv_no_header, write_array2csv_with_delimiter_no_header, \
                                    display_an_array_with_delimiter, \
    DEFAULT_NUMBER_FLOAT
import cProfile
import multiprocessing

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
        self.net_profit = DEFAULT_NUMBER_INT
        self.total_win = DEFAULT_NUMBER_INT
        self.fitness = DEFAULT_NUMBER_INT
        self.individual_ID = str(DEFAULT_NUMBER_INT)
       
        # copy optimize-needed and default parameters for each individual to become its genes
        self.genes = copy_string_array(OPTIMIZED_PARAMETERS_DATA)
        self.genes_completed = copy_string_array(DEFAULT_PARAMETERS_DATA)
        
        # create dictionaries for storing orders pools 
        self.ORDER_CLOSED_DICT = {} 
        self.ORDER_OPENED_DICT = {} 
        self.ORDER_DELETED_DICT = {}
        
    #===============================================================================
    def create_a_set_of_genes(self):
        # reset genes for each individual
        row = DEFAULT_NUMBER_INT
        col = 1
        
        # --> FilterSpread ==> pickup value 1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT, sys.maxint) % 2  
        row += 1
        # --> Friday ==> pickup value  1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT, sys.maxint) % 2  
        row += 1
        # --> OpenOrdersLimitDay ==> pickup value 1 to 3
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT + 1, int(self.genes[row][col]))  
        row += 1
        # --> Time_closing_trades ==> pickup value 1 or 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT, sys.maxint) % 2  
        # --> only change value of Time_of_closing_in_hours ==> pickup value 5 or 6 when Time_closing_trades==True
        if self.genes[row][col] == '1':
            row += 1
            self.genes[row][col] = random.randint(int(self.genes[row][col]), int(self.genes[row][col]) + 1) 
        else:
            row += 2
        # --> Profit_all_orders ==> pickup value 1 to 12 0
        self.genes[row][col] = random.randint(DEFAULT_NUMBER_INT + 1, int(self.genes[row][col]))  
        row += 1
        # --> Arrangements_of_trades ==> pickup value 1 or 25
        random_num = random.randint(DEFAULT_NUMBER_INT + 1, abs(int(self.genes[row][col])))
        self.genes[row][col] = random_num * (-1)  
        row += 1
        # --> Lots ==> pickup value 0.01 to 0.1
        random_num = random.uniform(float(self.genes[row][col]), MAX_LOTS)
        self.genes[row][col] = round(random_num, 2)  
        
        # create the whole completed parameters for running EA
        self.genes_completed = merge_2parametes_array_data(self.genes_completed, self.genes)
    
    #===============================================================================

    '''
    manual_parameters_list = ['FilterSpread', 'Friday', 'OpenOrdersLimitDay', 'Time_closing_trades', 'Time_of_closing_in_hours',
                       'Profit_all_orders', 'Arrangements_of_trades', 'Lots']
    '''

    def create_a_fixed_set_genes(self, manual_parameters_list):
        # reset genes randomly for each individual
        row = DEFAULT_NUMBER_INT
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
            self.create_a_set_of_genes()
            new_id = '_' . join([str(row[col_index_value]) for row in self.genes])
        
        # assign the new ID to an individual
        self.individual_ID = new_id
           
        return new_id
    
    #===============================================================================
    def flip_value(self, mutation_point):
        
        key_col_index = DEFAULT_NUMBER_INT
         
        # Flip values at the mutation point
        # --> FilterSpread=true (default) ==> 1/0
        if self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_SECOND_NUMBER_INT):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
         
        # --> Friday=true (default) ==> 1/0
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_SECOND_NUMBER_INT):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_SECOND_NUMBER_INT)
         
        # --> OpenOrdersLimitDay ==> 1 to 3
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(DEFAULT_NUMBER_INT + 1,
                                                                             int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
        
        # --> Time_closing_trades=false ==> 1/0
        # Check the special variable of Time_of_closing_in_hours 
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == str(DEFAULT_NUMBER_INT):
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_SECOND_NUMBER_INT)
                
                # --> only change value of Time_of_closing_in_hours ==> pickup value 5 or 6 when Time_closing_trades==True/1
                self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(5, 6) 
                
                if self.genes[mutation_point + 1][VALUE_COL_INDEX] == '5':
                    self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(int(self.genes[mutation_point + 1][VALUE_COL_INDEX]),
                                                                                     int(self.genes[mutation_point + 1][VALUE_COL_INDEX]) + 1) 
                elif self.genes[mutation_point + 1][VALUE_COL_INDEX] == '6':
                    self.genes[mutation_point + 1][VALUE_COL_INDEX] = random.randint(int(self.genes[mutation_point + 1][VALUE_COL_INDEX] - 1),
                                                                                     int(self.genes[mutation_point + 1][VALUE_COL_INDEX]))
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = str(DEFAULT_NUMBER_INT)
    
        # --> Profit_all_orders ==> 1 to 12
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(DEFAULT_NUMBER_INT + 1,
                                                                             int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) - 1)
            else:
                self.genes[mutation_point][VALUE_COL_INDEX] = OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]
        
        # --> Arrangements_of_trades ==> 1 to 25
        elif self.genes[mutation_point][key_col_index] == OPTIMIZED_PARAMETERS_DATA[mutation_point][key_col_index]:
            if self.genes[mutation_point][VALUE_COL_INDEX] == OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]:
                self.genes[mutation_point][VALUE_COL_INDEX] = random.randint(int(OPTIMIZED_PARAMETERS_DATA[mutation_point][VALUE_COL_INDEX]) + 1,
                                                                             DEFAULT_NUMBER_INT - 1)
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

        self.fittest = DEFAULT_NUMBER_INT
        self.individuals = [Individual()] * self.popSize
        self.individuals_ID_dict = {}  # a dictionary (as a hash-map) for storing ID
        self.FITNESS_DICT = {}  # a dictionary for storing fitness of all individuals
 
        # create an instance of EA for running 
        self.happyforex_EA_instance = HappyForexEA()
        
    #===============================================================================
    # Initialize population
    def initialize_population(self):
        for i in range(self.popSize):
            # create the individual with its attributes
            an_individual = Individual()
            an_individual.create_a_set_of_genes()
            new_id = an_individual.create_ind_uniqueID(self.individuals_ID_dict)

            # assign the individual with unique ID into population
            self.individuals[i] = an_individual
            self.individuals_ID_dict[new_id] = i 
            
#             # add the genes completed to the pool
#             self.all_genes_pool[an_individual.genes_completed] = i
            
    #===============================================================================
    # Get the highest fitness individual
    def get_fittest(self):
        max_fit = -sys.maxint - 1
        max_fit_index = DEFAULT_NUMBER_INT
        
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
        max_fit_1 = max_fit_2 = DEFAULT_NUMBER_INT
        
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
        min_fitness_index = DEFAULT_NUMBER_INT
        
        for i in range(len(self.individuals)):
            if min_fitness >= self.individuals[i].fitness:
                min_fitness = self.individuals[i].fitness
                min_fitness_index = i
        
        return min_fitness_index
    
    #===============================================================================
    # Calculate the fitness of each individual
    def cal_fitness(self, Individual):
        
        Individual.fitness = DEFAULT_NUMBER_INT
        
        # run the EA logic to return the profit
        Individual.net_profit = self.happyforex_EA_instance.run(Individual.genes_completed, Individual.individual_ID)
#         Individual.net_profit = self.happyforex_EA_instance.run_testing()
        Individual.ORDER_CLOSED_DICT = self.happyforex_EA_instance.ORDER_CLOSED_DICT
        Individual.ORDER_OPENED_DICT = self.happyforex_EA_instance.ORDER_OPENED_DICT
        Individual.ORDER_DELETED_DICT = self.happyforex_EA_instance.ORDER_DELETED_DICT
        
        # save profit to dictionary
        self.FITNESS_DICT[str(Individual.individual_ID) + '_origin'] = round(Individual.net_profit, 2)
        
        # calculate fitness for the HappyForex EA
        if Individual.net_profit > NET_PROFIT:
            Individual.fitness = MAX_FITNESS
        else:
            if Individual.net_profit <= DEFAULT_NUMBER_FLOAT:
                Individual.fitness = DEFAULT_NUMBER_FLOAT
            else:
                Individual.fitness = round(100 * Individual.net_profit / NET_PROFIT, 2)
            
        return Individual
            
    #===============================================================================
    # Calculate the fitness of each individual
    def calculate_fittest(self):
        
        ''' MONOTHREADING
        for ind_ in self.individuals:
            ind_ = self.cal_fitness(ind_)
        MONOTHREADING '''

        ''' MULTITHREADING '''
        # make the Pool of workers
        pool_size = multiprocessing.cpu_count()
        ea_pool = ThreadPool(pool_size)
        
        # and return the all_fitness_results
#         individuals_w_fitness = ea_pool.map(self.cal_fitness, self.individuals)
        results = [ea_pool.apply_async(self.cal_fitness, (ind_,)) for ind_ in self.individuals]
         
        # --> proxy.get() waits for task completion and returns the result
        individuals_w_fitness = [r.get() for r in results]  
        self.individuals = individuals_w_fitness
         
        # close the pool and wait for the work to finish 
        ea_pool.close() 
#         ea_pool.join() 
        ''' MULTITHREADING '''
        
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
        
        self.generationCount = DEFAULT_NUMBER_INT
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
        # Select a crossover point, from 0 to 6 (make sure less than the length of OPTIMIZE_PARAMETERS_LIST)
        cross_over_point = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 2);
        print("cross_over_point: %s" % cross_over_point)
        log.info("cross_over_point: %s" % cross_over_point)
        
        # Swap values among parents
        i = DEFAULT_NUMBER_INT
        while i <= cross_over_point:
            temp = self.fittest_ind.genes[i]
            self.fittest_ind.genes[i] = self.second_fittest_ind.genes[i]
            self.second_fittest_ind.genes[i] = temp
            i += 1
        
        # Check the special variable of Time_of_closing_in_hours 
        # --> only change value of Time_of_closing_in_hours ==> pickup value 5 or 6 when Time_closing_trades==True/1
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
        
        # Select a mutation point for fittest_ind  from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
        mutation_point_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
        
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
            # Select a mutation point from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
            mutation_point_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
            
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
        
        # Select a mutation point for second_fittest_ind from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
        mutation_point_second_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
        
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
            # Select a mutation point from 0 to 7 (less than the length of OPTIMIZE_PARAMETERS_LIST)
            mutation_point_second_fittest = random.randint(DEFAULT_NUMBER_INT, len(OPTIMIZE_PARAMETERS_LIST) - 1);
            
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
        self.fittest_ind.genes_completed = merge_2parametes_array_data(self.fittest_ind.genes_completed,
                                                                       self.fittest_ind.genes)
        self.second_fittest_ind.genes_completed = merge_2parametes_array_data(self.second_fittest_ind.genes_completed,
                                                                       self.second_fittest_ind.genes)
        
        ''' MONOTHREADING
        # Calculate fitness for these high fitness individuals
        self.fittest_ind = self.population.cal_fitness(self.fittest_ind)
        self.second_fittest_ind = self.population.cal_fitness(self.second_fittest_ind)
        MONOTHREADING ''' 
        
        highest_individuals = [self.fittest_ind, self.second_fittest_ind]
        
        ''' MULTITHREADING '''
        # make the Pool of workers
        pool_size = multiprocessing.cpu_count()
        ea_pool = ThreadPool(pool_size)
        
        # and return the all_fitness_results
        results = [ea_pool.apply_async(self.population.cal_fitness, (ind_,)) for ind_ in highest_individuals]
         
        # --> proxy.get() waits for task completion and returns the result
        individuals_w_fitness = [r.get() for r in results]  
        self.fittest_ind = individuals_w_fitness[DEFAULT_NUMBER_INT]
        self.second_fittest_ind = individuals_w_fitness[DEFAULT_SECOND_NUMBER_INT]
         
        # close the pool and wait for the work to finish 
        ea_pool.close() 
        ''' MULTITHREADING '''
        
        # Get index of least fit individual to retrieve that individual
        least_fittest_index = self.population.get_least_fittest()
        self.least_fittest_ind = self.population.individuals[least_fittest_index]
        
        # Save profit to dictionary
        self.population.FITNESS_DICT[str(self.added_offstring_ind.individual_ID) + '_eliminated'] = round(self.added_offstring_ind.net_profit, 2)
        
        # Retrieve the highest fitness offspring
        self.added_offstring_ind = self.get_fittest_offspring()
       
        # Replace least fitness individual by the highest fitness offspring
        self.population.individuals[least_fittest_index] = self.added_offstring_ind
        
        # Update individuals_ID_dict
        value_least_fittest_ind = self.population.individuals_ID_dict[self.least_fittest_ind.individual_ID]
        del self.population.individuals_ID_dict[self.least_fittest_ind.individual_ID]
        self.population.individuals_ID_dict[self.added_offstring_ind.individual_ID] = value_least_fittest_ind

        # Save profit to dictionary
        self.population.FITNESS_DICT[str(self.added_offstring_ind.individual_ID) + '_added'] = round(self.added_offstring_ind.net_profit, 2)
        
################################################################################
################################           FUNCTIONS           ##################################
################################################################################


#===============================================================================
def ga_run():
    # Create an instance for HappyForexGenericAlgorithm to run the program
    happyforexGA = HappyForexGenericAlgorithm()
    
    # Create an folder for storing all outputs in this section 
    folder_output = FOLDER_DATA_OUTPUT + SYMBOL + '_optimization_output/'
    if os.path.exists(folder_output):
        shutil.rmtree(folder_output)
    os.makedirs(folder_output)
    
    # Initialize population
    log.info('#============================== Initialize population ==============================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#============================== %s Initialize population ==============================' % time_stamp)
    happyforexGA.population.initialize_population()
    
    log.info('==> population size: %s' % happyforexGA.population.popSize)
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('%s ==> population size: %s' % (time_stamp, happyforexGA.population.popSize))
    
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    log.info('#============================================================')
    log.info('==> first individual genes and genes_completed:')
    print('#============================================================')
    print('%s ==> first individual genes and genes_completed:' % time_stamp)
    display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER_INT].genes_completed, '=')
    log.info('#============================================================')
    print('#============================================================')
    display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER_INT].genes, '=')
    
    # Write the individual_ID_list to a CSV file for reference
    log.info('#============================== Write the individual_ID_list to a CSV file ==============================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#============================== %s Write the individual_ID_list to a CSV file ==============================' % time_stamp)
    write_wholedict2csv_no_header(happyforexGA.population.individuals_ID_dict, folder_output + FILENAME_POPULATION_INITIAL)
     
    # Calculate fitness of each individual
    log.info('#============================== Calculate fitness of each individual ==============================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#============================== %s Calculate fitness of each individual ==============================' % time_stamp)
    happyforexGA.population.calculate_fittest()

    # Get the individual with highest fitness ==> retrieve the highest fitness for the population
    log.info('#============================== Get the individual with highest fitness ==============================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#============================== %s Get the individual with highest fitness ==============================' % time_stamp)
    happyforexGA.fittest_ind = happyforexGA.population.get_fittest()
           
    log.info('#============================== Population gets an individual with maximum fitness ==============================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#============================== %s Population gets an individual with maximum fitness ==============================' % time_stamp)
    # While population gets an individual with maximum fitness or the population has converged (does not produce different offspring)
    while (happyforexGA.population.fittest < MAX_FITNESS 
            and happyforexGA.generationCount < happyforexGA.population.popSize * 2):  # TODO: for testing only
        
        happyforexGA.generationCount += 1
           
        # Do selection
        log.info('#============================== population selection ==============================')
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#============================== %s population selection ==============================' % time_stamp)
        happyforexGA.selection()
        
        print("==> self.fittest_ind.individual_ID at selection: %s" % happyforexGA.fittest_ind.individual_ID)
        print("==> self.second_fittest_ind.individual_ID at selection: %s" % happyforexGA.second_fittest_ind.individual_ID)
        log.info("==> self.fittest_ind.individual_ID at selection: %s" % happyforexGA.fittest_ind.individual_ID)
        log.info("==> self.second_fittest_ind.individual_ID at selection: %s" % happyforexGA.second_fittest_ind.individual_ID)
           
        # Do crossover
        log.info('#============================== population crossover ==============================')
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print('#============================== %s population crossover ==============================' % time_stamp)
        happyforexGA.crossover()
        
        print("==> self.fittest_ind.individual_ID after crossover: %s" % happyforexGA.fittest_ind.individual_ID)
        print("==> self.second_fittest_ind.individual_ID after crossover: %s" % happyforexGA.second_fittest_ind.individual_ID)
        log.info("==> self.fittest_ind.individual_ID after crossover: %s" % happyforexGA.fittest_ind.individual_ID)
        log.info("==> self.second_fittest_ind.individual_ID after crossover: %s" % happyforexGA.second_fittest_ind.individual_ID)
           
        # Do mutation under probability
        if random.randint(DEFAULT_NUMBER_INT, MAX_FITNESS) < MAX_FITNESS:
            
            log.info('#============================== population mutation ==============================')
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            print('#============================== %s population mutation ==============================' % time_stamp)
            happyforexGA.mutation()
            
            print("==> self.fittest_ind.individual_ID after mutation: %s" % happyforexGA.fittest_ind.individual_ID)
            print("==> self.second_fittest_ind.individual_ID after mutation: %s" % happyforexGA.second_fittest_ind.individual_ID)
            log.info("==> self.fittest_ind.individual_ID after mutation: %s" % happyforexGA.fittest_ind.individual_ID)
            log.info("==> self.second_fittest_ind.individual_ID after mutation: %s" % happyforexGA.second_fittest_ind.individual_ID)
                   
        # Add highest fitness offspring to population
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        happyforexGA.add_fittest_offspring()
        print("==> Least_fittest_ind.individual_ID: %s" % happyforexGA.least_fittest_ind.individual_ID)
        print("... ==> least_fittest_ind.fitness: %s" % happyforexGA.least_fittest_ind.fitness)                   
        print("... replace by highest fitness offspring individual ==> added_offstring_ind.individual_ID: %s" % happyforexGA.added_offstring_ind.individual_ID)
        print("... ==> added_offstring_ind.fitness: %s" % happyforexGA.added_offstring_ind.fitness)                   
        log.info("==> Least_fittest_ind.individual_ID: %s" % happyforexGA.least_fittest_ind.individual_ID)
        log.info("... ==> least_fittest_ind.fitness: %s" % happyforexGA.least_fittest_ind.fitness)                   
        log.info("... replace by highest fitness offspring individual ==> added_offstring_ind.individual_ID: %s" % happyforexGA.added_offstring_ind.individual_ID)
        log.info("... ==> added_offstring_ind.fitness: %s" % happyforexGA.added_offstring_ind.fitness)                   
        
#             # Calculate new fitness value
#             happyforexGA.population.calculate_fittest()
         
        # Get the new individual with highest fitness ==> retrieve the highest fitness for the population
        happyforexGA.fittest_ind = happyforexGA.population.get_fittest()
        
        # Print out and write to CSV file the highest solution + remove the old highest solution file
        log.info("Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        print("%s Generation: %s - Highest Fitness: %s" % (time_stamp, happyforexGA.generationCount, happyforexGA.population.fittest))
        
        if happyforexGA.fittest_ind.fitness < MAX_FITNESS:
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            file_path_highest_solution = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_HIGHEST_FITNESS
            file_path_highest_parameters = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_HIGHEST_PARAMETERS
        
            write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
            write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, file_path_highest_parameters, '=')
        
        write_wholedict2csv_no_header(happyforexGA.population.FITNESS_DICT, folder_output + 'profit_list.csv')
        
        print('#===========================================================================')
        log.info('#===========================================================================')
        
    # Print out and write to CSV file the best solution
    log.info('#===========================================================================')
    log.info("==> Solution found in generation: %s" % happyforexGA.generationCount);
    log.info("Fitness: %s" % happyforexGA.fittest_ind.fitness);
    log.info("Individual_ID: %s" % happyforexGA.fittest_ind.individual_ID)
    log.info("Genes: %s" % happyforexGA.fittest_ind.genes);
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#===========================================================================')
    print("%s ==> Solution found in generation: %s" % (time_stamp, happyforexGA.generationCount))
    print("Fitness: %s" % happyforexGA.fittest_ind.fitness);
    print("Individual_ID: %s" % happyforexGA.fittest_ind.individual_ID)
    print("Genes: %s" % happyforexGA.fittest_ind.genes);
    
    # Write out the whole best parameters
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_BEST_SOLUTION, '=')
    write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_$' + str(happyforexGA.fittest_ind.net_profit) + '_' + SYMBOL + FILENAME_BEST_PARAMETERS, '=')
    
    # Write the population final to a CSV file for reference
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    log.info('#============================== Write the population final to a CSV file ==============================')
    print('#============================== %s Write the population final to a CSV file ==============================' % time_stamp)
    write_wholedict2csv_no_header(happyforexGA.population.individuals_ID_dict,
                             folder_output + FILENAME_POPULATION_FINAL.replace(".csv", "_" + str(happyforexGA.generationCount) + "th_gen.csv"))

################################################################################
##########################           MAIN           ############################
################################################################################        


#============================================================
if __name__ == '__main__': 

#     ga_run()
    
    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile(FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST):
        remove(FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST)
         
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", FOLDER_DATA_OUTPUT + FILENAME_LOG_BACKTEST))
     
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
     
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
     
    try:
        # running ST
        cProfile.run('ga_run()', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_BACKTEST)
         
    except Exception:
        logging.exception("Exception in main")
        exit(1) 

