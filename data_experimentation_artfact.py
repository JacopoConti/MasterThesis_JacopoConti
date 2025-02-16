#%%
import pandas as pd
import os
import ast
from IPython.display import display, HTML
from fuzzywuzzy import fuzz
#%%
# List of CSV files to import
csv_files = [
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000000.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000001.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000002.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000003.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000004.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000005.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000006.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000007.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000008.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000009.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000010.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000011.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000012.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000013.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000014.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000015.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000016.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000017.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000018.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000019.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000020.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000021.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000022.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000023.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000024.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000025.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000026.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000027.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000028.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000029.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000030.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000031.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000032.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000033.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000034.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000035.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000036.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000037.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000038.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000039.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000040.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000041.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000042.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000043.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000044.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000045.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000046.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000047.csv',
    '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000048.csv',
  '/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/artfacts_raw/000000000049.csv'
]
#%%
# Import all CSV files into individual DataFrames and delete specified columns
df_list = []
columns_to_delete = [
    'links_thumb', 'links_image', 'links_card', 'links_profile',
    'description', 'country_links_profile', 'caption'
]

for file in csv_files:
    df = pd.read_csv(file, on_bad_lines='warn', delimiter=';')
    existing_columns_to_delete = [col for col in columns_to_delete if col in df.columns]
    df.drop(columns=existing_columns_to_delete, inplace=True)
    df_list.append(df)

# Concatenate the DataFrames into a single DataFrame
df_artfacts_raw = pd.concat(df_list, ignore_index=True)
#%%
display(HTML(df_artfacts_raw.head(50).to_html(classes='table table-striped', max_rows=50, max_cols=50, notebook=True)))
#%%
# Export the DataFrame to a CSV file on the desktop
output_file_path = '/Users/jac/Desktop/scrape_arch_artfatcs_raw_50.csv'
df_artfacts_raw.to_csv(output_file_path, index=False)
#%%
# Calculate the number of rows in the concatenated DataFrame
num_rows = df_artfacts_raw.shape[0]
num_unique_ids = df_artfacts_raw['id'].nunique()

# Calculate the number and percentage of NaN values for each column
nan_counts = df_artfacts_raw.isna().sum()
nan_percentage = (nan_counts / num_rows) * 100

# Create a DataFrame for NaN counts and percentages
nan_df = pd.DataFrame({
    'Column': df_artfacts_raw.columns,
    'NaN Count': nan_counts,
    'NaN Percentage': nan_percentage
}).reset_index(drop=True)

# Display the results in a scrollable, aesthetically pleasing table
display(HTML(f"""
<div style='max-height: 300px; overflow-y: scroll;'>
    {nan_df.to_html(classes='table table-striped', index=False)}
</div>
"""))

# Print the dataset statistics
print(f"Number of rows in the dataset: {num_rows}")
print(f"Number of unique IDs: {num_unique_ids}")

#%%
# Extract the 'artists' column from df_artfacts_raw
artists_data = df_artfacts_raw['artists'].dropna()

# Initialize a list to store the parsed artist data
parsed_artists = []

# Initialize the index counter
index_counter = 0

# Iterate through each row in the 'artists' column
for artists in artists_data:
    try:
        # Parse the JSON-like structure
        artists_list = ast.literal_eval(artists)
        for artist in artists_list:
            artist['index'] = index_counter
            parsed_artists.append(artist)
        index_counter += 1
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing JSON: {e}")

# Create a new DataFrame from the parsed artist data
df_artists = pd.DataFrame(parsed_artists)

# Display the head of the new DataFrame in a scrollable, aesthetically pleasing table
display(HTML(df_artists.head().to_html(classes='table table-striped', max_rows=10, max_cols=10, notebook=True)))

# Save the new DataFrame to a CSV file on the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'parsed_artists.csv')
df_artists.to_csv(desktop_path, index=False)

print(f"Parsed artists DataFrame saved to: {desktop_path}")
#%%
# Display the first 20 rows of df_artfacts_raw in a scrollable, aesthetically pleasing table with all columns visible
display(HTML(df_artfacts_raw.head(20).to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))

# Display the first 20 rows of df_artists in a scrollable, aesthetically pleasing table with all columns visible
display(HTML(df_artists.head(20).to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))
# Print the number of unique ids in df_artists
unique_ids_artists = df_artists['id'].nunique()
print(f"Number of unique ids in df_artists: {unique_ids_artists}")

#%%
# Extract the column names of df_artfacts_raw and df_biennale_artists
columns_artfacts_raw = pd.DataFrame(df_artfacts_raw.columns, columns=['df_artfacts_raw Columns'])
columns_biennale_artists = pd.DataFrame(df_biennale_artists.columns, columns=['df_biennale_artists Columns'])
columns_artists = pd.DataFrame(df_artists.columns, columns=['df_artists Columns'])

# Display the column names in a scrollable, aesthetically pleasing table
display(HTML(columns_artfacts_raw.to_html(classes='table table-striped', max_rows=50, max_cols=50, notebook=True)))
display(HTML(columns_biennale_artists.to_html(classes='table table-striped', max_rows=50, max_cols=50, notebook=True)))
display(HTML(columns_artists.to_html(classes='table table-striped', max_rows=50, max_cols=50, notebook=True)))
#%%
# Display the head of df_artists in a scrollable, aesthetically pleasing table
display(HTML(df_artists.head(20).to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))

# Display the head of df_biennale_artists in a scrollable, aesthetically pleasing table
display(HTML(df_biennale_artists.head(20).to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))
#%% 2024 DATA WONT HAVE THE INDEX NUMBER!!!
#%%
# Convert the 'id' columns in both DataFrames to string
df_artists['id'] = df_artists['id'].astype(str)
df_biennale_artists['id'] = df_biennale_artists['id'].astype(str)

# Merge df_biennale_artists into df_artists on the 'id' column
df_artists_complete = df_artists.copy()

for column in df_biennale_artists.columns:
    if column in df_artists.columns:
        df_artists_complete[column] = df_biennale_artists[column]
    else:
        df_artists_complete[column] = df_biennale_artists[column]

# Display the first 20 rows of the merged DataFrame in a scrollable, aesthetically pleasing table
display(HTML(df_artists_complete.head(20).to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))

# Check unique IDs in df_artists and df_biennale_artists before merging
unique_ids_artists = df_artists['id'].nunique()
unique_ids_biennale_artists = df_biennale_artists['id'].nunique()

print(f"Unique IDs in df_artists before merging: {unique_ids_artists}")
print(f"Unique IDs in df_biennale_artists before merging: {unique_ids_biennale_artists}")

# Calculate the number of unique 'id' values in df_artists
unique_artist_ids = df_artists_complete['id'].nunique()
print(f"Number of unique artists in df_artists: {unique_artist_ids}")
#%%


# 1. merge 571 with the 15'000 in Dropbox
# 2. check the id with artfacts raw
#PROBLEM IN MERGIN WITH ID!! DF_ARTISTS_COMPLET EONLY 571 ROWS









# %%
# Calculate the number of unique 'id' values in df_artists
unique_artist_ids = df_artists['id'].nunique()
print(f"Number of unique artists in df_artists: {unique_artist_ids}")
# %%
# Identify the 'id' values in df_artists that have duplicates
duplicate_ids = df_artists['id'].value_counts()
duplicate_ids = duplicate_ids[duplicate_ids > 1]

# Create a list with the 'id' values and the number of times they are duplicated
duplicate_list = duplicate_ids.reset_index().values.tolist()

# Print the list
print("List of 'id' values with duplicates and their counts:")
for item in duplicate_list:
    print(f"ID: {item[0]}, Count: {item[1]}")
# %%
# Match the two DataFrames through the 'index' column and copy 'institution_id' values
df_artists = df_artists.merge(df_artfacts_raw[['index', 'institution_id']], on='index', how='left', suffixes=('', '_raw'))

# Display the first 20 rows of df_artists in a scrollable, aesthetically pleasing table
display(HTML(df_artists.head(20).to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))

# %%
# Calculate the number and percentage of NaN values in the 'institution_id' column of df_artists
nan_counts_institution_id = df_artists['institution_id'].isna().sum()
nan_percentage_institution_id = (nan_counts_institution_id / df_artists.shape[0]) * 100

# Print the results
print(f"Number of NaN values in 'institution_id' column of df_artists: {nan_counts_institution_id}")
print(f"Percentage of NaN values in 'institution_id' column of df_artists: {nan_percentage_institution_id:.2f}%")
# %%
# Condense duplicates based on 'index'
df_artists_condensed = df_artists.groupby('index').agg({
    'id': 'first',
    'institution_id': lambda x: x.nunique(),
    'name': 'first',
    'first_name': 'first',
    'last_name': 'first',
    'links': 'first',
    'birth_year': 'first',
    'nationality': 'first',
    'ranking': 'first',
    'institution_id': lambda x: list(x)
}).reset_index()

# Rename the columns for clarity
df_artists_condensed.rename(columns={'institution_id': 'unique_institution_count', 'institution_id': 'institution_id_list'}, inplace=True)

# Add a column 'institution_id_count' to count the number of items in 'institution_id_list'
df_artists_condensed['institution_id_count'] = df_artists_condensed['institution_id_list'].apply(len)
#%%
# Display the first 20 rows of the condensed DataFrame in a scrollable, aesthetically pleasing table
display(HTML(df_artists_condensed.head(20).to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))
#%%
# Save the condensed DataFrame to a CSV file on the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'condensed_artists.csv')
df_artists_condensed.to_csv(desktop_path, index=False)
print(f"Condensed artists DataFrame saved to: {desktop_path}")

# %%
# Find the highest and lowest values in the 'institution_id_count' column
highest_unique_institution_count = df_artists_condensed['institution_id_count'].max()
lowest_unique_institution_count = df_artists_condensed['institution_id_count'].min()

# Print the results
print(f"Highest unique_institution_count: {highest_unique_institution_count}")
print(f"Lowest unique_institution_count: {lowest_unique_institution_count}")
# %%
# Sort df_artists_condensed by 'unique_institution_count' in descending order
df_top_10_unique_institution_count = df_artists_condensed.sort_values(by='institution_id_count', ascending=False).head(100)

# Display the top 10 rows in a scrollable, aesthetically pleasing table
display(HTML(df_top_10_unique_institution_count.to_html(classes='table table-striped', max_rows=100, max_cols=None, notebook=True)))
# %%
# FILTERING DF_ARTISTS_CONDENSED BY WITH DF_BIO (BIENNALE)
csv_path_bio = "/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/produced_data_biennale_artists_bio_GS_1_0.csv"
df_bio = pd.read_csv(csv_path_bio)

# Display the top 10 rows in a scrollable, aesthetically pleasing table
display(HTML(df_bio.to_html(classes='table table-striped', max_rows=20, max_cols=None, notebook=True)))# %%

# Print the number of rows in df_bio
num_rows = df_bio.shape[0]
print(f"Number of rows in df_artists_complete: {num_rows}")

# Print the number of unique person_name in df_artists_complete
unique_person_names = df_bio['person_name'].nunique()
print(f"Number of unique person_name in df_artists_complete: {unique_person_names}")

# Print the number of unique person_id in df_artists_complete
unique_person_ids = df_bio['person_id'].nunique()
print(f"Number of unique person_id in df_artists_complete: {unique_person_ids}")

# %%
# Find the number of matching names between df_bio and df_artists_condensed
matching_names = df_bio['person_name'].isin(df_artists_condensed['name']).sum()

# Calculate the percentage of matching names
total_names = df_bio['person_name'].nunique()
percentage_matching = (matching_names / total_names) * 100

# Print the results
print(f"Number of matching names: {matching_names}")
print(f"Percentage of matching names: {percentage_matching:.2f}%")
#%%
# Find the number of matching names between df_bio and df_artists_condensed using fuzzy matching (# GIVE IT A SCORE IF IT IS A BIT DIFFERENT -- TRESHOLD ACCEPTANCE)
matching_names = 0
for name in df_bio['person_name']:
    if any(fuzz.ratio(name, artist_name) > 95 for artist_name in df_artists_condensed['name']):
        matching_names += 1

# Calculate the percentage of matching names
total_names = df_bio['person_name'].nunique()
percentage_matching = (matching_names / total_names) * 100

# Print the results
print(f"Number of matching names: {matching_names}")
print(f"Percentage of matching names: {percentage_matching:.2f}%")
# %%
# Number of rows in df_artists_condensed
num_rows_artists_condensed = df_artists_condensed.shape[0]

# Number of rows in df_bio
num_rows_bio = df_bio.shape[0]

# Print the results
print(f"Number of rows in df_artists_condensed: {num_rows_artists_condensed}")
print(f"Number of rows in df_bio: {num_rows_bio}")
# %%
df_artists_condensed.head(50)
# %%
# List of unique IDs in df_artists_condensed
unique_ids_artists_condensed = df_artists_condensed['id'].unique()
len(unique_ids_artists_condensed) 
# Print the results
print(f"List of unique IDs in df_artists_condensed: {unique_ids_artists_condensed}")
print(len(unique_ids_artists_condensed))




# %%
# 1. info_all+2024
# 2. clean url > id
# 3. filter df_artist_condensed with artists in info_all+2024
# %%
# Viz: Gpehi, Kepler, NetworkX, Cosmo