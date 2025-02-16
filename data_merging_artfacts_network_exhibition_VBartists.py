
# %%
import pandas as pd
from IPython.display import display, HTML
from tqdm import tqdm
#%%
# Import the first CSV file
file_1 = 'produced_data_artfacts_year_vs_artist_id_match_complete.csv'
df_year_VBartistid_VBsids = pd.read_csv(file_1)

# Import the second CSV file
file_2 = 'produced_data_artfacts_network_exhibition_VBartists.csv'
df_exhid_VBartistid = pd.read_csv(file_2)

#%%
rows_df_year_VBartistid_VBsids = len(df_year_VBartistid_VBsids)
rows_df_exhid_VBartistid = len(df_exhid_VBartistid)
print(f"df_year_VBartistid_VBsids_html has {rows_df_year_VBartistid_VBsids} rows.")
print(f"df_exhid_VBartistid_html has {rows_df_exhid_VBartistid} rows.")

#%%

# Display the first 100 rows of the first DataFrame in a scrollable table
df_year_html = df_year_VBartistid_VBsids.head(1000).to_html(classes='table table-striped', index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{df_year_html}</div>'))

# Display the first 100 rows of the second DataFrame in a scrollable table
df_exhid_html = df_exhid_VBartistid.head(100).to_html(classes='table table-striped', index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{df_exhid_html}</div>'))
# %%
# Create a new DataFrame named df_exid_artistid
df_exid_artistid = pd.DataFrame()

# Populate the 'exhibition_id' column with data from df_exhid_VBartistid
df_exid_artistid['exhibition_id'] = df_exhid_VBartistid['exhibition_id']

# Populate the 'artist_id' column with data from df_year_VBartistid_VBsids
df_exid_artistid['artist_id'] = df_year_VBartistid_VBsids['artist_id']

# Display the first few rows of the new DataFrame
df_exid_artistid_html = df_exid_artistid.head(100).to_html(classes='table table-striped', index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{df_exid_artistid_html}</div>'))
# %%
# Calculate the number of rows in the new dataset
num_rows_df_exid_artistid = len(df_exid_artistid)
print(f"Number of rows in df_exid_artistid: {num_rows_df_exid_artistid}")
# %%

#EXAMPLE
# Estrarre una lista di tutti gli exhibition_id dove artist_id = 249848
exhibition_ids = df_year_VBartistid_VBsids[df_year_VBartistid_VBsids['artist_id'] == 249848]['exhibition_id'].tolist()
print(f"Exhibition IDs for artist_id 249848: {exhibition_ids}")

exhibition_ids = df_year_VBartistid_VBsids[df_year_VBartistid_VBsids['artist_id'] == 40878]['exhibition_id'].tolist()
print(f"Exhibition IDs for artist_id 249848: {exhibition_ids}")
# %%
# MERGING THE 2 DATASETS

# 1. Create a new DataFrame as a copy of df_exhid_VBartistid
df_network_coplete = df_exhid_VBartistid.copy()

# 2. Append all rows from df_year_VBartistid_VBsids to this new DataFrame
df_network_coplete = pd.concat([df_network_coplete, df_year_VBartistid_VBsids], ignore_index=True)

# 3. Drop the 'year' column
df_network_coplete.drop(columns='year', inplace=True, errors='ignore')

# 4. Remove duplicate rows based on both 'exhibition_id' and 'artist_id' together
df_network_coplete.drop_duplicates(subset=['exhibition_id', 'artist_id'], inplace=True)

# 5. Ensure all numerical values do not display '.0' by converting them to plain integers (where possible)
for col in ['exhibition_id', 'artist_id']:
    # Convert to float first (if possible), then to int, then back to string
    df_network_coplete[col] = (
        df_network_coplete[col]
        .apply(lambda x: str(int(float(x))) if pd.notnull(x) and str(x).replace('.', '', 1).isdigit() else x)
    )

#%%
# Calculate the number of rows in the new dataset
num_rows_df_network_coplete = len(df_network_coplete)
print(f"Number of rows in df_network_coplete: {num_rows_df_network_coplete}")
# %%
# Export this DataFrame to a CSV file on the desktop
output_file_path = '/Users/jac/Desktop/produced_data_artfacts_network_exhibition_VBartists_complete.csv'
df_network_coplete.to_csv(output_file_path, index=False)
print(f"Exported df_network_coplete to {output_file_path}")


#%%



# Enable the tqdm pandas integration
tqdm.pandas()

# 1) We already have df_network_coplete with columns: exhibition_id, artist_id
#    Each row indicates that the given exhibition_id has the given artist_id.
#    We want to build a network of exhibitions where edges represent
#    how many artists the two exhibitions share.

# ------------------------------------------------------------------------------
# Merge df_network_coplete with itself on artist_id to get pairs of exhibitions
# Filter only pairs with exhibition_id_x < exhibition_id_y to avoid duplicates
# Then count how many artists each pair shares (groupby + progress_apply).
# Rename columns to (source, target, weight) for Gephi.
# ------------------------------------------------------------------------------

# Merge on artist_id
df_temp = (
    df_network_coplete[['exhibition_id', 'artist_id']]
    .merge(
        df_network_coplete[['exhibition_id', 'artist_id']],
        on='artist_id',
        suffixes=('_x', '_y')
    )
    .query('exhibition_id_x < exhibition_id_y')
)

# Group and count with a tqdm progress bar
df_cooccurrence = (
    df_temp
    .groupby(['exhibition_id_x', 'exhibition_id_y'])['artist_id']
    .progress_apply(len)   # Count how many artists a pair shares
    .reset_index(name='weight')
    .rename(columns={'exhibition_id_x': 'source', 'exhibition_id_y': 'target'})
)

# ------------------------------------------------------------------------------
# (Optional) Convert source and target to strings without trailing ".0" if needed
# ------------------------------------------------------------------------------
for col in ['source', 'target']:
    df_cooccurrence[col] = (
        df_cooccurrence[col]
        .apply(lambda x: str(int(float(x))) if pd.notnull(x) and str(x).replace('.', '', 1).isdigit() else x)
    )

# ------------------------------------------------------------------------------
# Inspect results
# ------------------------------------------------------------------------------
df_cooccurrence_html = df_cooccurrence.head(50).to_html(classes='table table-striped', index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{df_cooccurrence_html}</div>'))

# ------------------------------------------------------------------------------
# Export to CSV for Gephi
# ------------------------------------------------------------------------------
gephi_file_path = '/Users/jac/Desktop/produced_data_artfacts_network_exhibition_VBartists_for_gephi_by_exhibition.csv'
df_cooccurrence.to_csv(gephi_file_path, index=False)
print(f"Exported co-occurrence edge list with progress to {gephi_file_path}")
# %%

# Calculate the number of rows in the new dataset
num_rows_df_cooccurrence = len(df_cooccurrence)
print(f"Number of rows in df_network_coplete: {num_rows_df_cooccurrence}")
# %%
df_cooccurrence_html = df_cooccurrence.head(5000).to_html(classes='table table-striped', index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{df_cooccurrence_html}</div>'))
# %%
# Sort by weight in descending order and get the top 100
top_100 = df_cooccurrence.sort_values(by='weight', ascending=False).head(100)
# Optionally, display in a scrollable table
top_100_html = top_100.to_html(classes='table table-striped', index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{top_100_html}</div>'))
# %%
# Count the number of rows where weight is equal to 1
num_rows_weight_1 = df_cooccurrence[df_cooccurrence['weight'] == 1].shape[0]

print(f"Number of rows with weight = 1: {num_rows_weight_1}")

#%%

# Count the number of rows where weight is lower or equal to 5
num_rows_weight_le_5 = df_cooccurrence[df_cooccurrence['weight'] <= 5].shape[0]

print(f"Number of rows with weight <= 5: {num_rows_weight_le_5}")

#%%

# Count the number of rows where weight is lower or equal to 10
num_rows_weight_le_10 = df_cooccurrence[df_cooccurrence['weight'] <= 10].shape[0]

print(f"Number of rows with weight <= 10: {num_rows_weight_le_10}")
# %%
# Count the number of unique items in the 'source' column
num_unique_sources = df_cooccurrence['source'].nunique()

# Count the number of unique items in the 'target' column
num_unique_targets = df_cooccurrence['target'].nunique()

print(f"Number of unique items in 'source': {num_unique_sources}")
print(f"Number of unique items in 'target': {num_unique_targets}")
# %%

# EXPORT
# Filter the DataFrame to include only rows where weight > 10
df_cooccurrence_filtered = df_cooccurrence[df_cooccurrence['weight'] > 10]

# Export the filtered DataFrame to a CSV file on the desktop
output_file_path_filtered = '/Users/jac/Desktop/produced_data_artfacts_network_exhibition_VBartists_filtered_10.csv'
df_cooccurrence_filtered.to_csv(output_file_path_filtered, index=False)

print(f"Exported filtered co-occurrence edge list to {output_file_path_filtered}")
# %%
