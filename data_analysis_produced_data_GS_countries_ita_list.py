#%%
import pandas as pd

#%%
# Import the CSV file
csv_path = "produced_data_GS_countries_ita_list.csv"
df_produced_data_GS_countries_ita_list = pd.read_csv(csv_path)

# Print the first row
print(df_produced_data_GS_countries_ita_list.head(10))

#%%
# Produce a new list with only the third column
third_column_list = df_produced_data_GS_countries_ita_list.iloc[:, 2].tolist()

# Print the new list
print(third_column_list)
# %%
