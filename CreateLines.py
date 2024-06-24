import folium
import pandas as pd
from collections import Counter
import json

# Define a function to read addresses and coordinates from an Excel file
def read_addresses_from_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

# Function to count repeated addresses
def count_repeated_addresses(address_list):
    address_counter = Counter(address_list)
    return address_counter

# Load JSON data from a file
with open('Data/GeoLocation.json', 'r') as json_file:
    address_data = json.load(json_file)

# Function to retrieve latitude and longitude
def get_lat_lon(start_address, address_data):
    if start_address in address_data:
        lat_lon = address_data[start_address]
        return lat_lon['Latitude'], lat_lon['Longitude']
    else:
        return "Address not found", "Address not found"


# Read addresses and coordinates from the Excel file
##############################################
#  Document with locations to display on map #
##############################################

file_path = 'RouteVisualizationData.xlsx'
df = read_addresses_from_excel(file_path)

from_addresses = df.iloc[:, 0]
first_column_list = from_addresses.tolist()

address_counts = count_repeated_addresses(first_column_list)



for address, count in address_counts.items():
    print(f"Address: {address}, Count: {count}")

# Create a map centered on the Netherlands
m = folium.Map(location=[52.1, 5.3], zoom_start=8)

# Iterate through each row in the DataFrame and plot trips
for index, row in df.iterrows():
    start_address = row['Start Address']
    end_address = row['End Address']

    start_lat, start_lon = get_lat_lon(start_address, address_data)    
    end_lat, end_lon = get_lat_lon(end_address, address_data)   

    # Add markers for start and end locations
    folium.Marker(
        location=[start_lat, start_lon],
        popup=start_address,
        icon=folium.Icon(color='green')
    ).add_to(m)

    folium.Marker(
        location=[end_lat, end_lon],
        popup=end_address,
        icon=folium.Icon(color='red')

    ).add_to(m)

    # Add a line connecting start and end locations
    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        opacity = 0.7,
        weight = 3,
        color='blue'
    ).add_to(m)

# Save the map to an HTML file
m.save("map.html")