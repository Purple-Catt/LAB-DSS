import pandas as pd

# Load the data from the provided files
crashes_path = '/Users/elvislleshi/Desktop/dss app/LDS24 - Data (1)/Crashes.csv'
vehicles_path = '/Users/elvislleshi/Desktop/dss app/LDS24 - Data (1)/Vehicles.csv'
people_path = '/Users/elvislleshi/Desktop/dss app/LDS24 - Data (1)/People.csv'

crashes = pd.read_csv(crashes_path)
vehicles = pd.read_csv(vehicles_path)
people = pd.read_csv(people_path)

# Inspect the structure and relationships between the datasets
crashes_info = crashes.info()
vehicles_info = vehicles.info()
people_info = people.info()

# Check for missing values in each dataset
crashes_missing = crashes.isnull().sum()
vehicles_missing = vehicles.isnull().sum()
people_missing = people.isnull().sum()

# Display the head of each dataset to understand their structures
crashes_head = crashes.head()
vehicles_head = vehicles.head()
people_head = people.head()

crashes_info, crashes_missing, crashes_head, vehicles_info, vehicles_missing, vehicles_head, people_info, people_missing, people_head
