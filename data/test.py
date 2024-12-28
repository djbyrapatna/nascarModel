import pickle
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


with open("racingref/rdata.pkl", 'rb') as f:
    dfRace = pickle.load(f)

with open("racingref/rdatatotal.pkl", 'rb') as f:
    dfRace = pickle.load(f)

print(dfRace[124])
