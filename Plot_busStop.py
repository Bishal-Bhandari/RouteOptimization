import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# CSV file with latitudes and longitudes
df = pd.read_csv('your_file.csv')  # Adjust to your file path

# For basemap
fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(projection='merc',
            llcrnrlat=df['latitude'].min() - 1, urcrnrlat=df['latitude'].max() + 1,
            llcrnrlon=df['longitude'].min() - 1, urcrnrlon=df['longitude'].max() + 1,
            resolution='i')
