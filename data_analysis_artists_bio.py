
#%%
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
from tabulate import tabulate

#%%
# Load the CSV
df = pd.read_csv('scrape_arch_biennale_artists_bio.csv')

# Display the first 50 rows of the DataFrame as a scrollable table
display(HTML(df.head(10).to_html(classes='table table-striped table-hover', max_rows=50, max_cols=10, notebook=True)))
# %%
#Count the number of raws
df.shape[0]
# Check if there are person_id duplicates
df['person_id'].nunique()

    #366 more raws which is weird compared if the first file was artists.csv!
# %%
#calculate of N/a or missing values for each column
df.isna().sum()
#Give me the percentage of missing values for each column
df.isna().mean()*100

#%%
#Something went wrong with the scraping?
# Top 10 most popular artists
top_10_artists = df['person_name'].value_counts().head(10)
print(tabulate(top_10_artists.reset_index(), headers=['Top 10 most common artists:', 'Count'], tablefmt='pretty'))

# Top 10 most popular birth countries
top_10_birth_countries = df['birth_country'].value_counts().head(10)
print(tabulate(top_10_birth_countries.reset_index(), headers=['Top 10 most common birth countries', 'Count'], tablefmt='pretty'))
# %%
# Top 25 most popular birth countries
top_25_birth_countries_and_count = df['birth_country'].value_counts().head(25)
print(top_25_birth_countries_and_count)
print()

# Convert to a comma-separated list
country_list = ', '.join(top_25_birth_countries_and_count.index.tolist())
print(country_list)
# %%
