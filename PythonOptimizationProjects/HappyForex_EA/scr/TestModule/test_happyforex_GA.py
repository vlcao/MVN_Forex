'''
Created on Dec 29, 2017

@author: cao.vu.lam
'''
import unittest

from GenericAlgorithmModule.happyforex_GA import Individual
from DataHandler.happyforex_Datahandler import display_an_array_with_delimiter, OPTIMIZE_PARAMETERS_LIST, DEFAULT_NUMBER
from EAModule import happyforex_EA


class Test(unittest.TestCase):


        #===========================================================================
        def test_create_random_genes(self):
            print('#============================== test_create_random_genes ==============================')
            individual = Individual()
            individual.create_random_genes()
            display_an_array_with_delimiter(individual.genes, '=')
              
            # testing
            predefine_len = len(OPTIMIZE_PARAMETERS_LIST)
            print("==> predefine_len of OPTIMIZE_PARAMETERS_LIST: %s" % predefine_len)
            self.assertEqual(predefine_len, len(individual.genes), "The new array DOESN'T have the same rows with the source array.")
         
        #===========================================================================
        def test_create_uniqueID(self):
            print('#============================== test_create_uniqueID ==============================')
            individual = Individual()
             
            # testing
            dictionary_IDlist = {}
            individual.create_ind_uniqueID(dictionary_IDlist)
             
            flag_individualID = False
            if individual.individual_ID != DEFAULT_NUMBER:
                flag_individualID = True
             
            self.assertTrue(flag_individualID, "CANNOT create an individual.")
             
        #===========================================================================
        def test_cal_fitness(self):
            print('#============================== test_cal_fitness ==============================')
            individual = Individual()
             
            happyforex_EA.net_profit = 123
            happyforex_EA.total_win = 30.15
            '''
            50 * (self.net_profit / NET_PROFIT 
                             + self.total_win / MAX_WIN_TOTAL_TRADE)
            '''
             
            # testing
            individual.cal_fitness()
            print("==> individual.fitness: %s" % individual.fitness)
            predefinded_fitness = 67.08
            print("==> predefinded_fitness: %s" % predefinded_fitness)
             
            self.assertEqual(predefinded_fitness, individual.fitness, "The cal_fitness ISNOT correct.")
        
        #===========================================================================
        def test_create_manual_genes(self):
            print('#============================== test_create_manual_genes ==============================')
           
            manual_parameters_list = ['1', '1', '3', '1', '6', '12', '-25', '0.01']
            print("==> manual_parameters_list = ['1', '1', '3', '1', '6', '12', '-25', '0.01']")
            
            individual = Individual()
            individual.create_manual_genes(manual_parameters_list)
            display_an_array_with_delimiter(individual.genes, '=')
              
            # testing
            count = DEFAULT_NUMBER
            flag_item = False
            for item in manual_parameters_list:
                if item[count] == individual.genes[count][1]:
                    flag_item = True
                     
            self.assertTrue(flag_item, "CANNOT create genes manually.")
        
        #===========================================================================
        def test_flip_value(self):
            print('#============================== test_flip_value ==============================')
            individual = Individual()
            individual.create_random_genes()
             
            manual_parameters_list = ['1', '1', '3', '0', '6', '12', '-25', '0.01']
            print("==> manual_parameters_list = ['1', '1', '3', '0', '6', '12', '-25', '0.01']")
            
            
            individual = Individual()
            individual.create_manual_genes(manual_parameters_list)
            dictionary_IDlist = {}
            individual.create_ind_uniqueID(dictionary_IDlist)
 
            print('===========================================================================')
            print("==> individual[genes] BEFORE flip:")
            display_an_array_with_delimiter(individual.genes, '=')
            
            # Flip value at the mutation_point
            mutation_point = predefine_flip_value = DEFAULT_NUMBER
            print("==> mutation_point = %s" % mutation_point)
            individual.flip_value(mutation_point)
            
            print('===========================================================================')
            print("==> individual[genes] AFTER flip:")
            display_an_array_with_delimiter(individual.genes, '=')
            
            
            # testing
            count = DEFAULT_NUMBER
            flag_item = False
            if individual.genes[count][1] == str(predefine_flip_value):
                flag_item = True
                     
            self.assertTrue(flag_item, "CANNOT flip value.")
            
            
            # Flip value at the mutation_point
            mutation_point = 3
            print("==> mutation_point = %s" % mutation_point)
            individual.flip_value(mutation_point)
            
            print('===========================================================================')
            print("==> individual[genes] AFTER flip:")
            display_an_array_with_delimiter(individual.genes, '=')
            
            
            # testing
            count = 3
            predefine_flip_value = '1'
            flag_item = False
            if individual.genes[count][1] == str(predefine_flip_value):
                flag_item = True
                     
            self.assertTrue(flag_item, "CANNOT flip value.")
        
#===========================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
#===========================================================================
