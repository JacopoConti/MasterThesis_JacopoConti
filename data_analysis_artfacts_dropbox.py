#%%
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display, HTML
from datetime import datetime
# %%
# Load the CSV files
df_artists_2024 = pd.read_csv('/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/scrape_arch_artfacts_artist_2024_Yiuxan_dropbox.csv')
df_artists_info_all = pd.read_csv('/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/scrape_arch_artfacts_artist_info_all_dropbox.csv')
#%%
# Display the head of the two tables in a scrollable format
display(HTML(df_artists_2024.head().to_html(classes='table table-striped table-hover', max_rows=10)))
display(HTML(df_artists_info_all.head().to_html(classes='table table-striped table-hover', max_rows=10)))

# %%
# Create a new column 'id' (df_artists_info_all) and populate it with the 'url' column
df_artists_info_all['id'] = df_artists_info_all['url']

# Clean the 'id' column to remove the 'https://' part and keep the last digits
df_artists_info_all['id'] = df_artists_info_all['id'].apply(lambda x: x.split('/')[-1])

# Display the updated DataFrame
display(HTML(df_artists_info_all.head().to_html(classes='table table-striped table-hover', max_rows=10, max_cols=10)))

# %%
#CLEANING DF_ARTISTS_2024

# 1. Drop columns 'first_name' and 'last_name'
df_artists_2024.drop(columns=['first_name', 'last_name'], inplace=True)

# 2. Remove the '.0' after the 4 digits date in 'birth_year' and 'death_year'
df_artists_2024['birth_year'] = (
    df_artists_2024['birth_year']
    .astype(str)
    .str.replace('.0', '', regex=False)
)
df_artists_2024['death_year'] = (
    df_artists_2024['death_year']
    .astype(str)
    .str.replace('.0', '', regex=False)
)

# 3. Rename 'country_index' --> 'country_index_birth' and clean 'birth_location'
df_artists_2024.rename(columns={'country_index': 'country_index_birth'}, inplace=True)
df_artists_2024['country_index_birth'] = df_artists_2024['birth_location'].str.extract(r'\(([^)]+)\)')
df_artists_2024['birth_location'] = df_artists_2024['birth_location'].str.replace(r'\s*\([^)]*\)', '', regex=True)

# (Reorder columns so that 'country_index_birth' is right after 'birth_location')
cols = list(df_artists_2024.columns)
birth_location_index = cols.index('birth_location')
cols.insert(birth_location_index + 1, cols.pop(cols.index('country_index_birth')))
df_artists_2024 = df_artists_2024[cols]

# 4. Transform 'm' to 'Male' and 'f' to 'Female' in the 'gender' column
df_artists_2024['gender'] = df_artists_2024['gender'].replace({'m': 'Male', 'f': 'Female'})

# 5. Remove just the parentheses in 'death_location'
df_artists_2024['death_location'] = df_artists_2024['death_location'].str.replace(r'[()]', '', regex=True)

# 6. Add 'country_index_death' just after 'death_location' 
#    and transfer 2 uppercase letters from 'death_location' into it, then remove them.
df_artists_2024['country_index_death'] = df_artists_2024['death_location'].str.extract(r'\b([A-Z]{2})\b')
df_artists_2024['death_location'] = (
    df_artists_2024['death_location']
    .str.replace(r'\b[A-Z]{2}\b', '', regex=True)
    .str.strip()
)

cols = list(df_artists_2024.columns)
death_location_index = cols.index('death_location')
cols.insert(death_location_index + 1, cols.pop(cols.index('country_index_death')))
df_artists_2024 = df_artists_2024[cols]

# 7. Replace any empty strings with NaN across the entire DataFrame
df_artists_2024.replace(r'^\s*$', np.nan, regex=True, inplace=True)

# 8. Change 'url' column name to 'profile_link'
df_artists_2024.rename(columns={
    'sector': 'period',
}, inplace=True)

# Display the updated DataFrame
display(HTML(df_artists_2024.head().to_html(classes='table table-striped table-hover', max_rows=100)))

# %%
# CLEANING DF_ARTISTS_INFO_ALL

# 1. Bring the 'id' column to be the first column
cols = list(df_artists_info_all.columns)
cols.insert(0, cols.pop(cols.index('id')))  # remove 'id' and insert at index 0
df_artists_info_all = df_artists_info_all[cols]

# 2. After the 'name' column, add 6 new columns: 
#    'birth_year', 'birth_location', 'country_index_birth', 
#    'death_year', 'death_location', 'country_index_death'.
#    (We'll fill them in steps 3-5.)

df_artists_info_all['birth_year'] = ''
df_artists_info_all['birth_location'] = ''
df_artists_info_all['country_index_birth'] = ''
df_artists_info_all['death_year'] = ''
df_artists_info_all['death_location'] = ''
df_artists_info_all['country_index_death'] = ''

new_order = []
for col in df_artists_info_all.columns:
    new_order.append(col)
    if col == 'name':
        new_order.extend([
            'birth_year', 'birth_location', 'country_index_birth',
            'death_year', 'death_location', 'country_index_death'
        ])
# Remove duplicates in case they were appended twice
new_order = list(dict.fromkeys(new_order))
df_artists_info_all = df_artists_info_all[new_order]

# 3. Extract the 4-digit year from 'Born' into 'birth_year', 
#    and from 'Death' into 'death_year'.
df_artists_info_all['birth_year'] = df_artists_info_all['Born'].str.extract(r'(\d{4})')
df_artists_info_all['death_year'] = df_artists_info_all['Death'].str.extract(r'(\d{4})')

# 4. Extract the location name after the '|' and before the '(' 
#    for 'birth_location' and 'death_location'.
df_artists_info_all['birth_location'] = df_artists_info_all['Born'].str.extract(r'\|\s*(.*?)\s*\(')
df_artists_info_all['death_location'] = df_artists_info_all['Death'].str.extract(r'\|\s*(.*?)\s*\(')

# 5. Extract the content inside parentheses for Born into 'country_index_birth',
#    and for Death into 'country_index_death'.
df_artists_info_all['country_index_birth'] = df_artists_info_all['Born'].str.extract(r'\((.*?)\)')
df_artists_info_all['country_index_death'] = df_artists_info_all['Death'].str.extract(r'\((.*?)\)')

# 6. Drop the 'Born' and 'Death' columns
df_artists_info_all.drop(columns=['Born', 'Death'], inplace=True)

# 7. Change 'url' column name to 'profile_link'
df_artists_info_all.rename(columns={
    'url': 'profile_link',
    'Gender': 'gender',
    'Nationality': 'nationality',
    'Media': 'media',
    'Period': 'period'
}, inplace=True)

# 8. Move 'profile_link' column as the last column
cols = list(df_artists_info_all.columns)
cols.append(cols.pop(cols.index('profile_link')))
df_artists_info_all = df_artists_info_all[cols]

# 9. Swap the positions of 'nationality' and 'gender' columns
gender_index = cols.index('gender')
nationality_index = cols.index('nationality')
cols[gender_index], cols[nationality_index] = cols[nationality_index], cols[gender_index]
df_artists_info_all = df_artists_info_all[cols]


# 9. Swap the positions of 'period' and 'media' columns
media_index = cols.index('media')
period_index = cols.index('period')
cols[media_index], cols[period_index] = cols[period_index], cols[media_index]
df_artists_info_all = df_artists_info_all[cols]

# Display the updated DataFrame
display(HTML(df_artists_info_all.head().to_html(classes='table table-striped table-hover', max_rows=10)))


# %%
# STATISTICAL ANALYSIS dfs
# Number of unique IDs and number of rows for df_artists_2024
num_unique_ids_artists_2024 = df_artists_2024['id'].nunique()
num_rows_artists_2024 = df_artists_2024.shape[0]

# Number of unique IDs and number of rows for df_artists_info_all
num_unique_ids_artists_info_all = df_artists_info_all['id'].nunique()
num_rows_artists_info_all = df_artists_info_all.shape[0]

# Print the results
print(f"Number of unique IDs in df_artists_2024: {num_unique_ids_artists_2024}")
print(f"Number of rows in df_artists_2024: {num_rows_artists_2024}")
print(f"Number of unique IDs in df_artists_info_all: {num_unique_ids_artists_info_all}")
print(f"Number of rows in df_artists_info_all: {num_rows_artists_info_all}")
# %%
# MERGING THE TWO DATAFRAMES
# Convert id columns to same type
df_artists_info_all['id'] = df_artists_info_all['id'].astype(str)
df_artists_2024['id'] = df_artists_2024['id'].astype(str)

# Merge dataframes
df_artfacts_complete = pd.merge(
    df_artists_info_all, 
    df_artists_2024,
    how='outer',
    on='id',
    suffixes=('_info', '_2024')
)

# Combine duplicate columns where needed
for col in df_artfacts_complete.columns:
    if col.endswith('_info'):
        base_col = col[:-5]  # Remove '_info' suffix
        col_2024 = base_col + '_2024'
        if col_2024 in df_artfacts_complete.columns:
            # Combine columns, preferring non-null values from _2024
            df_artfacts_complete[base_col] = df_artfacts_complete[col_2024].fillna(df_artfacts_complete[col])
            # Drop the duplicate columns
            df_artfacts_complete = df_artfacts_complete.drop([col, col_2024], axis=1)

# Display result
display(HTML(df_artfacts_complete.head().to_html(classes='table table-striped table-hover', max_rows=10)))
# %%
# STATISTICAL ANALYSIS df_artfacts_complete

# Number of unique IDs and number of rows for df_artfacts_complete
num_unique_ids_artists_2024 = df_artfacts_complete['id'].nunique()
num_rows_artists_2024 = df_artfacts_complete.shape[0]

# Print the results
print(f"Number of unique IDs in df_artfacts_complete: {num_unique_ids_artists_2024}")
print(f"Number of rows in df_artists_2024: {num_rows_artists_2024}")
# %%

# Create filename with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
filename = f"produced_data_artfacts_VB_artists_complete_{timestamp}.csv"

# Get desktop path for macOS
desktop_path = os.path.expanduser("~/Desktop")
full_path = os.path.join(desktop_path, filename)

# Export to CSV
df_artfacts_complete.to_csv(full_path, index=False)

# %%
