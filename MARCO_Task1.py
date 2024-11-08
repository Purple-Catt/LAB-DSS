import pandas as pd
import numpy as np
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
people = pd.read_csv(ROOT_DIR + '/Data/People.csv', header=0)
crashes = pd.read_csv(ROOT_DIR + '/Data/Crashes.csv', header=0)
vehicles = pd.read_csv(ROOT_DIR + '/Data/Vehicles.csv', header=0)
print(people.isna().sum())
