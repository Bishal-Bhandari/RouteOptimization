import numpy as np
import pandas as pd
import math
from scipy.stats import t
import matplotlib.pyplot as plt
import seaborn as sns

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
rank_diff = rank_col1 - rank_col2

# Compute Spearman's rank correlation coefficient
num_var = len(col1)
spearman_corr = 1 - (6 * sum(rank_diff**2)) / (num_var * (num_var ** 2 - 1))

# Calculate the t-statistic for Spearman correlation
t_statistic = spearman_corr * math.sqrt((num_var - 2) / (1 - spearman_corr ** 2))

# Calculate the p-value using the t-distribution (two-tailed test)
df = num_var - 2  # degrees of freedom
p_value = 2 * (1 - t.cdf(abs(t_statistic), df))

# Display the results
print(f"Spearman Correlation: {spearman_corr}")
print(f"P-Value: {p_value}")

# Add the rank columns to the DataFrame
data['Rank_Density'] = rank_col1
data['Rank_Line_Count'] = rank_col2
data['Rank_Difference'] = rank_diff

# Save the DataFrame to a new ODS file
output_file_path = "refineData/BackUP/output_with_ranks.ods"  # Replace with desired output file path
data.to_excel(output_file_path, index=False, engine='odf')

# Scatter plot to show the relationship between ranks
plt.figure(figsize=(8, 6))
sns.scatterplot(x=rank_col1, y=rank_col2)

# Adding labels and title
plt.title('Ranked Data (Density vs Line Count)', fontsize=16)
plt.xlabel('Rank of Density')
plt.ylabel('Rank of Line Count')

# Optionally, you can add a line for the correlation (Spearman's rank) using np.polyfit
slope, intercept = np.polyfit(rank_col1, rank_col2, 1)
plt.plot(rank_col1, slope*rank_col1 + intercept, color='red', linestyle='--', label='Spearman correlation line')

plt.legend()
plt.show()

