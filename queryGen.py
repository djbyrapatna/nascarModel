dataType = ["race-results", "practice-results", "qual-results", "loopdata"]

yrArray = [2021,2022,2023]

for yr in yrArray:
    for type in dataType:
        for i in range(1,37):
            raceNum = str(i)
            if i<10:
                raceNum = "0"+raceNum
            url = "https://racing-reference.info/"+type+"/"+str(yr)+"-"+raceNum+"/W/"
            f = open("queries/"+type+"-"+str(yr)+"-"+raceNum+".iqy", "w+")
            f.write(url)
            f.close()
