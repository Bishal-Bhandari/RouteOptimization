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

# Add the rank columns to the DataFrame
data['Rank_Density'] = rank_col1
data['Rank_Line_Count'] = rank_col2
data['Rank_Difference'] = d

# Save the DataFrame to a new ODS file
output_file_path = "refineData/BackUP/output_with_ranks.ods"  # Replace with desired output file path
data.to_excel(output_file_path, index=False, engine='odf')

# Plotting the ranked data
plt.figure(figsize=(10, 6))

# Scatter plot of ranked data
sns.regplot(x=data['Rank_Density'], y=data['Rank_Line_Count'], scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})

# Add title and labels
plt.title(f'Spearman Correlation: {spearman_corr:.2f}\nP-Value: {p_value:.2e}', fontsize=16)
plt.xlabel('Ranked Density')
plt.ylabel('Ranked Line Count')

# Show the plot
plt.show()
