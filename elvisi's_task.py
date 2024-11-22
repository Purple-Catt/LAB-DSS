import pandas as pd
import os

import pandas as pd
import os

# Kontrollo ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Rruga Absolute për testim
people_path = '/Users/elvislleshi/Desktop/dss app/LDS24 - Data (1)/People.csv'
crashes_path = '/Users/elvislleshi/Desktop/dss app/LDS24 - Data (1)/Crashes.csv'
vehicles_path = '/Users/elvislleshi/Desktop/dss app/LDS24 - Data (1)/Vehicles.csv'

# Ngarkimi i skedarëve
try:
    people = pd.read_csv(people_path, header=0)
    crashes = pd.read_csv(crashes_path, header=0)
    vehicles = pd.read_csv(vehicles_path, header=0)

    print(people.isna().sum())
    print(crashes.isna().sum())
    print(vehicles.isna().sum())

