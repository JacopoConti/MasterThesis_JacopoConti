
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
df_cleaned = pd.read_csv('scrape_arch_biennale_artists_years_cleaned.csv')
df_bio_GS = pd.read_csv('produced_data_biennale_artists_bio_GS_1_0.csv')

#%%
#%% Count of Artists by Years
year_counts = df_cleaned['Year'].value_counts().sort_index()
print(year_counts)
# %%
# Calculate the average number of artists per year [582.30]
average_artists_per_year = df_cleaned.groupby('Year')['Artist_name'].nunique().mean()
print(f"Average number of artists per year: {average_artists_per_year:.2f}")

# %%
# Aggiungi la colonna 'id' inizialmente con valori NaN
df_cleaned['id'] = pd.NA  

# Crea un dizionario di mappatura tra 'person_name' e 'person_id' da df_bio_GS
mapping = dict(zip(df_bio_GS['person_name'], df_bio_GS['person_id']))

# Popola la colonna 'id' in df_cleaned con il valore corrispondente di 'person_id'
df_cleaned['id'] = df_cleaned['Artist_name'].map(mapping)

# Converte 'id' in stringa rimuovendo '.0' dai numeri float
df_cleaned['id'] = df_cleaned['id'].apply(lambda x: str(int(x)) if pd.notna(x) else "")

# Verifica il risultato
print(df_cleaned[['Artist_name', 'id']].head())

# Calcola numero e percentuale di match non riusciti
unsuccessful_matches = df_cleaned['id'].eq("").sum()
total_records = len(df_cleaned)
percentage_unsuccessful = (unsuccessful_matches / total_records) * 100

print(df_cleaned[['Artist_name', 'id']].head())
print(f"Unsuccessful matches: {unsuccessful_matches}")
print(f"Percentage of unsuccessful matches: {percentage_unsuccessful:.2f}%")


# %%
# Create a new column 'GS' in df_cleaned
# Map the 'artist_birthplace_country_GS' from df_bio_GS to df_cleaned based on matching 'person_id' and 'id'

# Create a dictionary mapping from df_bio_GS
mapping_gs = dict(zip(df_bio_GS['person_id'].astype(str), df_bio_GS['artist_birthplace_country_GS']))

# Populate the 'GS' column in df_cleaned using the mapping
df_cleaned['GS'] = df_cleaned['id'].map(mapping_gs)

# Verify the result
print(df_cleaned[['Artist_name', 'id', 'GS']].head())
df_cleaned.head(100)

# Calculate number and percentage of unsuccessful matches
unsuccessful_matches = df_cleaned['GS'].isna().sum()
total_records = len(df_cleaned)
percentage_unsuccessful = (unsuccessful_matches / total_records) * 100

# Verify the result
print(df_cleaned[['Artist_name', 'id', 'GS']].head())
print(f"Unsuccessful matches: {unsuccessful_matches}")
print(f"Percentage of unsuccessful matches: {percentage_unsuccessful:.2f}%")

# %%
# Find the row(s) with the name 'Lenora  de Barros'
lenora_row = df_cleaned[df_cleaned['id'] == '410211']

# Display the full row(s)
print(lenora_row)

# %%
# 1. Duplicate df_cleaned and create df_cleaned_GS
df_cleaned_GS = df_cleaned.copy()

# 2. Remove decimal part in the 'GS' column
df_cleaned_GS['GS'] = df_cleaned_GS['GS'].apply(
    lambda x: str(int(float(x))) if pd.notnull(x) else x
)

# 3. Remove decimal part in the 'Year' column
df_cleaned_GS['Year'] = df_cleaned_GS['Year'].apply(
    lambda x: str(int(float(x))) if pd.notnull(x) else x
)

df_cleaned_GS.head(10)

# %%
# Save the DataFrame to the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'data_viz_graph.csv')
df_cleaned_GS.to_csv(desktop_path, index=False)

print(f"File saved successfully to: {desktop_path}")
# %%
# Group by Year and GS, then pivot into separate columns
df_stacked = df_cleaned_GS.groupby(['Year', 'GS']).size().unstack(fill_value=0)

# Create a stacked bar plot
plt.figure(figsize=(16, 6), dpi=300)
df_stacked.plot(kind='bar', stacked=True, ax=plt.gca(), color=['orange', 'green'])

plt.xlabel('Year', fontsize=14, labelpad=20)
plt.ylabel('Count', fontsize=14, labelpad=20)
plt.title('Count of Artists by Year (Stacked by GS status)', fontsize=16, pad=30)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add a legend
plt.legend(title='GS', labels=['Not GS (0)', 'GS (1)'])

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()
# %%
#2024TH EDITION 331 PARTECIPANTS (WEBSITE) VS. BARCHART...

#%%

# Group by Year and GS, then pivot into separate columns
df_stacked = df_cleaned_GS.groupby(['Year', 'GS']).size().unstack(fill_value=0)

# Normalize the counts so each Year sums to 1 (or 100%)
df_stacked_normalized = df_stacked.div(df_stacked.sum(axis=1), axis=0)

# Create a stacked bar plot with normalized values
plt.figure(figsize=(16, 6), dpi=300)
df_stacked_normalized.plot(kind='bar', stacked=True, ax=plt.gca(), color=['orange', 'green'])

plt.xlabel('Year', fontsize=14, labelpad=20)
plt.ylabel('Fraction', fontsize=14, labelpad=20)
plt.title('Normalized Count of Artists by Year (Stacked by GS status)', fontsize=16, pad=30)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add a legend
plt.legend(title='GS', labels=['Not GS (0)', 'GS (1)'])

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()

#%%
# Calculate the average number of artists per year
average_artists_per_year = df_cleaned_GS.groupby('Year')['Artist_name'].nunique().mean()
print(f"Average number of artists per year: {average_artists_per_year:.2f}")

# Group by Year to get the total number of artists per year
df_total_artists = df_cleaned_GS.groupby('Year').size()

# Create a bar plot with the total number of artists per year
plt.figure(figsize=(16, 6), dpi=300)
df_total_artists.plot(kind='bar', color='orange', ax=plt.gca())

# Add an average line at the calculated average count
plt.axhline(y=average_artists_per_year, color='r', linestyle='--', label=f'Average Count ({average_artists_per_year:.2f})')

plt.xlabel('Year', fontsize=14, labelpad=20)
plt.ylabel('Count', fontsize=14, labelpad=20)
plt.title('Total Count of Artists by Year', fontsize=16, pad=30)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add a legend
plt.legend()

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()
# %%

# Print the total number of rows in df_cleaned_GS
print(f"Total number of rows in df_cleaned_GS: {len(df_cleaned_GS)}")

# Print how many NaN values each column has
print("NaN values per column in df_cleaned_GS:")
print(df_cleaned_GS.isna().sum())

# Print how many unique ids there are
unique_id_count = df_cleaned_GS['id'].nunique()
print(f"Number of unique 'id': {unique_id_count}")

# Print how many unique Artist_name there are
unique_artist_name_count = df_cleaned_GS['Artist_name'].nunique()
print(f"Number of unique 'Artist_name': {unique_artist_name_count}")
# %%
#Number of unique 'id': 17650
#Number of unique 'Artist_name': 19007
#HOW IS THAT POSSIBLE?
# 1. WHY THIS DIFFERENCE?
# 2. WHY BIG LOSS OF DATA IN 2024?
# %%
# Verify the total count of artists per year
df_total_artists = df_cleaned_GS.groupby('Year').size()
print("Total count of artists per year:")
html_total_artists = df_total_artists.to_frame().to_html()
display(HTML(f"<div style='max-height: 200px; overflow-y: scroll;'>{html_total_artists}</div>"))

# Group by Year and GS, then pivot into separate columns
df_stacked = df_cleaned_GS.groupby(['Year', 'GS']).size().unstack(fill_value=0)

# Verify the stacked counts
print("Stacked counts by Year and GS:")
html_stacked_counts = df_stacked.to_html()
display(HTML(f"<div style='max-height: 200px; overflow-y: scroll;'>{html_stacked_counts}</div>"))
# %%
