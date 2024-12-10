
import pandas as pd
import math
from scipy.stats import t

# ODS file
file_path = "../refineData/POI_BusStops_Proximity_with_Rank.ods"  # Replace with your actual ODS file path
sheet_name = "Sheet1"

data = pd.read_excel(file_path, sheet_name=sheet_name, engine='odf')

# Extract the columns
col1 = data['Bus Stop Count']
col2 = data['Popularity Rank']

# Rank the data
rank_col1 = col1.rank(method="average")
rank_col2 = col2.rank(method="average")

# Differences in ranks
rank_diff = rank_col1 - rank_col2

# Correlation
num_var = len(col1)
spearman_corr = 1 - (6 * sum(rank_diff**2)) / (num_var * (num_var ** 2 - 1))

# T-statistic for correlation
t_statistic = spearman_corr * math.sqrt((num_var - 2) / (1 - spearman_corr ** 2))

# P-value
df = num_var - 2
p_value = 2 * (1 - t.cdf(abs(t_statistic), df))

# Results
print(f"Spearman Correlation: {spearman_corr}")
print(f"P-Value: {p_value}")


