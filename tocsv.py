import pandas as pd

fact = pd.read_csv('Data\\fact.csv', header=0)
tourney = pd.read_json('Data\\tourney.json', orient='split')
countries = pd.read_xml('Data\\countries.xml')

tourney.to_csv('Data\\tourney.csv', index=False)
countries.to_csv('Data\\countries.csv', index=False)
