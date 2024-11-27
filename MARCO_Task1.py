import pandas as pd
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
people = pd.read_csv(ROOT_DIR + '/Data/People.csv', header=0)
crashes = pd.read_csv(ROOT_DIR + '/Data/Crashes.csv', header=0)
vehicles = pd.read_csv(ROOT_DIR + '/Data/Vehicles.csv', header=0)
# print the number of missing values in each dataset
# The way to deal with them is described in 'handling_missing_values.txt'
print(people.isna().sum())
print(crashes.isna().sum())
print(vehicles.isna().sum())
print(vehicles.columns)
print(crashes.columns)
print(people.columns)
print(vehicles['VEHICLE_YEAR'].value_counts(dropna=False))
