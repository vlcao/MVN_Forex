'''
Created on Dec 27, 2017

@author: cao.vu.lam
'''

from os import path, remove
import logging

from DataHandler.happyforex_Datahandler import *
 
# # If applicable, delete the existing log file to generate a fresh log file during each execution
# if path.isfile(FOLDER_DATA_OUTPUT + FILENAME_LOG):
#     remove(FOLDER_DATA_OUTPUT + FILENAME_LOG)
 
# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
 
# Create the Handler for logging data to a file
logger_handler = logging.FileHandler(FOLDER_DATA_OUTPUT + FILENAME_LOG)
logger_handler.setLevel(logging.DEBUG)
 
# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
 

# Create the Handler for logging data to the console
logger_handler_console = logging.StreamHandler()
logger_handler_console.setLevel(logging.DEBUG)
logger_handler_console.setFormatter(logger_formatter)
logger.addHandler(logger_handler_console) 
  
 
# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)
 
# Add the Handler to the Logger
logger.addHandler(logger_handler)
logger.info('Completed configuring logger()!')



#===============================================================================
# def initialize_logger(file_name):
#     
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#     
#     # create a logging format
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#      
#     # create a file handler
#     handler_file = logging.FileHandler(file_name)
#     handler_file.setLevel(logging.INFO)
#     handler_file.setFormatter(formatter)
#     logger.addHandler(handler_file)
#     
#     
#     # create console handler and set level to info
#     handler_console = logging.StreamHandler()
#     handler_console.setLevel(logging.INFO)
#     handler_console.setFormatter(formatter)
#     logger.addHandler(handler_console)
#===============================================================================
    

