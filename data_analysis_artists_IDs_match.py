#%%
import pandas as pd

#%%
df = pd.read_csv('artists_years_removed.csv')
df_bio = pd.read_csv('scrape_arch_biennale_artists_bio.csv')

#%%

# Create a dictionary from df_bio for quick lookup
bio_dict = dict(zip(df_bio['person_name'], df_bio['person_id']))

# Create a new column 'merged_id' in df
df['merged_id'] = df['Artist_name'].map(bio_dict)

# Save the updated dataframe to a new CSV file
df.to_csv('artists_with_merged_ids.csv', index=False)
# ...existing code...
# %%
# Calculate the number and percentage of unsuccessful matches
unsuccessful_matches = df['merged_id'].isna().sum()
total_matches = len(df)
percentage_unsuccessful = (unsuccessful_matches / total_matches) * 100

print(f"Number of unsuccessful matches: {unsuccessful_matches}")
print(f"Percentage of unsuccessful matches: {percentage_unsuccessful:.2f}%")
# %%
