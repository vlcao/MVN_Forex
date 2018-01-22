'''
Created on Dec 11, 2017

@author: cao.vu.lam
'''
import pandas as pd
import os

#===============================================================================
def convert_backflash2forwardflash(backflash_path):
    forwardflash_path = ''
    
    # replace the back flash with forward flash
    for i in range(len(backflash_path)):
        if backflash_path[i] == '\\':
            forwardflash_path += '/'
        else:
            forwardflash_path += backflash_path[i]
        
    return forwardflash_path

#===============================================================================
# Get the CSV file's path
file_name = str(os.path.dirname(os.getcwd())) + '/DataHandler/data/input/GBPUSD_M1_1y.csv'
print("==> file_name: %s" % file_name)
     
# convert the back flash with forward flash (just in case)
file_name = convert_backflash2forwardflash(file_name)
     
# Import the M1 data
print("==> Load CSV file into Data frame...")
DataFrame = pd.read_csv(file_name)
 
# Print out M1 data
print(DataFrame)
#===============================================================================

#     default_parameters_df = load_csv2dataframe(file_name_parameters)
#     default_parameters_df.columns = HEADER_PARAMETER_FILE
#     default_parameters_df.set_index('Parameter', inplace=True)
#     print(default_parameters_df)
#     
#     # retrieve subset data frame with optimize-needed parameters
#     subset_data = get_subset_dataframe(default_parameters_data, OPTIMIZE_PARAMETERS_LIST)
#     print(subset_data)
