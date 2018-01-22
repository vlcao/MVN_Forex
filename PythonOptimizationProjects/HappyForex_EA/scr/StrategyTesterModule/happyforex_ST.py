'''
Created on Dec 22, 2017

@author: cao.vu.lam
'''

import logging
import random
import shutil
import os
from os import path, remove
from GenericAlgorithmModule.happyforex_GA import HappyForexGenericAlgorithm
from DataHandler.happyforex_Datahandler import DEFAULT_NUMBER, MAX_FITNESS, FOLDER_DATA_OUTPUT, SYMBOL, TIME_STAMP, \
                                    FILENAME_HIGHEST_FITNESS, FILENAME_BEST_SOLUTION, FILENAME_BEST_PARAMETERS, \
                                    FILENAME_POPULATION_INITIAL, FILENAME_POPULATION_FINAL, \
                                    OPTIMIZED_PARAMETERS_DATA, FILENAME_OPTIMIZE_PARAMETER, \
                                    FILENAME_ORDER_CLOSED_HISTORY, FILENAME_ORDER_OPENED_HISTORY, \
                                    write_dict2csv_no_header, write_array2csv_with_delimiter_no_header
from EAModule.happyforex_EA import happyforex_EA_instance

logger = logging.getLogger(__name__)
    
################################################################################
##########################           MAIN           ############################
################################################################################        
if __name__ == '__main__': 
    
    # Create an instance for HappyForexGenericAlgorithm to run the program
    happyforexGA = HappyForexGenericAlgorithm()
    
    # Create an folder for storing all outputs in this section 
    folder_output = FOLDER_DATA_OUTPUT + SYMBOL + '_optimization_output/'
    if os.path.exists(folder_output):
        shutil.rmtree(folder_output)
    os.makedirs(folder_output)
    
    # Initialize population
    print('#============================== Initialize population ==============================')
    happyforexGA.population.initialize_population()
    
    # Write the individual_ID_list to a CSV file for reference
    print('#============================== Write the individual_ID_list to a CSV file ==============================')
    write_dict2csv_no_header(happyforexGA.population.individuals_ID_dict, folder_output + FILENAME_POPULATION_INITIAL)
    
     
    # Calculate fitness of each individual
    print('#============================== Calculate fitness of each individual ==============================')
    happyforexGA.population.calculate_fittest()
     
    # Get the individual with highest fitness ==> retrieve the highest fitness for the population
    print('#============================== Get the individual with highest fitness ==============================')
    happyforexGA.fittest_ind = happyforexGA.population.get_fittest()
    
    
    # Print out and write to CSV file the highest solution
    print("==> Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
    if happyforexGA.fittest_ind.fitness < MAX_FITNESS:
        file_path_highest_solution = folder_output + TIME_STAMP + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_HIGHEST_FITNESS
        write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
     
           
    print('#============================== Population gets an individual with maximum fitness ==============================')
    # While population gets an individual with maximum fitness
    while (happyforexGA.population.fittest < MAX_FITNESS):
        happyforexGA.generationCount += 1
           
        # Do selection
        happyforexGA.selection()
        print("==> self.fittest_ind.individual_ID at selection: %s" % happyforexGA.fittest_ind.individual_ID)
        print("==> self.second_fittest_ind.individual_ID at selection: %s" % happyforexGA.second_fittest_ind.individual_ID)
          
           
        # Do crossover
        happyforexGA.crossover()
        print("==> self.fittest_ind.individual_ID after crossover: %s" % happyforexGA.fittest_ind.individual_ID)
        print("==> self.second_fittest_ind.individual_ID after crossover: %s" % happyforexGA.second_fittest_ind.individual_ID)
        
           
        # Do mutation under a random probability
        if random.randint(DEFAULT_NUMBER, MAX_FITNESS) < MAX_FITNESS:
            happyforexGA.mutation()
            print("==> self.fittest_ind.individual_ID after mutation: %s" % happyforexGA.fittest_ind.individual_ID)
            print("==> self.second_fittest_ind.individual_ID after mutation: %s" % happyforexGA.second_fittest_ind.individual_ID)
        
                   
        # Add highest fitness offspring to population
        happyforexGA.add_fittest_offspring()
        print("==> Least_fittest_ind.individual_ID: %s" % happyforexGA.least_fittest_ind.individual_ID)
        print("... replace by highest fitness offspring individual ==> added_offstring_ind.individual_ID: %s" % happyforexGA.added_offstring_ind.individual_ID)
        
         
        # Calculate new fitness value
        happyforexGA.population.calculate_fittest()
         
        # Get the new individual with highest fitness ==> retrieve the highest fitness for the population
        happyforexGA.fittest_ind = happyforexGA.population.get_fittest()
        
        # Print out and write to CSV file the highest solution + remove the old highest solution file
        print("Generation: %s - Highest Fitness: %s" % (happyforexGA.generationCount, happyforexGA.population.fittest))
        if happyforexGA.fittest_ind.fitness < MAX_FITNESS:
            if path.isfile(file_path_highest_solution):
                remove(file_path_highest_solution)
            file_path_highest_solution = folder_output + TIME_STAMP + str(happyforexGA.fittest_ind.fitness) + '_' + FILENAME_HIGHEST_FITNESS
            write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, file_path_highest_solution, '=')
    
        print('#===========================================================================')
    
    # Print out and write to CSV file the best solution
    print('#===========================================================================')
    print("Solution found in generation: %s" % happyforexGA.generationCount);
    print("Fitness: %s" % happyforexGA.fittest_ind.fitness);
    print("Individual_ID: %s" % happyforexGA.fittest_ind.individual_ID)
    print("Genes: %s" % happyforexGA.fittest_ind.genes);
    write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes, folder_output + TIME_STAMP + FILENAME_BEST_SOLUTION, '=')
             
    
    # Write out the whole best parameters (converted back 1/0 in the data into True/False)
    write_array2csv_with_delimiter_no_header(happyforexGA.fittest_ind.genes_completed, folder_output + TIME_STAMP + FILENAME_BEST_PARAMETERS, '=')
          
          
    # Write the population final to a CSV file for reference
    print('#============================== Write the population final to a CSV file ==============================')
    write_dict2csv_no_header(happyforexGA.population.individuals_ID_dict,
                             folder_output + "%sth_generation_" % happyforexGA.generationCount + FILENAME_POPULATION_FINAL)

    # Write out other data for reference
    write_array2csv_with_delimiter_no_header(OPTIMIZED_PARAMETERS_DATA, FOLDER_DATA_OUTPUT + FILENAME_OPTIMIZE_PARAMETER, '=')
    write_dict2csv_no_header(happyforex_EA_instance.ORDER_CLOSED_DICT, FOLDER_DATA_OUTPUT + FILENAME_ORDER_CLOSED_HISTORY)
    write_dict2csv_no_header(happyforex_EA_instance.ORDER_OPENED_DICT, FOLDER_DATA_OUTPUT + FILENAME_ORDER_OPENED_HISTORY)