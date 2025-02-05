
# %%
import pandas as pd
from IPython.display import display, HTML
import networkx as nx
import matplotlib.pyplot as plt

#%%
# Define the file paths
csv_path_cleaned = "/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/data_viz_df_cleaned_GS.csv"
csv_path_bio = "/Users/jac/Documents/GitHub/MasterThesis_JacopoConti/produced_data_biennale_artists_bio_GS_1_0.csv"

# Read the CSV files into DataFrames
df_cleaned_GS = pd.read_csv(csv_path_cleaned)
df_cleaned_bio = pd.read_csv(csv_path_bio)

# Display the head of both DataFrames as scrollable tables
display(HTML("<h2>Head of df_cleaned_GS:</h2>"))
display(HTML(df_cleaned_GS.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)))

display(HTML("<h2>Head of df_cleaned_bio:</h2>"))
display(HTML(df_cleaned_bio.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)))


# Add a new column 'birth_country' to df_cleaned_GS
df_cleaned_GS['birth_country'] = None

# Change the column 'person_id' name of df_cleaned_bio to 'id'
df_cleaned_bio.rename(columns={'person_id': 'id'}, inplace=True)

# Merge the two DataFrames on 'id' and update 'birth_country' in df_cleaned_GS
df_cleaned_GS = df_cleaned_GS.merge(df_cleaned_bio[['id', 'birth_country']], on='id', how='left', suffixes=('', '_bio'))

# Update the 'birth_country' column in df_cleaned_GS with the values from 'birth_country_bio'
df_cleaned_GS['birth_country'] = df_cleaned_GS['birth_country_bio']

# Drop the 'birth_country_bio' column
df_cleaned_GS.drop(columns=['birth_country_bio'], inplace=True)

# Display the head of both DataFrames as scrollable tables
display(HTML("<h2>Head of df_cleaned_GS:</h2>"))
display(HTML(df_cleaned_GS.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)))

# %%# Copy df_cleaned_GS and rename the copy to df_cleaned_GS_Birth_country
df_cleaned_GS_Birth_country = df_cleaned_GS.copy()
# Display the head of both DataFrames as scrollable tables
display(HTML("<h2>Head of df_cleaned_GS_Birth_country:</h2>"))
display(HTML(df_cleaned_GS_Birth_country.head().to_html(classes='table table-striped', max_rows=10, max_cols=10)))# %%

# %%
# NODES = BIRTH_COUNTRY
# EDGES = ??
# %%
