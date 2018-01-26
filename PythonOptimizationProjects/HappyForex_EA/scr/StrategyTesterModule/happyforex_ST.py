'''
Created on Dec 22, 2017

@author: cao.vu.lam
'''
#!/usr/bin/env python

from datetime import datetime
import logging.handlers
import random
import shutil
import os

from os import path, remove
from GenericAlgorithmModule.happyforex_GA import HappyForexGenericAlgorithm
from DataHandler.happyforex_Datahandler import DEFAULT_NUMBER, MAX_FITNESS, FOLDER_DATA_OUTPUT, SYMBOL, \
                                    FILENAME_HIGHEST_FITNESS, FILENAME_BEST_SOLUTION, FILENAME_BEST_PARAMETERS, \
                                    FILENAME_POPULATION_INITIAL, FILENAME_POPULATION_FINAL, \
                                    FILENAME_ORDER_CLOSED_HISTORY, FILENAME_ORDER_OPENED_HISTORY, \
                                    FILENAME_HIGHEST_PARAMETERS, FILENAME_DATE_DICT, TIME_STAMP_FORMAT, \
                                    write_dict2csv_no_header, write_array2csv_with_delimiter_no_header, \
                                    display_an_array_with_delimiter

log = logging.getLogger(__name__)


################################################################################
##########################           MAIN           ############################
################################################################################        
if __name__ == '__main__': 
    
    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile(FOLDER_DATA_OUTPUT + "HappyForexBackTests.log"):
        remove(FOLDER_DATA_OUTPUT + "HappyForexBackTests.log")
        
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", FOLDER_DATA_OUTPUT + "HappyForexBackTests.log"))
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
    
    try:
        
        # Create an instance for HappyForexGenericAlgorithm to run the program
        happyforexGA = HappyForexGenericAlgorithm()
        
        # Create an folder for storing all outputs in this section 
        folder_output = FOLDER_DATA_OUTPUT + SYMBOL + '_optimization_output/'
        if os.path.exists(folder_output):
            shutil.rmtree(folder_output)
        os.makedirs(folder_output)
        
        # Initialize population
        print('#============================== Initialize population ==============================')
        log.info('#============================== Initialize population ==============================')
        happyforexGA.population.initialize_population()
        print('==> population size: {0}'.format(happyforexGA.population.popSize))
        log.info('==> population size: {0}'.format(happyforexGA.population.popSize))
        
        print('#============================================================')
        print('==> first individual genes and genes_completed:')
        display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER].genes_completed, '=')
        print('#============================================================')
        log.info('#============================================================')
        display_an_array_with_delimiter(happyforexGA.population.individuals[DEFAULT_NUMBER].genes, '=')
        
        
        # Write the individual_ID_list to a CSV file for reference
        print('#============================== Write the individual_ID_list to a CSV file ==============================')
        log.info('#============================== Write the individual_ID_list to a CSV file ==============================')
        write_dict2csv_no_header(happyforexGA.population.individuals_ID_dict, folder_output + FILENAME_POPULATION_INITIAL)
        
         
        # Calculate fitness of each individual
        print('#============================== Calculate fitness of each individual ==============================')
        log.info('#============================== Calculate fitness of each individual ==============================')
        happyforexGA.population.calculate_fittest()
        

        # Get the individual with highest fitness ==> retrieve the highest fitness for the population
        print('#============================== Get the individual with highest fitness ==============================')
        log.info('#============================== Get the individual with highest fitness ==============================')
        happyforexGA.fittest_ind = happyforexGA.population.get_fittest()
        
        
        # Print out and write to CSV file the highest solution
        print("==> Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
        log.info("==> Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
        if happyforexGA.fittest_ind.fitness < MAX_FITNESS:
            
            time_stamp = str(datetime.now().strftime(TIME_STAMP_FORMAT))
            file_path_highest_solution = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + FILENAME_HIGHEST_FITNESS
            file_path_highest_parameters = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_HIGHEST_PARAMETERS
            
            write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
            write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, file_path_highest_parameters, '=')
            write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_CLOSED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_CLOSED_HISTORY)
            write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_OPENED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_OPENED_HISTORY)
    
         
               
        print('#============================== Population gets an individual with maximum fitness ==============================')
        log.info('#============================== Population gets an individual with maximum fitness ==============================')
        # While population gets an individual with maximum fitness or the population has converged (does not produce different offspring)
        while (happyforexGA.population.fittest < MAX_FITNESS 
                and happyforexGA.generationCount < happyforexGA.population.popSize * 2):  # TODO: for testing only
            
            happyforexGA.generationCount += 1
               
            # Do selection
            happyforexGA.selection()
            print("==> self.fittest_ind.individual_ID at selection: %s" % happyforexGA.fittest_ind.individual_ID)
            print("==> self.second_fittest_ind.individual_ID at selection: %s" % happyforexGA.second_fittest_ind.individual_ID)
            log.info("==> self.fittest_ind.individual_ID at selection: %s" % happyforexGA.fittest_ind.individual_ID)
            log.info("==> self.second_fittest_ind.individual_ID at selection: %s" % happyforexGA.second_fittest_ind.individual_ID)
            
               
            # Do crossover
            happyforexGA.crossover()
            print("==> self.fittest_ind.individual_ID after crossover: %s" % happyforexGA.fittest_ind.individual_ID)
            print("==> self.second_fittest_ind.individual_ID after crossover: %s" % happyforexGA.second_fittest_ind.individual_ID)
            log.info("==> self.fittest_ind.individual_ID after crossover: %s" % happyforexGA.fittest_ind.individual_ID)
            log.info("==> self.second_fittest_ind.individual_ID after crossover: %s" % happyforexGA.second_fittest_ind.individual_ID)
            
               
            # Do mutation under a random probability
            if random.randint(DEFAULT_NUMBER, MAX_FITNESS) < MAX_FITNESS:
                happyforexGA.mutation()
                print("==> self.fittest_ind.individual_ID after mutation: %s" % happyforexGA.fittest_ind.individual_ID)
                print("==> self.second_fittest_ind.individual_ID after mutation: %s" % happyforexGA.second_fittest_ind.individual_ID)
                log.info("==> self.fittest_ind.individual_ID after mutation: %s" % happyforexGA.fittest_ind.individual_ID)
                log.info("==> self.second_fittest_ind.individual_ID after mutation: %s" % happyforexGA.second_fittest_ind.individual_ID)
                
                       
            # Add highest fitness offspring to population
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
            print("Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
            log.info("Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
            if happyforexGA.fittest_ind.fitness < MAX_FITNESS:
                if path.isfile(file_path_highest_solution):
                    remove(file_path_highest_solution)
                
                time_stamp = str(datetime.now().strftime(TIME_STAMP_FORMAT))
                file_path_highest_solution = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_HIGHEST_FITNESS
                file_path_highest_parameters = folder_output + time_stamp + '_' + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_HIGHEST_PARAMETERS
            
                write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
                write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, file_path_highest_parameters, '=')
                write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_CLOSED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_CLOSED_HISTORY)
                write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_OPENED_DICT, folder_output + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_ORDER_OPENED_HISTORY)
    
            print('#===========================================================================')
            log.info('#===========================================================================')
            
        # Print out and write to CSV file the best solution
        print('#===========================================================================')
        print("Solution found in generation: %s" % happyforexGA.generationCount);
        print("Fitness: %s" % happyforexGA.fittest_ind.fitness);
        print("Individual_ID: %s" % happyforexGA.fittest_ind.individual_ID)
        print("Genes: %s" % happyforexGA.fittest_ind.genes);
        log.info('#===========================================================================')
        log.info("Solution found in generation: %s" % happyforexGA.generationCount);
        log.info("Fitness: %s" % happyforexGA.fittest_ind.fitness);
        log.info("Individual_ID: %s" % happyforexGA.fittest_ind.individual_ID)
        log.info("Genes: %s" % happyforexGA.fittest_ind.genes);
        
        # Write out the whole best parameters (converted back 1/0 in the data into True/False)
        
        time_stamp = str(datetime.now().strftime(TIME_STAMP_FORMAT))
        write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, folder_output + time_stamp + '_' + FILENAME_BEST_SOLUTION, '=')
        write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, folder_output + time_stamp + '_' + FILENAME_BEST_PARAMETERS, '=')
        
        write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_CLOSED_DICT, folder_output + time_stamp + '_' + FILENAME_ORDER_CLOSED_HISTORY)
        write_dict2csv_no_header(happyforexGA.fittest_ind.ORDER_OPENED_DICT, folder_output + time_stamp + '_' + FILENAME_ORDER_OPENED_HISTORY)
        write_dict2csv_no_header(happyforexGA.population.DATE_DATA_DICT, folder_output + time_stamp + '_' + FILENAME_DATE_DICT)
        
        # Write the population final to a CSV file for reference
        print('#============================== Write the population final to a CSV file ==============================')
        log.info('#============================== Write the population final to a CSV file ==============================')
        write_dict2csv_no_header(happyforexGA.population.individuals_ID_dict,
                                 folder_output + "%sth_generation_" % happyforexGA.generationCount + FILENAME_POPULATION_FINAL)

    except Exception:
        logging.exception("Exception in main")
        exit(1) 
  
