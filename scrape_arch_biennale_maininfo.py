#%%
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#Find the right version of the. webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# Create a Service object with the path from ChromeDriverManager
service = Service(ChromeDriverManager().install())
# Pass the service object to webdriver.Chrome
driver = webdriver.Chrome(service=service)

#%%
# Define the range of years to scrape
years = range(1895, 2025)  # Adjust the range if necessary

# Initialize a list to store all data
all_data = []

# Loop over each year
for year in years:
    url = f"https://asac.labiennale.org/attivita/arti-visive/annali?anno={year}" #Change the url based on what we want to scrape (from Architecture to arti-visive)

     # Open the webpage for the current year
    driver.get(url)

    # Sleep for 5 seconds to wait for the page to load
    time.sleep(5)
    
    # Try to get the title text from the h2 > font > font
    try:
        title = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > main > article > header > div > h2 ").text
    except:
        title = None  # If the title doesn't exist, set it to None
    
    # Locate all dl > div elements
    items = driver.find_elements(By.CSS_SELECTOR, "#__next > div > div > main > article > header > div > dl > div")
    
    for item in items:
        # Get the text for the first column (dt)
        col1 = item.find_element(By.CSS_SELECTOR, "dt").text
        
        # Locate all dd elements under the same item
        dds = item.find_elements(By.CSS_SELECTOR, "dd")
        
        for dd in dds:
            # Check if dd contains a link (a) or a span
            try:
                col2_element = dd.find_element(By.CSS_SELECTOR, "a")
                col2 = col2_element.text
                href = col2_element.get_attribute("href")  # Get the link href
            except:
                col2_element = dd.find_element(By.CSS_SELECTOR, "span")
                col2 = col2_element.text
                href = None  # No link, set href as None
            
            # Get HTML content if present
            col2_html = col2_element.get_attribute('innerHTML')
            
            # Append the data for this row, including the year and title
            all_data.append({
                'year': year,
                'Title': title,
                'Items': col1,
                'Text': col2,
                'html': col2_html,
                'href': href
            })

# Close the browser
driver.quit()

# Convert the data to a DataFrame
df = pd.DataFrame(all_data)

# %%
# To clean all the years where there has not been a Biennale but the years open a main page anycase.
# Optionally, save to CSV
df=df.sort_values(by='year', ascending=False)
df=df.drop_duplicates(subset=['Title', 'Items','Text'], keep='first')
df.to_csv('scraped_data_biennale_maininfo.csv', index=False)

# %%
df.head()
# %%
df['Title_url']='https://asac.labiennale.org/attivita/arti-visive/annali?anno='+df['year'].astype(str)
df.to_csv('scraped_data_biennale_maininfo.csv', index=False)
# %%