#%%
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#%%
# Setting the default figure parameters to de-frame the upper x-axis, left y-axis, and right y-axis
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.left'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['ytick.left'] = False
plt.rcParams['axes.grid'] = True  # Ensure grid lines are enabled
plt.rcParams['axes.grid.which'] = 'major'  # Apply grid lines only to major ticks
plt.rcParams['axes.grid.axis'] = 'y'  # Only show horizontal grid lines
plt.rcParams['grid.linestyle'] = '--'  # Set grid line style to dashed
plt.rcParams['grid.alpha'] = 0.3  # Set grid line transparency

#%%
box_info=pd.read_csv('scraped_data_biennale_maininfo.csv')
Title_urls=list(set("https://asac.labiennale.org/attivita/arti-visive/annali?anno="+box_info['year'].astype(str)))
service = Service("/opt/homebrew/bin/geckodriver")
driver = webdriver.Firefox(service=service)

#%%
# Initialize a list to store all data
all_data = []

# Loop over each URL
for url in Title_urls:
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(3)

    # Click the cookie banner button if present
    try:
        cookie_button = driver.find_element(By.CSS_SELECTOR, "#__next > div > footer > div.CookieBanner_banner__kcn5h.CookieBanner_bannerIsOpen__vFJEY > div > button")
        cookie_button.click()
        time.sleep(3)  # Wait after closing the cookie banner
    except:
        print(f"Cookie banner not found or already closed for {url}")
    
    # Click on the tab with selector #react-tabs-2
    try:
        tab = driver.find_element(By.CSS_SELECTOR, "#react-tabs-2")
        tab.click()
        time.sleep(3)  # Wait for the tab content to load
    except:
        print(f"Tab #react-tabs-2 not found for {url}")
        continue  # Skip to the next URL if the tab is not found
    
    # Locate all 'li' elements under the specified 'ul' class
    items = driver.find_elements(By.CSS_SELECTOR, 'ul.Dettaglio_itemInTabList__m0uZU > li')

    # Loop through the 'li' elements and extract data
    for item in items:
        try:
            a_tag = item.find_element(By.TAG_NAME, 'a')
            artist_name = a_tag.text
            artist_url = a_tag.get_attribute('href')
            
            # Add data to list
            all_data.append({
                'Artist_name': artist_name,
                'Artist_url': artist_url,
                'Biennale_url': url  # Store the current URL as 'Biennale_url'
            })
        except:
            print(f"Error processing item in {url}")
            continue  # Skip to the next item if there's an issue

# Close the browser
driver.quit()

# Convert the data to a DataFrame
df = pd.DataFrame(all_data)

# Print the DataFrame
print(df)


# %%
df['Year']=df['Biennale_url'].str.extract(r'(\d{4})')
# Optionally, save to CSV
df.to_csv('scraped_data_artists.csv', index=False)


# %%
df.head()
# %% Plot some figures
df=pd.read_csv('scraped_data_artists.csv')

plt.figure(figsize=(8, 4), dpi=300)
sns.countplot(data=df, x='Year',palette='BuPu')
plt.show()

#%%
df['Artist_url'].nunique()

# %%
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
year_counts = df['Year'].value_counts().reset_index()
year_counts.columns = ['Year', 'Count']
year_counts = year_counts.sort_values('Year')

# Plot using a bar plot with precise year intervals
plt.figure(figsize=(8, 4), dpi=300)
plt.bar(year_counts['Year'], year_counts['Count'], width=0.9, color='lightsteelblue')

# Customize labels
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Count of Artists by Year')

# Adjust the x-axis to reflect the correct year intervals
plt.xticks(year_counts['Year'], rotation=30)

# Display the plot
plt.show()

# %% Who are the most occured ones
# Get the top 10 most common architects and their counts
top_artists = df['Artist_name'].value_counts().head(10).reset_index()
top_artists.columns = ['Artist_name', 'count']
print(top_artists)

# Plot the top 10 most common architects vertically
plt.figure(figsize=(4, 3), dpi=300)
sns.barplot(data=top_artists, x='count', y='Artist_name', palette='BuPu')
plt.xlabel('Count')
plt.ylabel('Artists')
plt.title('Top 10 Most Common Artists')

# Display the plot
plt.show()

#%%
artists_count=df['Artist_name'].value_counts()
artists_count.columns=['Artist_name','count']
artists_count[artists_count>1]
