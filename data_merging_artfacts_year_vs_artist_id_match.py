# %%
import pandas as pd
from IPython.display import display, HTML

#%%
# Load the CSV files into DataFrames
file_path_1 = 'produced_data_artfacts_year_vs_artist_id_match.csv'
file_path_2 = '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/scrape_arch_artfacts_artist_2024_Yiuxan_dropbox.csv'

data_1 = pd.read_csv(file_path_1)
data_2 = pd.read_csv(file_path_2)

#%%
# Display the first few rows of the first DataFrame in a scrollable table
html_1 = data_1.to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_1}</div>'))

#%%
# DATA_1 : CLEANING URL > IDS

# Make a copy of the first DataFrame
data_1_copy = data_1.copy()

# Change the column name artist_url to artist_id
data_1_copy.rename(columns={'artist_url': 'artist_id'}, inplace=True)

# Extract the ID from the artist_url column
data_1_copy['artist_id'] = data_1_copy['artist_id'].apply(lambda x: x.split('/')[-1])

# Display the modified DataFrame in a scrollable table
html_copy = data_1_copy.to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_copy}</div>'))

#%%
# Display the first few rows of the first DataFrame in a scrollable table
html_1 = data_2.to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_1}</div>'))

# %%
# DATA_2 : CLEANING

# Make a copy of the second DataFrame
data_2_copy = data_2.copy()

# Keep only the id column
data_2_copy = data_2_copy[['id']]

# Rename the column to artist_id
data_2_copy.rename(columns={'id': 'artist_id'}, inplace=True)

# Add a new column and call it year
data_2_copy['year'] = 2024

# Invert the position of the columns
data_2_copy = data_2_copy[['year', 'artist_id']]

# Display the first few rows of the modified DataFrame in a scrollable table
html_1 = data_2_copy.to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_1}</div>'))

#%%
# Print the number of rows and unique artist_id for both datasets
print(f"data_1_copy: Number of rows = {len(data_1_copy)}, Unique artist_id = {data_1_copy['artist_id'].nunique()}")
print(f"data_2_copy: Number of rows = {len(data_2_copy)}, Unique artist_id = {data_2_copy['artist_id'].nunique()}")
# %%

# Merge the two datasets by putting data_2_copy rows before data_1_copy
merged_data = pd.concat([data_2_copy, data_1_copy], ignore_index=True)

# Display the first few rows of the modified DataFrame in a scrollable table
html_1 = merged_data.to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_1}</div>'))

#%%
# Print the number of rows and unique artist_id for bomerged_data
print(f"merged_data: Number of rows = {len(merged_data)}, Unique artist_id = {merged_data['artist_id'].nunique()}")
# %%

# Export the merged DataFrame to a CSV file on the desktop
output_file_path = '/Users/jac/Desktop/produced_data_artfacts_year_vs_artist_id_match_complete.csv'
merged_data.to_csv(output_file_path, index=False)
# %%

# Add a column called exhibition_id
merged_data['exhibition_id'] = None

# Set exhibition_id to 1131238 for the year 2024
merged_data.loc[merged_data['year'] == 2024, 'exhibition_id'] = 1131238

# Display the first few rows of the modified DataFrame in a scrollable table
html_1 = merged_data.to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_1}</div>'))


#%%
# Load the CSV file into a DataFrame
file_path = '/Users/jac/Desktop/scrape_arch_artfatcs_raw_50.csv'
df_artfacts_raw = pd.read_csv(file_path)

# Display the first few rows of the DataFrame in a scrollable table
html = df_artfacts_raw.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html}</div>'))
# %%
# VENICE BIENNALE INSTITUTION_ID = 2367

#%%
# Create a copy of df_artfacts_raw with only the data where institution_id = 2367
df_venice_biennale = df_artfacts_raw[df_artfacts_raw['institution_id'] == 2367].copy()

# Display the first few rows of the filtered DataFrame in a scrollable table
html_venice = df_venice_biennale.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_venice}</div>'))
# %%
# Create a new DataFrame named df_VBs_ids
df_VBs_ids = pd.DataFrame()

# Create the 'year' column by extracting the first 4 digits from 'begin_date'
df_VBs_ids['year'] = df_venice_biennale['begin_date'].str[:4]

# Create the 'exhibition_id' column by extracting the 'id' column
df_VBs_ids['exhibition_id'] = df_venice_biennale['id']

# Order the df_VBs_ids chronologically by the 'year' column
df_VBs_ids = df_VBs_ids.sort_values(by='year')

# Display the first few rows of the filtered DataFrame in a scrollable table
html_venice = df_VBs_ids.head().to_html(classes='table table-striped', max_rows=10, max_cols=10, index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_venice}</div>'))

# %%
# Print the number of rows and unique exhibition_id
num_rows = len(df_VBs_ids)
num_unique_ids = df_VBs_ids['exhibition_id'].nunique()
print(f"Number of rows: {num_rows}, Unique exhibition_id: {num_unique_ids}")
# %%

# Display the first few rows of the filtered DataFrame in a scrollable table
html_venice = df_VBs_ids.head().to_html(classes='table table-striped', max_rows=10, max_cols=10, index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_venice}</div>'))

# Display the first few rows of the modified DataFrame in a scrollable table
html_1 = merged_data.to_html(classes='table table-striped', max_rows=10, max_cols=10, index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_1}</div>'))
#%%

# Convert the 'year' columns to string in both DataFrames and drop the existing 'exhibition_id' in merged_data
merged_on_year = pd.merge(
    merged_data.drop(columns=['exhibition_id']).assign(year=lambda x: x['year'].astype(str)),
    df_VBs_ids[['year', 'exhibition_id']].assign(year=lambda x: x['year'].astype(str)),
    on='year',
    how='left'
)

# Display the merged result in a scrollable table
html_merged = merged_on_year.head().to_html(classes='table table-striped', max_rows=10, max_cols=10, index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html_merged}</div>'))
# %%
pd.set_option('display.max_rows', None)  # Allows printing all rows
print(merged_on_year)
# %%

# 1. For the year 2024, set exhibition_id to 1131238
merged_on_year.loc[merged_on_year['year'] == '2024', 'exhibition_id'] = 1131238

# 2. Remove any trailing ".0" in the exhibition_id values, keeping only the numbers before
merged_on_year['exhibition_id'] = (
    merged_on_year['exhibition_id']
    .astype(str)
    .str.replace(r'\.0$', '', regex=True)
)

pd.set_option('display.max_rows', None)  # Allows printing all rows
print(merged_on_year)
# %%
# Export the merged DataFrame to a CSV file on the desktop
output_file_path = '/Users/jac/Desktop/produced_data_artfacts_year_vs_artist_id_match_complete.csv'
merged_on_year.to_csv(output_file_path, index=False)
# %%
