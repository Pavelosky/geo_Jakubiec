import folium
import pandas as pd
import json
import getGeo

# Define a function to read addresses and coordinates from an Excel file
def read_addresses_from_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df


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


#group the same commute combinations and sum nr of passengers
grouped_df = df.groupby(['Start Address', 'End Address']).agg({
    'NrPassengers' : 'sum',
    'Travel Distance' : 'first',
    'Housing Location' : 'first',
    'Work Location' : 'first'

}).reset_index()

# Rename 'Passengers' column to 'Occupants'
grouped_df.rename(columns={'Passengers': 'Occupants'}, inplace=True)
# Convert the grouped DataFrame to a dictionary
commutes = grouped_df.to_dict(orient='records')


# Initialize an empty set to store unique addresses
new_addresses = set()

# Create a map centered on the Netherlandsx
m = folium.Map(location=[52.1, 5.3], zoom_start=8)

# # Iterate through each row in the DataFrame and plot trips
for commute in commutes:
    start_address = commute['Start Address']
    end_address = commute['End Address']

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

# # Load JSON data from a file
with open('Data/GeoLocation.json', 'r') as json_file:
    address_data = json.load(json_file)

# Create layer groups for different distance categories
short_distance_layer = folium.FeatureGroup(name='Distance (<30 km)')
mediumextra_distance_layer = folium.FeatureGroup(name='Distance (<50 km)')
long_distance_layer = folium.FeatureGroup(name='Distance (≥60 km)')

low_passengers_layer = folium.FeatureGroup(name='Passengers (<9)')
medium_passengers_layer = folium.FeatureGroup(name='Passengers (<27)')
high_passengers_layer = folium.FeatureGroup(name='Passengers (≥27)')


for commute in commutes:
    start_address = commute['Start Address']
    end_address = commute['End Address']
    housing = commute['Housing Location']
    work = commute['Work Location']
    occupancy = commute['NrPassengers']
    distance = commute['Travel Distance']



    start_lat, start_lon = get_lat_lon(start_address, address_data)    
    end_lat, end_lon = get_lat_lon(end_address, address_data) 


    # Determine which layer to add to based on distance
    if distance < 30:
        distance_layer = short_distance_layer
        distance_color = 'blue'
    elif distance >= 30 and distance < 60:
        distance_layer = mediumextra_distance_layer
        distance_color = "red"
    else:
        distance_layer = long_distance_layer
        distance_color = 'brown'


    #Add markers for start and end locations for DISTANCES
    folium.Marker(
        location=[start_lat, start_lon],
        popup=housing,
        icon=folium.Icon(color='green')
    ).add_to(distance_layer)

    folium.Marker(
        location=[end_lat, end_lon],
        popup=work,
        icon=folium.Icon(color='red')

        ).add_to(distance_layer)

    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        opacity=0.5,
        weight=12,
        color=distance_color
    ).add_to(distance_layer)


        # Determine which layer to add to based on occupancy
    if occupancy < 9:
        occupancy_layer = low_passengers_layer
        occupancy_nr = 3
    elif distance >= 9 and distance < 27:
        occupancy_layer = medium_passengers_layer
        occupancy_nr = 6
    else:
        occupancy_layer = high_passengers_layer
        occupancy_nr = 9

    #Add markers for start and end locations for PASSENGERS
    folium.Marker(
        location=[start_lat, start_lon],
        popup=housing,
        icon=folium.Icon(color='green')
    ).add_to(occupancy_layer)

    folium.Marker(
        location=[end_lat, end_lon],
        popup=work,
        icon=folium.Icon(color='red')

        ).add_to(occupancy_layer)

    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        opacity=0.7,
        weight=occupancy_nr,
        color='White'
    ).add_to(occupancy_layer)


# Add layer groups to the map
short_distance_layer.add_to(m)
mediumextra_distance_layer.add_to(m)
long_distance_layer.add_to(m)

low_passengers_layer.add_to(m)
medium_passengers_layer.add_to(m)
high_passengers_layer.add_to(m)

#Add layer control to the map
folium.LayerControl().add_to(m)



# Save the map to an HTML file
m.save("map.html")