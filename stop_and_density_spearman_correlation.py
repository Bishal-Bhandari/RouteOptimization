import pandas as pd

# Read the ODS file into a DataFrame
input_file = "refineData/final_busStop_density.ods"
output_file = "refineData/spearman_unique_stopName_Density"

# Load the data from ODS
df = pd.read_excel(input_file, engine="odf")  # Use 'engine="odf"' for ODS files

# Remove duplicate names in the 'stop' column, keeping the first occurrence
unique_stops_df = df.drop_duplicates(subset=["Stop name"], keep="first")

# Save the filtered data to a new ODS file
unique_stops_df.to_excel(output_file, engine="odf", index=False)

print(f"Filtered data saved to {output_file}")
