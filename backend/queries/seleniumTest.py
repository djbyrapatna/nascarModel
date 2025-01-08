from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def fetchRaceData(url):
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
        driver = webdriver.Chrome(options=chromeOptions)
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript to load content
        
        html = driver.page_source
        driver.quit()
        
        tables = pd.read_html(html)
        print(f"Tables found: {len(tables)} in {url}")
        
        if len(tables) > 4:
            return tables[4]
        else:
            print(f"No expected table found in {url}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Example Usage
if __name__ == "__main__":
    testUrl = "https://www.racing-reference.info/race-results/2023-19/W/"
    raceData = fetchRaceData(testUrl)
    if raceData is not None:
        print(raceData.head())
    else:
        print("Failed to fetch data.")
