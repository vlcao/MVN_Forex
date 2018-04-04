import os
from datetime import *
import time
import sys
import shutil

#===============================================================================
EA_CODE = 'Synergista_v1.00'
SCR_DIR_PATH = os.getcwd()
FOLDER_DATA_OUTPUT = SCR_DIR_PATH + '/data/output/'


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
def init():
    
    global OPT_DURATION_LIST
#     OPT_DURATION_LIST = [365, 1095, 1825, 2555, 3285]
    OPT_DURATION_LIST = [365, 1095, 1825]   
    
    global SYMBOLS
    SYMBOLS = [
#         'AUDCAD',
#         'AUDJPY',
#         'AUDUSD',
#         'CADJPY',
#         'EURCAD',
#         'EURGBP',
#         'EURJPY',
#         'GBPJPY',
#         'USDCAD',
        'EURUSD',
        'GBPUSD',
        'USDJPY',
        ]
    
    return


#===============================================================================
def fix_create_time(filename):
    if not os.path.isfile(filename):
        print("file \"%s\" doesn't exit" % (str(filename)))
        return
    
    def fix(filename):
        new_file = filename + ' 2'
        ofile = open(new_file, 'w')
        with open(filename, 'r') as f:
            for line in f:
                if 'CREATE_TIME' in line:
                    _1, _2 = line.split('=')
                    s1, s2 = _2.split(' ')
                    line = 'CREATE_TIME=2018.04.14 ' + s2
                
                ofile.write(line)
        return new_file
    
    new_file = fix(filename)
    os.remove(filename)
    os.rename(new_file, filename)
    
    return


#===============================================================================
def main():
    init()
    
    global OPT_DURATION_LIST
    for OPT_DURATION in OPT_DURATION_LIST:
        for symbol in SYMBOLS:
            
            filename = convert_backflash2forwardflash(FOLDER_DATA_OUTPUT + EA_CODE + '/30/' 
                                                                + str(OPT_DURATION) + '/' 
                                                                + symbol + '/' 
                                                                + symbol + '.' + str(OPT_DURATION) + '.30.optimize_last.txt')
            
#             filename = str(OPT_DURATION) + '/' + symbol + '/' + symbol + '.' + \
#                 str(OPT_DURATION) + '.30.optimize_last.txt'
                
            fix_create_time(filename)
            
    print("Completed fixing CREATE_TIME!!!")
    return


#===============================================================================
if __name__ == "__main__":
    main()
