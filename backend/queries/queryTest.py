import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

#Table 4 for race data
#Table 4 for qual data
#Table 4 for practice data
#Table 4 for loop data

def fetchRaceData(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find all tables in the page
        tables = pd.read_html(response.text)
        
        for i, table in enumerate(tables):
            print("---------------------------------------------------")
            print(i)
            print("---------------------------------------------------")
            print(table)
        # Identify the correct table (assuming the first table is the race results)
        # race_results = tables[0]  # Adjust the index if necessary
        
        # # Add metadata if needed (e.g., year and race number from URL)
        # # Example: Extract year and race_number from URL
        # parts = url.split('/')
        # race_info = parts[-2].split('-')
        # year = race_info[0]
        # race_number = race_info[1]
        
        # race_results['Year'] = int(year)
        # race_results['Race_Number'] = int(race_number)
        
        return race_results
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

url = "https://www.racing-reference.info/loopdata/2023-18/W/"

fetchRaceData(url)
