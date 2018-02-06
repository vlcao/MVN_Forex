'''
Created on Dec 22, 2017

@author: cao.vu.lam
'''
#!/usr/bin/env python

import logging.handlers
import random
import shutil
import os
from datetime import datetime
from os import path, remove
from GenericAlgorithmModule.happyforex_GA import HappyForexGenericAlgorithm
from DataHandler.hardcoded_data import DEFAULT_NUMBER, MAX_FITNESS, FOLDER_DATA_OUTPUT, SYMBOL, \
                                    FILENAME_HIGHEST_FITNESS, FILENAME_BEST_SOLUTION, FILENAME_BEST_PARAMETERS, \
                                    FILENAME_POPULATION_INITIAL, FILENAME_POPULATION_FINAL, \
                                    FILENAME_ORDER_CLOSED_HISTORY, FILENAME_ORDER_OPENED_HISTORY, \
                                    FILENAME_HIGHEST_PARAMETERS, FILENAME_DATE_DICT, TIME_STAMP_FORMAT, \
                                    write_dict2csv_no_header, write_array2csv_with_delimiter_no_header, \
                                    display_an_array_with_delimiter, \
    FILENAME_LOG_BACKTEST, FILENAME_PROFILE_BACKTEST, \
    FILENAME_ORDER_DELETED_HISTORY
import cProfile

log = logging.getLogger(__name__)


#===============================================================================
def main():
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
    
    log.info('#============================================================')
    log.info('==> first individual genes and genes_completed:')
    print('#============================================================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('%s ==> first individual genes and genes_completed:' % time_stamp)
    display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER].genes_completed, '=')
    display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER].genes, '=')
    
    # Write the individual_ID_list to a CSV file for reference
    log.info('#============================== Write the individual_ID_list to a CSV file ==============================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#============================== %s Write the individual_ID_list to a CSV file ==============================' % time_stamp)
    write_dict2csv_no_header(happyforexGA.population.individuals_ID_dict, folder_output + FILENAME_POPULATION_INITIAL)
     
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
    
    # Print out and write to CSV file the highest solution
    log.info("==> Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print("%s ==> Generation: %s - Highest Fitness: %s" % (time_stamp, happyforexGA.generationCount, happyforexGA.population.fittest))
    if happyforexGA.fittest_ind.fitness < MAX_FITNESS:
        
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        file_path_highest_solution = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + SYMBOL + FILENAME_HIGHEST_FITNESS
        file_path_highest_parameters = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_' + SYMBOL + FILENAME_HIGHEST_PARAMETERS
        
        write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
        write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, file_path_highest_parameters, '=')
        write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_CLOSED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_CLOSED_HISTORY)
        write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_OPENED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_OPENED_HISTORY)
        write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_DELETED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_DELETED_HISTORY)
           
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
           
        # Do mutation under a random probability
        if random.randint(DEFAULT_NUMBER, MAX_FITNESS) < MAX_FITNESS:
            
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
            if path.isfile(file_path_highest_solution):
                remove(file_path_highest_solution)
            
            time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
            file_path_highest_solution = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_' + SYMBOL + FILENAME_HIGHEST_FITNESS
            file_path_highest_parameters = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_' + SYMBOL + FILENAME_HIGHEST_PARAMETERS
        
            write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
            write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, file_path_highest_parameters, '=')
            write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_CLOSED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_CLOSED_HISTORY)
            write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_OPENED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_OPENED_HISTORY)
            write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_DELETED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_DELETED_HISTORY)
        
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
    
    # Write out the whole best parameters (converted back 1/0 in the data into True/False)
    
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, folder_output + time_stamp + '_' + SYMBOL + FILENAME_BEST_SOLUTION, '=')
    write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, folder_output + time_stamp + '_' + SYMBOL + FILENAME_BEST_PARAMETERS, '=')
    
    write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_CLOSED_DICT, folder_output + time_stamp + '_' + FILENAME_ORDER_CLOSED_HISTORY)
    write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_OPENED_DICT, folder_output + time_stamp + '_' + FILENAME_ORDER_OPENED_HISTORY)
    write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_DELETED_DICT, folder_output + time_stamp + '_' + FILENAME_ORDER_DELETED_HISTORY)
        
    # Write the population final to a CSV file for reference
    log.info('#============================== Write the population final to a CSV file ==============================')
    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    print('#============================== %s Write the population final to a CSV file ==============================' % time_stamp)
    write_dict2csv_no_header(happyforexGA.population.individuals_ID_dict,
                             folder_output + "%sth_generation_" % happyforexGA.generationCount + FILENAME_POPULATION_FINAL)


################################################################################
##########################           MAIN           ############################
################################################################################        
if __name__ == '__main__': 
    
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
        cProfile('main()', FOLDER_DATA_OUTPUT + FILENAME_PROFILE_BACKTEST)
        
    except Exception:
        logging.exception("Exception in main")
        exit(1) 
  
