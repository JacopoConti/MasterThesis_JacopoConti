#%%
import pandas as pd
from IPython.display import display, HTML
from fuzzywuzzy import fuzz
#%%
# Define the file paths
csv_path_rkd_cleaned = "/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/RKD_cleaned.csv"
csv_path_bio = "/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/produced_data_biennale_artists_bio_GS_1_0.csv"

# Read the CSV files into DataFrames
df_rkd_cleaned = pd.read_csv(csv_path_rkd_cleaned)
df_bio = pd.read_csv(csv_path_bio)

# Display the first few rows of each DataFrame
display(HTML("<h2>Head of df_rkd_cleaned:</h2>"))
display(HTML(df_rkd_cleaned.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)))

display(HTML("<h2>Head of df_bio:</h2>"))
display(HTML(df_bio.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)))
# %%
# Add a new column 'VB_name' to df_rkd_cleaned
df_rkd_cleaned['VB_name'] = df_rkd_cleaned['Artist_Name']

# Modify the 'VB_name' by inverting the family name with the names and eliminating the comma
df_rkd_cleaned['VB_name'] = df_rkd_cleaned['VB_name'].apply(lambda x: ' '.join(x.split(', ')[::-1]))

# Display the first few rows of the updated DataFrame
display(HTML("<h2>Head of df_rkd_cleaned with VB_name:</h2>"))
display(HTML(df_rkd_cleaned.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)))
# %%
# Compare the 'VB_name' column of df_rkd_cleaned with 'person_name' of df_bio
matches = df_rkd_cleaned['VB_name'].isin(df_bio['person_name'])

# Calculate the number of matches
num_matches = matches.sum()

# Calculate the percentage of matches
percentage_matches = (num_matches / len(df_rkd_cleaned)) * 100

# Calculate the number of unique names in 'person_name' of df_bio
unique_names = df_bio['person_name'].nunique()

# Calculate the percentage of unique names
percentage_unique_names = (unique_names / len(df_bio)) * 100

# Calculate the number of unsuccessful matches from df_bio
unsuccessful_matches = ~df_bio['person_name'].isin(df_rkd_cleaned['VB_name'])
num_unsuccessful_matches = unsuccessful_matches.sum()

# Calculate the percentage of unsuccessful matches
percentage_unsuccessful_matches = (num_unsuccessful_matches / len(df_bio)) * 100

# Print the results
print(f"Number of matches: {num_matches}")
print(f"Percentage of matches [on len(rkd)]: {percentage_matches:.2f}%")
print(f"Number of unique names in 'person_name' of df_bio: {unique_names}")
print(f"Percentage of unique names in 'person_name' of df_bio: {percentage_unique_names:.2f}%")
print(f"Number of unsuccessful matches in 'person_name' of df_bio: {num_unsuccessful_matches}")
print(f"Percentage of unsuccessful matches in 'person_name' of df_bio: {percentage_unsuccessful_matches:.2f}%")

# %%
# Create a new DataFrame with only the matched rows
df_rkd_cleaned_matches = df_rkd_cleaned[matches]

#%%
# Calculate the number of unique names in 'person_name' of df_bio
unique_names_RKD_matches = df_rkd_cleaned_matches['VB_name'].nunique()
print(unique_names_RKD_matches)
#%%
# Clean the years in the specified columns
columns_to_clean = ['Birthdate', 'Deathdate', 'Start_Date', 'End_Date']
for column in columns_to_clean:
    df_rkd_cleaned_matches[column] = df_rkd_cleaned_matches[column].astype(str).str.split('.').str[0]
#%%
# Save the new DataFrame to a CSV file
output_csv_path = "/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/RKD_cleaned_matches.csv"
df_rkd_cleaned_matches.to_csv(output_csv_path, index=False)

print(f"New CSV file created with matched rows: {output_csv_path}")
# %%
# Find the number of matching names between df_bio and df_artists_condensed using fuzzy matching (# GIVE IT A SCORE IF IT IS A BIT DIFFERENT -- TRESHOLD ACCEPTANCE)
matching_names = 0
for name in df_bio['person_name']:
    if any(fuzz.ratio(name, artist_name) > 95 for artist_name in df_rkd_cleaned['VB_name']):
        matching_names += 1

# Calculate the percentage of matching names
total_names = df_bio['person_name'].nunique()
percentage_matching = (matching_names / total_names) * 100

# Print the results
print(f"Number of matching names: {matching_names}")
print(f"Percentage of matching names: {percentage_matching:.2f}%")
# %%
