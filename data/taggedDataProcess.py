import pandas as pd
import numpy as np
import pickle



def add_teammates_column(df):
    grouped = df.groupby(['Year', 'Team'])['Driver'].apply(lambda x: ', '.join(x))
    
    # Map the grouped data to the original DataFrame
    df['Teammates'] = df.apply(lambda row: grouped.loc[row['Year'], row['Team']], axis=1)
    df['Teammates'] = df.apply(lambda row: ', '.join([driver for driver in row['Teammates'].split(', ') if driver != row['Driver']]), axis=1)
    return df

def updateTaggedData(taggedDataFile, destFiles):
        df = pd.read_excel(taggedDataFile, sheet_name = None)

        years = df["Teams"]['Year'].unique()

        dfs_by_year = {year: df["Teams"][df["Teams"]['Year'] == year].reset_index(drop=True) for year in years}

        df['Teams'] = add_teammates_column(df['Teams'])

        fileArr = destFiles
        with open(fileArr[0], 'wb') as f:
                pickle.dump(df['Tracks'], f)

        with open(fileArr[1], 'wb') as f:
                pickle.dump(df['Teams'], f)


# updateTaggedData("racingref/taggedData2.xlsx",
# ['racingref/trackDataTagged2.pkl', "racingref/teamDatatagged2.pkl"])
