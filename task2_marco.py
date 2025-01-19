import pandas as pd

fact = pd.read_csv('Data\\fact.csv', header=0)
tourney = pd.read_csv('Data\\tourney.csv', header=0)
countries = pd.read_csv('Data\\countries.csv', header=0)

print('FACT DATASET INFO')
print(fact.describe())
print(fact.isna().sum())
print('TOURNEY DATASET INFO')
print(tourney.describe(include='all')[['surface', 'draw_size']])
print(tourney.isna().sum())
print('COUNTRIES DATASET INFO')
print(countries.describe())
print(countries.isna().sum())
