#need to do following steps
#1. Import historic data and do same processing as other stuff
#a. Combine with current data 
#b. update prevs to incorporate across seasons
#2. Parse historic data seasonwide
#3. Incorporate tagged track data-prev track averages, prev race averages
#4. Incorporate teammate and manufacturer-prevSeason, prev track type avs, etc

import pickle
import pandas as pd
from statistics import fmean

def dataForRace(fileName, posKey, race, yr, includeCurr):
    # Define constants
    RACES_PER_SEASON = 36
    EARLIEST_YEAR = 2021

    # Find key corresponding to this specific race
    raceKey = race * 100 + (yr % 100)
    
    # Load data file
    with open(fileName, 'rb') as f:
        dfRace = pickle.load(f)
    
    # Get the list of drivers to calculate data for this particular race
    driverList = dfRace[raceKey]['Driver']
    
    # Define DataFrame columns based on whether to include current finish
    if includeCurr:
        avgFinishes = pd.DataFrame(columns=["Driver", "Year", "Curr", "Prev", 
                                            "Prev3", "Prev5", "Prev10", "PrevAll"])
    else:
        avgFinishes = pd.DataFrame(columns=["Driver", "Year", "Prev", 
                                            "Prev3", "Prev5", "Prev10", "PrevAll"])
    
    for driver in driverList:
        finishes = []
        finishes_current_year = []
        curr = 0
        currentRace = race
        currentYear = yr
        
        # Adjust the starting race based on includeCurr
        if not includeCurr:
            currentRace -= 1
        
        racesCollected = 0
        DESIRED_RACES = 10  # Number of previous races required
        
        while racesCollected < DESIRED_RACES:
            # Check if we've gone before the earliest year
            if currentYear < EARLIEST_YEAR:
                break  # Not enough races in the dataset
            
            # If race number is less than 1, wrap to the last race of the previous year
            if currentRace < 1:
                currentYear -= 1
                if currentYear < EARLIEST_YEAR:
                    break  # Prevent going before the earliest year
                currentRace = RACES_PER_SEASON
            key = currentRace * 100 + (currentYear % 100)
            
            # Retrieve race data if the key exists
            d = dfRace.get(key, pd.DataFrame())
            
            # Find row of data corresponding to driver
            rowDf = d[d['Driver'] == driver]
            if rowDf.empty and isinstance(driver, str):
                driverSpace = "  " + driver
                rowDf = d[d['Driver'] == driverSpace]
            
            # If row exists, process the finish position
            if not rowDf.empty:
                finish_position = rowDf[posKey].tolist()[0]
                if currentRace == race and currentYear == yr and includeCurr:
                    curr = finish_position
                    finishes_current_year.append(curr)
                else:
                    finishes.append(finish_position)
                    if currentYear == yr:
                        finishes_current_year.append(finish_position)
                    racesCollected += 1  # Increment only when a finish is added
            
            # Move to the previous race
            currentRace -= 1
        
        # After collecting finishes, check if we have enough data
        if racesCollected >= DESIRED_RACES:
            dfAdd = [driver, yr]
            if includeCurr:
                dfAdd.append(curr)
            
            # Previous finish (most recent finish before current race)
            
            dfAdd.append(finishes[0])
            
            # Calculate averages
            prev3 = fmean(finishes[:3]) if len(finishes) >= 3 else fmean(finishes)
            prev5 = fmean(finishes[:5]) if len(finishes) >= 5 else fmean(finishes)
            prev10 = fmean(finishes[:10]) if len(finishes) >= 10 else fmean(finishes)
            
            dfAdd.append(prev3)
            dfAdd.append(prev5)
            dfAdd.append(prev10)
            
            # Calculate PrevAll (average of collected finishes in the current year)
            dfAdd.append(fmean(finishes_current_year) if finishes_current_year else None)
            
            # Append the data to the DataFrame
            avgFinishes.loc[len(avgFinishes)] = dfAdd
    
    return avgFinishes







# import pickle
# import pandas as pd
# from statistics import fmean

# def dataForRace(fileName, posKey, race, yr, includeCurr):
#     #find key corresponding to this specific race
#     raceKey = race*100 +(yr%100)
#     #load data file
#     with open(fileName, 'rb') as f:
#         dfRace = pickle.load(f)
#     f.close()
#     minKey = min(dfRace.keys())
#     #get the list of drivers to calc data for this particular race
#     driverList = dfRace[raceKey]['Driver']
#     if includeCurr:
#         avgFinishes = pd.DataFrame(columns=["Driver", "Year", "Curr", "Prev", 
#                                             "Prev3", "Prev5", "Prev10", "PrevAll"])
#     else:
#         avgFinishes = pd.DataFrame(columns=["Driver", "Year","Prev", 
#                                             "Prev3", "Prev5", "Prev10", "PrevAll"])
    
#     for driver in driverList:
#         finishes = []
#         curr = 0
#         startRange = race
#         if not includeCurr:
#             startRange -=1
#         #loop thru races in data set
#         for i in range(startRange,0,-1):
#             #get specific dataframe corresponding to race
#             key = i*100 +(yr%100)
#             d = dfRace[key]
            

#             #find row of data corresponding to driver
#             if not d.empty:
#                 rowDf = d[d['Driver'] == driver]
#             #if row exists, append finishes array
#             if rowDf.empty and isinstance(driver, str):
#                 driverSpace = "  "+driver
#                 rowDf = d[d['Driver'] == driverSpace]
#             if not rowDf.empty:
#                 if i == race:
#                     curr = rowDf[posKey].tolist()[0]   
#                 else:
#                     finishes.append(rowDf[posKey].tolist()[0])
    
#         numRaces = len(finishes)
        
#         #calculate and append the previous finish, the average finish over the last 3, 5, 10, and total season races
#         if numRaces>=10:
#             dfAdd = [driver,yr]
#             if includeCurr:
                
#                 dfAdd.append(curr)
            
#             dfAdd.append(finishes[0])
            
#             prev3 = fmean(finishes[0:3])
#             dfAdd.append(prev3)
            
            
#             prev5 = fmean(finishes[0:5])
#             dfAdd.append(prev5)
            
            
#             prev10 = fmean(finishes[0:10])
#             dfAdd.append(prev10)
            
#             dfAdd.append(fmean(finishes))

#             avgFinishes.loc[len(avgFinishes)] = dfAdd
            
    
#     return avgFinishes

def createSeasonData(fileName, posKey):
    with open(fileName, 'rb') as f:
        dfRace = pickle.load(f)
    f.close()
    yearArray = [2021,2022,2023,2024]
    avgFinishes =  pd.DataFrame(columns=["Driver", "Year",posKey])
    for yr in yearArray:
        raceKey = yr%100 + 100
        driverList = dfRace[raceKey]['Driver']
        
        for driver in driverList:
            avgFinish = []
            endRange = yr%100+3600
            for key in range(raceKey,endRange,100):
                if key in dfRace:
                    d = dfRace[key]
                    if not d.empty:
                        rowDf = d[d['Driver'] == driver]
                    if not rowDf.empty:
                        avgFinish.append(rowDf[posKey].tolist()[0])
            numRaces = len(avgFinish)
            if numRaces>=5:
                dfAdd = [driver,yr]
                #print(dfAdd, avgFinish)
                dfAdd.append(fmean(avgFinish))
                avgFinishes.loc[len(avgFinishes)] = dfAdd
    return avgFinishes

fileArr = ["racingref/rdatatotal.pkl","racingref/pdatatotal.pkl","racingref/qdatatotal.pkl"]
posArr = ["Pos", "Rank", "Rank"]
