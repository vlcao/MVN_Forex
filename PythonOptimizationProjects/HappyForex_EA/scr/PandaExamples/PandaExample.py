'''
Created on Dec 11, 2017

@author: cao.vu.lam
'''
import pandas as pd

dict = {"countryAbbr": ["US", "AUS", "JAP", "IN", "RU", "MOR", "EG"],
       "cars_per_cap": [809, 731, 588 , 18, 200, 70, 45],
       "country": ["United States", "Australia", "Japan", "India", "Russia", "Morocco", "Egypt"],
       "drives_right": [True, False, False, False, True, True, True] }
cars = pd.DataFrame(dict)
print(cars)
print('===============================================================================')

# Set the index for brics
cars.index = ["US", "AUS", "JAP", "IN", "RU", "MOR", "EG"]
print(cars)
print('===============================================================================')
 
# Print out country column as Pandas Series
print(cars['cars_per_cap'])
print('===============================================================================')
 
# Print out country column as Pandas DataFrame
print(cars[['cars_per_cap']])
print('===============================================================================')
 
# Print out DataFrame with country and drives_right columns
print(cars[['cars_per_cap', 'country']])
print('===============================================================================')
 
# Print out first 4 observations
print(cars[0:4])
print('===============================================================================')
 
# Print out fifth, sixth, and seventh observation
print(cars[4:6])
print('===============================================================================')

# Print out observation for Japan
print(cars.iloc[2])
print('===============================================================================')

# Print out observations for Australia and Egypt
print(cars.loc['AUS'])
print('===============================================================================')
print(cars.loc[['AUS']])
print('===============================================================================')
print(cars.loc[['AUS', 'EG']])
print('===============================================================================')


    
    
    
    
    
    