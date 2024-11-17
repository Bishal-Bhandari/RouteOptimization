import pandas as pd
import math
from scipy.stats import t

# Load the ODS file and specify the sheet name
file_path = "refineData/final_correlation_matched_output.ods"  # Replace with your actual ODS file path
sheet_name = "Sheet1"        # Replace with the correct sheet name


# Read the ODS file
data = pd.read_excel(file_path, sheet_name=sheet_name, engine='odf')

# Extract the two columns
col1 = data['Density']
col2 = data['Line_Count']

# Rank the data
rank_col1 = col1.rank(method="average")
rank_col2 = col2.rank(method="average")

# Calculate the differences in ranks
d = rank_col1 - rank_col2

# Compute Spearman's rank correlation coefficient
n = len(col1)
spearman_corr = 1 - (6 * sum(d**2)) / (n * (n**2 - 1))

# Calculate the t-statistic for Spearman correlation
t_statistic = spearman_corr * math.sqrt((n - 2) / (1 - spearman_corr**2))

# Calculate the p-value using the t-distribution (two-tailed test)
df = n - 2  # degrees of freedom
p_value = 2 * (1 - t.cdf(abs(t_statistic), df))

# Display the results
print(f"Spearman Correlation: {spearman_corr}")
print(f"P-Value: {p_value}")
