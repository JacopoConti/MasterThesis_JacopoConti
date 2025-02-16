#%%
import pandas as pd
from IPython.display import display, HTML

#%%
# Load the CSV file into a DataFrame
file_path = 'produced_data_artfacts_VB_artists_exhibition_record_info.csv'
df = pd.read_csv(file_path)

#%%
# Display the first few rows of the DataFrame in a scrollable table
html = df.head(100).to_html(classes='table table-striped', max_rows=10, max_cols=10, index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html}</div>'))

#%%
# Filter the DataFrame for specific exhibition_id values
filtered_df = df[df['exhibition_id'].isin([11934, 303196, 134486, 714957, 714941])]

#%%
# Display the filtered DataFrame in a scrollable table
html = filtered_df.to_html(classes='table table-striped', index=False)
display(HTML(f'<div style="max-height: 400px; overflow-y: scroll;">{html}</div>'))
# %%