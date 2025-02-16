
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
# Display the tables in an aesthetically scrollable way
display(HTML("<h2>df_cleaned:</h2>"))
display(HTML(df_cleaned.to_html(classes='table table-striped', max_rows=10, max_cols=10)))

display(HTML("<h2>df_bio_GS:</h2>"))
display(HTML(df_bio_GS.to_html(classes='table table-striped', max_rows=10, max_cols=10)))

#%%
# Unique names of the 2 dataframes
unique_person_names = df_bio_GS['person_name'].nunique()
unique_person_id_count = df_bio_GS['person_id'].nunique()
unique_artist_names = df_cleaned['Artist_name'].nunique()

print(f"Unique person_name in df_bio_GS: {unique_person_names}")
print(f"Unique person_id in df_bio_GS: {unique_person_id_count}")
print(f"Unique Artist_name in df_cleaned: {unique_artist_names}")

#%%
# NaN for each column of df_bio_GS
nan_counts = df_bio_GS.isna().sum()
print(nan_counts)

#%% Count of Artists by Years
year_counts = df_cleaned['Year'].value_counts().sort_index()
print(year_counts)
# %%
# Calculate the average number of artists per year [582.30]
average_artists_per_year = df_cleaned.groupby('Year')['Artist_name'].nunique().mean()
print(f"Average number of artists per year: {average_artists_per_year:.2f}")


#%%

# Step 1: Create a new column 'GS' in df_cleaned
df_cleaned['GS'] = pd.NA

# Step 2: Create a mapping from 'person_name' to 'artist_birthplace_country_GS' in df_bio_GS
birthplace_mapping = dict(zip(df_bio_GS['person_name'], df_bio_GS['artist_birthplace_country_GS']))

# Step 3: Populate the 'GS' column in df_cleaned using the mapping
df_cleaned['GS'] = df_cleaned['Artist_name'].map(birthplace_mapping)

# Step 4: Calculate number and percentage of unsuccessful matches
unsuccessful_matches = df_cleaned['GS'].isna().sum()
total_records = len(df_cleaned)
percentage_unsuccessful = (unsuccessful_matches / total_records) * 100

print(f"Number of unsuccessful matches: {unsuccessful_matches}")
print(f"Percentage of unsuccessful matches: {percentage_unsuccessful:.2f}%")

# Step 5: Display df_cleaned in a scrollable table
display(HTML(df_cleaned.to_html(classes='table table-striped', max_rows=10, max_cols=10, notebook=True)))


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

# Get desktop path for macOS
desktop_path = os.path.expanduser("~/Desktop")
svg_path = os.path.join(desktop_path, "artists_count_by_year_GS_status.svg")

# Save the plot as an SVG file
plt.savefig(svg_path, format='svg')

# Display the plot
plt.show()

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

# Get desktop path for macOS
desktop_path = os.path.expanduser("~/Desktop")
svg_path = os.path.join(desktop_path, "artists_count_by_year_.svg")

# Save the plot as an SVG file
plt.savefig(svg_path, format='svg')

# Display the plot
plt.show()

#%%
# Group by Year and GS, then pivot into separate columns
df_stacked = df_cleaned_GS.groupby(['Year', 'GS']).size().unstack(fill_value=0)

# Create a stacked bar plot
plt.figure(figsize=(16, 6), dpi=300)
df_stacked.plot(kind='bar', stacked=True, ax=plt.gca(), color=['lightgrey', '#B2C6B8'])

plt.xlabel('Year', fontsize=14, labelpad=20)
plt.ylabel('Count', fontsize=14, labelpad=20)
plt.title('Count of Artists by Year (Stacked by GS status)', fontsize=16, pad=30)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add a legend
plt.legend(title='GS', labels=['Not GS (0)', 'GS (1)'])

# Adjust layout
plt.tight_layout()

# Get desktop path for macOS
desktop_path = os.path.expanduser("~/Desktop")
svg_path = os.path.join(desktop_path, "artists_count_by_year_GS_status_V2.svg")

# Save the plot as an SVG file
plt.savefig(svg_path, format='svg')

# Display the plot
plt.show()

print(f"SVG file saved to: {svg_path}")
# %%
# Print the total number of rows in df_cleaned_GS
print(f"Total number of rows in df_cleaned_GS: {len(df_cleaned_GS)}")

# Print how many NaN values each column has
print("NaN values per column in df_cleaned_GS:")
print(df_cleaned_GS.isna().sum())

# Print how many unique Artist_name there are
unique_artist_name_count = df_cleaned_GS['Artist_name'].nunique()
print(f"Number of unique 'Artist_name': {unique_artist_name_count}")


#%%
# RISULTATI 102 SONO SPREAD OVER THE YEARS = ACCEPTABLES
# Count of Artists by Years for df_cleaned
year_counts = df_cleaned['Year'].value_counts().sort_index()

# Filter out rows with NaN values in the 'GS' column of df_cleaned_GS
df_cleaned_GS_filtered = df_cleaned_GS.dropna(subset=['GS'])
year_counts_GS = df_cleaned_GS_filtered['Year'].value_counts().sort_index()

# Create DataFrames for comparison
df_year_counts = year_counts.to_frame(name='df_cleaned')
df_year_counts_GS = year_counts_GS.to_frame(name='df_cleaned_GS')

# Highlight differences
def highlight_diff(s):
    return ['background-color: yellow' if s.name in df_year_counts.index and s['df_cleaned_GS'] != df_year_counts.loc[s.name, 'df_cleaned'] else '' for v in s]

styled_year_counts_GS = df_year_counts_GS.style.apply(highlight_diff, axis=1)

# Display the results in two tables side by side
html_year_counts = df_year_counts.to_html(classes='table table-striped')
html_year_counts_GS = styled_year_counts_GS.to_html()

display(HTML(f"""
<div style='display: flex;'>
    <div style='flex: 1;'>
        <h2>Count of Artists by Years in df_cleaned</h2>
        <div style='margin-top: 10px;'>{html_year_counts}</div>
    </div>
    <div style='flex: 1;'>
        <h2>Count of Artists by Years in df_cleaned_GS</h2>
        <div style='margin-top: 10px;'>{html_year_counts_GS}</div>
    </div>
</div>
"""))

# %%

# Count of Artists by Years for df_cleaned
year_counts = df_cleaned['Year'].value_counts().sort_index()

# Filter out rows with NaN values in the 'GS' column of df_cleaned_GS
df_cleaned_GS_filtered = df_cleaned_GS.dropna(subset=['GS'])
year_counts_GS = df_cleaned_GS_filtered['Year'].value_counts().sort_index()

# Create DataFrames for comparison
df_year_counts = year_counts.to_frame(name='df_cleaned')
df_year_counts_GS = year_counts_GS.to_frame(name='df_cleaned_GS')

# Highlight differences
def highlight_diff(s):
    return ['background-color: yellow' if s.name in df_year_counts.index and s['df_cleaned_GS'] != df_year_counts.loc[s.name, 'df_cleaned'] else '' for v in s]

styled_year_counts_GS = df_year_counts_GS.style.apply(highlight_diff, axis=1)

# Display the results in two tables side by side
html_year_counts = df_year_counts.to_html(classes='table table-striped')
html_year_counts_GS = styled_year_counts_GS.to_html()

display(HTML(f"""
<div style='display: flex;'>
    <div style='flex: 1;'>
        <h2>Count of Artists by Years in df_cleaned</h2>
        <div style='margin-top: 10px;'>{html_year_counts}</div>
    </div>
    <div style='flex: 1;'>
        <h2>Count of Artists by Years in df_cleaned_GS</h2>
        <div style='margin-top: 10px;'>{html_year_counts_GS}</div>
    </div>
</div>
"""))

# Verify the total count of artists per year
df_total_artists = df_cleaned_GS.groupby('Year').size()
html_total_artists = df_total_artists.to_frame().to_html()

# Group by Year and GS, then pivot into separate columns
df_stacked = df_cleaned_GS.groupby(['Year', 'GS']).size().unstack(fill_value=0)
html_stacked_counts = df_stacked.to_html()

# Display the results in two tables side by side
display(HTML(f"""
<div style='display: flex;'>
    <div style='flex: 1;'>
        <h2>Total count of artists per year</h2>
        <div style='max-height: 200px; overflow-y: scroll;'>{html_total_artists}</div>
    </div>
    <div style='flex: 1;'>
        <h2>Stacked counts by Year and GS</h2>
        <div style='max-height: 200px; overflow-y: scroll;'>{html_stacked_counts}</div>
    </div>
</div>
"""))
