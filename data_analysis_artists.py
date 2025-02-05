
#%%
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML

#%%
# Load the CSV file where we will delate years 1974 (no Art exhibit) and 1975 (joint exhibition with Architecture Biennale) [cfr. Venice Biennale ASAC Database]
# Deleted raws: 336
df = pd.read_csv('scrape_arch_biennale_artists_years_cleaned.csv')
#%%
# only unqiue artists or eveng group?
# contact curator switzerland 2024

# %%
#Count the number of raws
df.shape[0]
# Check if there are person_id duplicates
df['Artist_url'].nunique()
df.head(50)
#%%
# Count unique Artist URLs
# 1974,1975 raws deleted = 336
unique_artist_urls = df['Artist_url'].nunique()
print(f"Number of unique artist URLs: {unique_artist_urls}")

#%%
# Count unique Artist names
# Los of 26 names compared to URLs
unique_artist_urls = df['Artist_name'].nunique()
print(f"Number of unique artist names: {unique_artist_urls}")
#%%
# Count the number of unique years [60] (1974, 1975 deleted)
num_bars = df['Year'].nunique()
print(f"Number of unique years (barchart): {num_bars}")

#%% Unique years of the Venice Biennales
    # Missing years: 1916, 1918 (WWI), 1944, 1946 (WWII).
    # Strange years: 1990 ('shocking' exhibition > safty ocncearns)[https://www.labiennale.org/en/history-biennale-arte], 1993 (organisational changes) [https://www.academia.edu/43761255/Towards_a_Contemporary_Venice_Biennale_Reassessing_the_Impact_of_the_1993_Exhibition_paper_?utm_source=chatgpt.com]
unique_years = df['Year'].unique()
print(f"Unique years: {sorted(unique_years)}")

#%% Count of Artists by Years
year_counts = df['Year'].value_counts().sort_index()
print(year_counts)

    # Need to be confirmed with the Venice Biennale website. Where is the problem (group exhibitions)?
    # 331 Artists in the International Exhibition [https://www.labiennale.org/en/news/biennale-arte-2024-closes-700000-tickets-sold#:~:text=With%20an%2018%25%20increase%20over,3%2C300%20visitors%20per%20day)%2C%20in]
#[https://universes.art/en/venice-biennale/2024/artists]

    # H1: The number of artists per year is the sum of national pavilions artists + arensale. (https://en.wikipedia.org/wiki/List_of_national_pavilions_at_the_60th_Venice_Biennale?utm_source=chatgpt.com) > 272 artists + 331 arensale (VB website) = 603 artists
    # H2 = maybe overlapping between np and arsnale?
    #wiki_list > cleaned manually = 265 (9 extra artists after having added 331)
    # H3 = 9 artists did both? (np and arsenale?) H4 = error in cleaning.
#We use compare softwares to find the differences between the two lists. (Claire Fontaine also both (the 311 ‘regular’ listed at Universes in Universe, and the Wikipedia list of artists from the pavilions, Yinka Shonibare)
# NP + arsenale : same artists but with different Event ID. If he has exhibited in different spaces (NP and Arsenale), he will be collected mutliple times.

#- president and GDirector
#- artists NP + artists Arsenale
    #- oepra roles: 

# %%
# Calculate the average number of artists per year [582.30]
average_artists_per_year = df.groupby('Year')['Artist_name'].nunique().mean()
print(f"Average number of artists per year: {average_artists_per_year:.2f}")
#%%

# Count of Artists by Years
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.left'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['ytick.left'] = False
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.grid.which'] = 'major'
plt.rcParams['axes.grid.axis'] = 'y'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5

# Create the count plot
plt.figure(figsize=(16, 6), dpi=300)
sns.countplot(data=df, x='Year', color='orange') #The sns.countplot function automatically counts the occurrences of each unique value in the Year column of the DataFrame df.

# Add an average line at the calculated average count
plt.axhline(y=average_artists_per_year, color='r', linestyle='--', label=f'Average Count ({average_artists_per_year:.2f})')

# Add labels and title
plt.xlabel('Year', fontsize=14, labelpad=20)
plt.ylabel('Count', fontsize=14, labelpad=20)
plt.title('Count of Artists_urls by Year', fontsize=16, pad=30)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Set x-axis ticks to show every 10 years using the actual years from the DataFrame
years = sorted(df['Year'].unique())
plt.xticks(ticks=range(0, len(years), 10), labels=[years[i] for i in range(0, len(years), 10)])

# Display the plot
plt.show()
# %% Who are the most occured artists

# Get the top most common artists and their counts
top_artists = df['Artist_name'].value_counts().reset_index()
top_artists.columns = ['Artist_name', 'count']

# Convert the DataFrame to HTML and make it scrollable
html_table = top_artists.to_html(index=False)
scrollable_table = f"""
<div style="max-height: 400px; overflow-y: scroll; border: 1px solid #ccc;">
    {html_table}
</div>
"""

# Display the scrollable table
display(HTML(scrollable_table))

# %%
# Calculate the average number of Venice Biennale exhibitions attended by artists [1.84]

# Get the top most common artists and their counts
top_artists = df['Artist_name'].value_counts().reset_index()
top_artists.columns = ['Artist_name', 'count']

# Calculate the average count
average_count = top_artists['count'].mean()
print(f"Average count of top artists: {average_count:.2f}")

# %%
# Calculate the average number of Venice Biennale exhibitions attended by top 100 artists [15.26]
# Get the top most common artists and their counts
top_artists = df['Artist_name'].value_counts().reset_index()
top_artists.columns = ['Artist_name', 'count']

# Select only the top 100 artists
top_100_artists = top_artists.head(100)

# Calculate the average count for the top 100 artists
average_count_top_100 = top_100_artists['count'].mean()
print(f"Average count of top 100 artists: {average_count_top_100:.2f}")
# %%
# Plotting the bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_100_artists['Artist_name'], top_100_artists['count'], color='skyblue')
plt.axhline(y=average_count_top_100, color='r', linestyle='--', label=f'Average Count ({average_count_top_100:.2f})')
plt.xlabel('Artist Names')
plt.ylabel('Count')
plt.title('Top Artists and Their Exhibition Counts')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.show()
# %%
