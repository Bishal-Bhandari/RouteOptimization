import numpy as np
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

m.drawcoastlines()
m.drawcountries()

# Scatter plot for latitude and longitude with different colors
colors = plt.cm.rainbow(np.linspace(0, 1, len(df)))
for i, (lat, lon) in enumerate(zip(df['latitude'], df['longitude'])):
    x, y = m(lon, lat)
    m.plot(x, y, 'o', markersize=5, color=colors[i])

plt.show()
