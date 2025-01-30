
#%%
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
from tabulate import tabulate
from pprint import pprint
import csv
import os
#%%
# Load the CSVs
df = pd.read_csv('scrape_arch_biennale_artists_bio.csv')
df_produced_data_GS_countries_ita_list = pd.read_csv('produced_data_GS_countries_ita_list.csv')
#df_produced_data_artists_bio_birth_country_list = pd.read_csv('produced_data_artists_bio_birth_country_list.csv')

# Display the first 50 rows of the DataFrame as a scrollable table
display(HTML(df.head(10).to_html(classes='table table-striped table-hover', max_rows=50, max_cols=10, notebook=True)))

# Display the first 50 rows of the DataFrame as a scrollable table
display(HTML(df_produced_data_GS_countries_ita_list.head(10).to_html(classes='table table-striped table-hover', max_rows=50, max_cols=10, notebook=True)))
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
# Get a unique list of all countries cited in birth_country
unique_countries = df['birth_country'].unique()

# Convert all items to strings and filter out any NaN values
unique_countries_str = [str(country) for country in unique_countries if pd.notna(country)]

# Sort the list in ascending alphabetical order
unique_countries_str.sort()

# Print the list in a more readable format
html = "<div style='max-height: 200px; overflow-y: scroll;'><pre>{}</pre></div>".format('\n'.join(unique_countries_str))
display(HTML(html))
# %%
#exporting the list as a CSV file on my desktop
# Define the file path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "artists_bio_birth_country_list.csv")

# Write the list to a CSV file
with open(desktop_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    for country in unique_countries_str:
        writer.writerow([country])

print(f"CSV file has been created at {desktop_path}")

#%%
GS_countries_ita = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua e Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Azerbaigian', 'Bahamas', 'Bahrein', 'Bangladesh', 'Barbados', 'Bielorussia', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia ed Erzegovina', 'Botswana', 'Brasile', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambogia', 'Camerun', 'Capo Verde', 'Repubblica Centrafricana', 'Chad', 'Isole del Canale', 'Chile', 'Cina', 'Cina, Regione amministrativa speciale di Macao', 'Colombia', 'Comore', 'Congo', 'Congo, Repubblica Democratica del', 'Costa Rica', "Costa d'Avorio", 'Croazia', 'Cuba', 'Cipro', 'Repubblica Ceca', 'Gibuti', 'Dominica', 'Repubblica Dominicana', 'Ecuador', 'Egitto', 'El Salvador', 'Guinea Equatoriale', 'Eritrea', 'Etiopia', 'Figi', 'Guyana Francese', 'Polinesia Francese', 'Gabon', 'Gambia', 'Georgia', 'Ghana', 'Grenada', 'Guadalupa', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'India', 'Indonesia', "Iran, Repubblica Islamica dell'", 'Iraq', 'Giamaica', 'Giordania', 'Kazakistan', 'Kenya', 'Kiribati', 'Corea, Repubblica Popolare Democratica del', 'Kuwait', 'Kirghizistan', 'Laos, Repubblica Democratica Popolare del', 'Libano', 'Lesotho', 'Liberia', 'Libia', 'Madagascar', 'Malawi', 'Malesia', 'Maldive', 'Mali', 'Malta', 'Isole Marshall', 'Martinica', 'Mauritania', 'Mauritius', 'Mayotte', 'Messico', 'Micronesia, Stati Federati di', 'Mongolia', 'Montenegro', 'Marocco', 'Mozambico', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Antille Olandesi', 'Nuova Caledonia', 'Nicaragua', 'Niger', 'Nigeria', 'Oman', 'Pakistan', 'Palau', 'Territorio palestinese occupato', 'Panama', 'Papua Nuova Guinea', 'Paraguay', 'Perù', 'Filippine', 'Porto Rico', 'Qatar', 'Repubblica di Moldavia', 'Riunione', 'Romania', 'Federazione Russa', 'Ruanda', 'Saint Kitts e Nevis', 'Saint Lucia', 'Saint Vincent e Grenadine', 'Samoa', 'Sao Tome e Principe', 'Arabia Saudita', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovacchia', 'Isole Salomone', 'Somalia', 'Sudafrica', 'Sudan del Sud', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Repubblica araba siriana', 'Taiwan', 'Tagikistan', 'Tanzania, Repubblica Unita di', 'Thailandia', 'Ex Repubblica Jugoslava di Macedonia', 'Timor Est', 'Togo', 'Tonga', 'Trinidad e Tobago', 'Tunisia', 'Turchia', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ucraina', 'Emirati Arabi Uniti', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Isole Vergini', 'Sahara Occidentale', 'Yemen', 'Zambia', 'Zimbabwe']

#%%
# Add a new empty column named artist_birthplace_country_GS to the existing DataFrame
df['artist_birthplace_country_GS'] = 0

# Populate the column based on the comparison
df['artist_birthplace_country_GS'] = df['birth_country'].apply(
    lambda x: 1 if x in GS_countries_ita else 0
)

# Ensure that unsuccessful matches are marked with 0
df['artist_birthplace_country_GS'] = df['artist_birthplace_country_GS'].apply(
    lambda x: 0 if x != 1 else 1
)

# Calculate the number and percentage of unsuccessful matches
unsuccessful_matches = df['artist_birthplace_country_GS'].value_counts().get(0, 0)
total_entries = len(df)
percentage_unsuccessful = (unsuccessful_matches / total_entries) * 100

print(f"Number of unsuccessful matches: {unsuccessful_matches}")
print(f"Percentage of unsuccessful matches: {percentage_unsuccessful:.2f}%")
# %%
df.head(50)
# %%
