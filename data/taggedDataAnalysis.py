import pickle
import pandas as pd
import numpy as np
from statistics import fmean
from .historicAnalysis import dataForRace
from .linRegModelSetup import createRaceKeyArray
#Have tagged data for 1. track and track type
#2. Teammates and manufacturers
#Let's see what we have so far first



def createHelperDf(fileName, raceMin, raceMax, yearMin, yearMax, fileArr):
    teamFile, trackFile = fileArr
    with open(teamFile, 'rb') as f:
        dfTeam = pickle.load(f)
    with open(trackFile, 'rb') as f:
        dfTrack = pickle.load(f)
    raceKeyArray = createRaceKeyArray(raceMin, raceMax, yearMin, yearMax)
    H = pd.DataFrame(columns=["Driver", "Year", "Race", "Finish"])
    with open(fileName, 'rb') as f:
        dfRace = pickle.load(f)
    f.close()
    for key in raceKeyArray:
        raceNum = key//100
        yr = key%100 + 2000
        d = dfRace[key]
        driverList = d['Driver']
        finish = pd.DataFrame(columns=["Driver", "Year", "Race", "Finish"])
        for driver in driverList:
            if driver ==driver and driver!="# Of" and driver != "Laps":
                dfAdd = [driver, yr, raceNum]
                if not d.empty:
                    rowDf = d[d['Driver'] == driver]
                if rowDf.empty and isinstance(driver, str):
                    driverSpace = "  "+driver
                    rowDf = d[d['Driver'] == driverSpace]
                if not rowDf.empty:
                    dfAdd.append(rowDf["Pos"].tolist()[0])
                finish.loc[len(finish)] = dfAdd
        H = H._append(finish)
    H['Driver'] = H['Driver'].str.strip()
    H = pd.merge(H, dfTrack[['Race', 'Year', 'Track', 'Type']], on=['Race', 'Year'], how='left')
    H = pd.merge(H, dfTeam[[ 'Year', 'Driver', 'Manufacturer', 'Team', 'Teammates']], on=[ 'Year', 'Driver'], how='left')
    return H

def createMainDf(fileName):
    with open(fileName, 'rb') as f:
        H = pickle.load(f)
    M = pd.DataFrame(columns=["Driver", "Year", "Race", "PrevFinishAtTrack",
                            "AvgFinishAtTrack", "AvgFinishAtTrackType",
                            "ManufacturerPrevYearAvg", "TeamPrevYearAvg",
                            "TeamAvgFinishAtTrack", "TeamAvgFinishAtTrackType"])
    M = pd.merge(M,H,on=["Driver","Year","Race"], how='right')
    M['Driver']= M['Driver'].str.strip()
    M['Finish'] = pd.to_numeric(M['Finish'])
    M['OriginalOrder'] = M.index
    #calculate prev finish at track
    helper_df = M.groupby(['Driver', 'Track']).shift(1)
    M['PrevFinishAtTrack'] = helper_df['Finish']
    #calculate avg finish at track
    M = M.sort_values(by=['Driver', 'Track', 'Year'])
    def calculate_avg_finish(group):
        group['AvgFinishAtTrack'] = group['Finish'].expanding().mean().shift(1)
        return group
    M = M.groupby(['Driver', 'Track']).apply(calculate_avg_finish).reset_index(drop=True)
    M = M.sort_values(by='OriginalOrder')
    #calculate avg finish at track type
    M = M.sort_values(by=['Driver', 'Type', 'Year'])
    def calculate_avg_finish_type(group):
        group['AvgFinishAtTrackType'] = group['Finish'].expanding().mean().shift(1)
        return group
    M = M.groupby(['Driver', 'Type']).apply(calculate_avg_finish_type).reset_index(drop=True)
    M = M.sort_values(by='OriginalOrder')
    #calculate team avg finish at track type
    helper = M[['Year', 'Race', 'Team','Track', 'Type']].drop_duplicates().reset_index(drop=True)
    # Calculate the average of the "Finish" column for each combination of "Year", "Race", and "Team"
    avg_finish = M.groupby(['Year', 'Race', 'Team','Track', 'Type'])['Finish'].mean().reset_index()
    avg_finish.rename(columns={'Finish': 'TeamAvgFinish'}, inplace=True)
    # Merge the calculated averages into the helper DataFrame
    helper = pd.merge(helper, avg_finish, on=['Year', 'Race', 'Team', 'Track', 'Type'], how='left')
    helper['TeamRunningAvgFinishAtTrack'] = helper.groupby(['Team', 'Track'])['TeamAvgFinish'].expanding().mean().reset_index(level=[0,1], drop=True)
    helper['TeamRunningAvgFinishAtTrackType'] = helper.groupby(['Team', 'Type'])['TeamAvgFinish'].expanding().mean().reset_index(level=[0,1], drop=True)
    M = pd.merge(M, helper[['Year', 'Race', 'Track', 'Team', 'TeamRunningAvgFinishAtTrack', 'TeamRunningAvgFinishAtTrackType']], on=['Year', 'Race', 'Track', 'Team'], how='left', suffixes=('', '_helper'))
    
    #add team avg finishes at track, type
    # Initialize the TeamAvgFinishAtTrack column with NaNs
    M['TeamAvgFinishAtTrack'] = np.nan
    M['TeamAvgFinishAtTrackType'] = np.nan

    # Iterate through each row in the DataFrame M
    for idx, row in M.iterrows():
        team = row['Team']
        track = row['Track']
        year = row['Year']
        race = row['Race']
        type = row['Type']
        
        # Find the previous rows with the same Team and Track but different Race and/or Year
        previous_rows = M[(M['Team'] == team) & (M['Track'] == track) & 
                        ((M['Year'] < year) | ((M['Year'] == year) & (M['Race'] != race))) & 
                        (M.index < idx)]
        
        # If there are previous rows, get the most recent one and its TeamRunningAvgFinishAtTrack
        if not previous_rows.empty:
            most_recent_row = previous_rows.iloc[-1]
            M.at[idx, 'TeamAvgFinishAtTrack'] = most_recent_row['TeamRunningAvgFinishAtTrack']

        previous_rows = M[(M['Team'] == team) & (M['Type'] == type) & 
                        ((M['Year'] < year) | ((M['Year'] == year) & (M['Race'] != race))) & 
                        (M.index < idx)]
        if not previous_rows.empty:
            most_recent_row = previous_rows.iloc[-1]
            M.at[idx, 'TeamAvgFinishAtTrackType'] = most_recent_row['TeamRunningAvgFinishAtTrackType']

    # Drop the helper columns
    M = M.drop(columns=['TeamRunningAvgFinishAtTrack', 'TeamRunningAvgFinishAtTrackType'])

    M = M.sort_values(by='OriginalOrder')

    M['TeamPrevYearAvg'] = np.nan
    M['ManufacturerPrevYearAvg'] = np.nan
    # Calculate the previous year's average finishes for each team
    prev_year_avg_team = M.groupby(['Team', 'Year'])['Finish'].mean().reset_index()
    prev_year_avg_team['Year'] += 1  # Shift the years to the next year to match with the current year

    # Merge the previous year's averages back into the original DataFrame for teams
    M = pd.merge(M, prev_year_avg_team[['Team', 'Year', 'Finish']], on=['Team', 'Year'], how='left', suffixes=('', '_PrevYear'))
    M['TeamPrevYearAvg'] = M['Finish_PrevYear']
    M = M.drop(columns=['Finish_PrevYear'])
    M = M.sort_values(by='OriginalOrder')
    # Calculate the previous year's average finishes for each manufacturer
    prev_year_avg_manufacturer = M.groupby(['Manufacturer', 'Year'])['Finish'].mean().reset_index()
    prev_year_avg_manufacturer['Year'] += 1  # Shift the years to the next year to match with the current year

    # Merge the previous year's averages back into the original DataFrame for manufacturers
    M = pd.merge(M, prev_year_avg_manufacturer[['Manufacturer', 'Year', 'Finish']], on=['Manufacturer', 'Year'], how='left', suffixes=('', '_PrevYear'))
    M['ManufacturerPrevYearAvg'] = M['Finish_PrevYear']
    M = M.drop(columns=['Finish_PrevYear'])

    M = M.sort_values(by='OriginalOrder').drop(columns=['OriginalOrder'])
   
    return M


# H = createHelperDf('racingref/forModel/raceDataUntagged.pkl',1, 36, 2021, 2024, ['racingref/trackDataTagged2.pkl', "racingref/teamDatatagged2.pkl"])
# with open('racingref/helperTag2.pkl', 'wb') as f:
#     pickle.dump(H,f)


# M = createMainDf("racingref/helperTag2.pkl")

# pklFile = 'racingref/mainTagData2.pkl'
# with open(pklFile, 'wb') as f:
#     pickle.dump(M, f)

# M.to_excel("tagDataCheck2.xlsx")
#df structure:
#Driver Year Race PrevFinishAtTrack AvgFinishAtTrack AvgFinishAtTrackType ManufacturerPrevSzn TeamPrevSzn TeamAvgFinishAtTrack TeamAvgFinishatTrackType

#helper df likely needed
#driver year Race Finish Track TrackType Manufacturer Team



#should calculate:
#Average finish at track, avg finish at track type
#previous finish at track
#manufacturer prev season avg
#team prev season avg
#team avg finish at track, team avg finish at track type
