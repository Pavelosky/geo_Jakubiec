import folium
import pandas as pd
from collections import Counter
import json
import getGeo

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
        return "EMPTY", "EMPTY"

##############################################
#  Document with locations to display on map #
##############################################

file_path = 'RouteVisualizationData.xlsx'
df = read_addresses_from_excel(file_path)

from_addresses = df.iloc[:, 0]
first_column_list = from_addresses.tolist()

# Initialize an empty set to store unique addresses
new_addresses = set()

#address_counts = count_repeated_addresses(first_column_list)

# for address, count in address_counts.items():
#     print(f"Address: {address}, Count: {count}")

# Create a map centered on the Netherlandsx
m = folium.Map(location=[52.1, 5.3], zoom_start=8)

# Iterate through each row in the DataFrame and plot trips
for index, row in df.iterrows():
    start_address = row['Start Address']
    end_address = row['End Address']

    start_lat, start_lon = get_lat_lon(start_address, address_data)    
    end_lat, end_lon = get_lat_lon(end_address, address_data)   

    if start_lat == "EMPTY" and start_lon == "EMPTY" or end_lat == "EMPTY" and end_lon == "EMPTY":
        new_addresses.add(start_address)
        new_addresses.add(end_address)
    

addresses_to_check = list(new_addresses)

if len(addresses_to_check) > 0:
    getGeo.main(addresses_to_check)
else:
    print("Locations check: OK")

# Load JSON data from a file
with open('Data/GeoLocation.json', 'r') as json_file:
    address_data = json.load(json_file)

# Create layer groups for different distance categories
short_distance_layer = folium.FeatureGroup(name='Short Distance (<55 km)')
long_distance_layer = folium.FeatureGroup(name='Long Distance (≥55 km)')

for index, row in df.iterrows():
    start_address = row['Start Address']
    end_address = row['End Address']
    housing = row['Housing Location']
    work = row['Work Location']
    weight = row['NrPassengers']
    distance = row['Travel Distance']

    start_lat, start_lon = get_lat_lon(start_address, address_data)    
    end_lat, end_lon = get_lat_lon(end_address, address_data) 


    # Determine which layer to add to based on distance
    if distance < 55:
        distance_layer = short_distance_layer
        distance_color = 'blue'
    else:
        distance_layer = long_distance_layer
        distance_color = 'red'


    #Add markers for start and end locations for DISTANCES
    folium.Marker(
        location=[start_lat, start_lon],
        popup=work,
        icon=folium.Icon(color='green')
    ).add_to(distance_layer)

    folium.Marker(
        location=[end_lat, end_lon],
        popup=housing,
        icon=folium.Icon(color='red')

        ).add_to(distance_layer)

    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        opacity=0.5,
        weight=weight,
        color=distance_color
    ).add_to(distance_layer)


# Add layer groups to the map
short_distance_layer.add_to(m)
long_distance_layer.add_to(m)

# Add layer control to the map
folium.LayerControl().add_to(m)



# Save the map to an HTML file
m.save("map.html")