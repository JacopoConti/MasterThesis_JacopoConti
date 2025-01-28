
#%%
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
from tabulate import tabulate

#%%
df = pd.read_csv('scraped_data_biennale_maininfo.csv')

# Print unique titles with display
html_table = df.to_html(classes='table table-striped table-hover', max_rows=len(unique_titles), max_cols=10, notebook=True)
scrollable_table = f'<div style="height:400px; width:800px; overflow:auto;">{html_table}</div>'
display(HTML(scrollable_table))

# %%
# List of unique Titles
    # Presidenza done in numbers (filtering)
# Get unique titles
unique_titles = df['Title'].unique()

# Convert to DataFrame for display
unique_titles_df = pd.DataFrame(unique_titles, columns=['Title'])

# Print unique titles with display
html_table = unique_titles_df.to_html(classes='table table-striped table-hover', max_rows=len(unique_titles), max_cols=10, notebook=True)
scrollable_table = f'<div style="height:400px; width:800px; overflow:auto;">{html_table}</div>'
display(HTML(scrollable_table))

# %% # Export dataframe on desktop
# Ensure the DataFrame has two columns
unique_titles_df['Index'] = range(1, len(unique_titles_df) + 1)
unique_titles_df = unique_titles_df[['Index', 'Title']]

# Export the DataFrame to a CSV file on the desktop
unique_titles_df.to_csv('/Users/jac/Desktop/produced_data_biennale_themes_list.csv', index=False)