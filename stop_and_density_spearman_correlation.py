import pandas as pd
from scipy.stats import spearmanr

# Input file path
input_file = "your_input_file.ods"  # Replace with your ODS file name

# Read the data from the ODS file
df = pd.read_excel(input_file, usecols=['A', 'B'], engine="odf")  # Load only columns A and B

# Ensure there are no missing values in the selected columns
df = df.dropna(subset=['A', 'B'])

# Calculate the Spearman correlation
spearman_corr, p_value = spearmanr(df['A'], df['B'])

print(f"Spearman Correlation: {spearman_corr}")
print(f"P-Value: {p_value}")
