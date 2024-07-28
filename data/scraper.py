
urlBase = "https://www.racing-reference.info"

subUrl = ["race-results", "qual-results", "practice-results", "loopdata"]

for i in range(1,23):
    for sub in subUrl:
        fileName = "racingref/queries/2024-"+str(i)+"-"+sub[0]+".iqy"
        f = open(fileName, "w")
        outputUrl = urlBase + "/"+sub+"/2024-"
        if i <10:
            outputUrl = outputUrl+"0"
        outputUrl = outputUrl+str(i)+"/W/"
        f.write(outputUrl)
        f.close()

print("All files written")