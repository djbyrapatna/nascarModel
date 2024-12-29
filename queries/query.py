'''
File to query racing reference webpages and 
extract results tables from each one
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time
import logging
import pickle
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(
    filename='data_retrieval_parallel.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


#Global strings for URL components (these are constant)
_rrefUrl = "https://www.racing-reference.info/"
_loopStr = "loopdata/"
_practiceStr = "practice-results/"
_qualStr = "qual-results/"
_raceStr = "race-results/"

_nonNumericColumns = ['Driver', 'Sponsor/Owner', 'Car', 'Status', 'Time']

#Generates URL's for racing reference practice, qualifiying, loop date
#and race data pages given year and race number range
def urlGen(yrmin, yrmax, raceMin, raceMax, splitByType=True):
    urls = []
    
    strs = [_raceStr, _qualStr, _practiceStr, _loopStr]
    for yr in range(yrmin, yrmax+1):
        for raceNum in range(raceMin, raceMax+1):
            dateStr = str(yr)+"-"+str(raceNum)
            urlGroup = ["","","",""]
            for i, specStr in enumerate(strs):
                newUrl = _rrefUrl+specStr+dateStr+"/W/"
                urlGroup[i] = newUrl
            urlGroup[2] += "1/"
            urls.append(urlGroup)
    #splits out URL's by type (practice, qualifying, race, loop) if needed for ordering
    if splitByType:
        urls = [url for urlG in urls for url in urlG]
        urls.sort()
        n = len(urls)
        lUrls = urls[0:n//4]
        pUrls = urls[n//4:n//2]
        qUrls = urls[n//2:3*n//4]
        rUrls = urls[3*n//4:n]
        urls = [lUrls, pUrls, qUrls, rUrls]
    return urls


def fetchRaceData(url, removeCertainRaceData=False):
    #define selenium options, add header
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")  # Run in headless mode
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    )
    
    try:
        #selenium driver does get request, waits until a table has loaded or 10 seconds
        #have passed
        driver = webdriver.Chrome(options=chromeOptions)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        html = driver.page_source
        driver.quit()
        
        tables = pd.read_html(html)
        #ensures at least 4 tables have loaded (stats table is always 4th)
        if len(tables) > 4:
            trimmed = tables[4]
            if _loopStr in url:
                trimmed = trimmed.iloc[2:]
            elif _practiceStr in url:
                trimmed = trimmed.iloc[1:]
            elif _qualStr in url:
                trimmed = trimmed.iloc[1:]
                trimmed = trimmed.iloc[:,:-1]
            if _raceStr not in url:
                trimmed = trimmed.reset_index(drop=True)
                trimmed.columns = trimmed.iloc[0]  
                trimmed = trimmed[1:].reset_index(drop=True)  # Remove the header row and reset index
            
            for col in trimmed.columns:
                if col not in _nonNumericColumns:
                     trimmed[col] = pd.to_numeric(trimmed[col], errors='coerce')


            #print(trimmed)
            if removeCertainRaceData:
                #print(trimmed)
                trimmed=trimmed.drop(columns=['Sponsor / Owner', "Pts", "PPts"])
                trimmed.dropna(inplace=True)
            return trimmed
        else:
            logging.error(f"No expected table found in {url}")
            return None
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def compileDataset(urls, existingDatasetPath=None, max_workers=8, removeCertainRaceData=False):
    #attempts to open existing dataset for appending, creates clean dataset if none exists
    #returns and logs error if the filename is invalid
    if existingDatasetPath:
        try:
            with open(existingDatasetPath, 'rb') as f:
                masterDf = pickle.load(f)
                #print(type(masterDf))
        
        except FileNotFoundError:
            masterDf = {}
            logging.error("No existing dataset found. Starting fresh.")
            return None
    else:
        masterDf = {}
    
    #creates key for each url, adds key and url to tasks list
    tasks = []
    dataType = None
    for url in urls:
        parts = url.rstrip('/').split('/')
        if parts[-1]=='1':
            raceInfo = parts[-3].split('-')
        else:
            raceInfo = parts[-2].split('-')
        if not dataType:
            dataType=parts[-3]
        
        yr = int(raceInfo[0])%100
        raceNum = int(raceInfo[1])
        keyNum = raceNum*100+yr
        if keyNum in masterDf:
            continue
        else:
            tasks.append([keyNum, url])

    #creates fetchRaceData job for each key/url pair in stasks
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetchRaceData, url, removeCertainRaceData): (keyNum) for keyNum, url in tasks}
        
        for future in as_completed(future_to_url):
            keyNum = future_to_url[future]
            #if result exists, adds data to master Df with appropriate key
            #logs issue if job fails or error thrown
            try:
                data = future.result()

                if data is not None:
                    masterDf[keyNum]=data
                    
                    logging.info(f"Appended record for {dataType}, {keyNum}.")
                else:
                    logging.warning(f"Failed to fetch data for {dataType}, {keyNum}.")
                    #print(f"Failed to fetch data for {dataType}, {keyNum}.")
            except Exception as e:
                logging.error(f"Exception for {dataType}, {keyNum}: {e}")
    
    return masterDf






