import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# API endpoint and authorization
url = "https://api.mobilitytwin.brussels/stib/shapefile"
api_key = "YOUR_API_KEY"  # Replace this with your actual API key

# Fetch data from the API
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})

# Check if the request was successful
if response.status_code == 200:
    # Convert JSON data to a GeoDataFrame
    data = response.json()
    gdf = gpd.GeoDataFrame.from_features(data["features"])

    # Save to ODS file
    output_file = "/mnt/data/mobility_data.ods"
    df = pd.DataFrame(gdf.drop(columns='geometry'))  # Drop geometry column to save as a table
    df.to_excel(output_file, engine='odf', index=False)
    print(f"Data saved to {output_file}")

    # Plot the data using GeoPandas
    plt.figure(figsize=(10, 10))
    gdf.plot(edgecolor='k', color='cyan', alpha=0.7)
    plt.title("Brussels Mobility Twin - STIB Data Visualization")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    print(response.text)
