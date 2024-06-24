import folium
import pandas as pd

# Define a function to read addresses and coordinates from an Excel file
def read_addresses_from_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

# Read addresses and coordinates from the Excel file


##############################################
#  Document with locations to display on map #
##############################################

file_path = 'RouteVisualizationData.xlsm'
df = read_addresses_from_excel(file_path)





# Create a map centered on the Netherlands
m = folium.Map(location=[52.1, 5.3], zoom_start=8)

# Iterate through each row in the DataFrame and plot trips
for index, row in df.iterrows():
    start_lat = row['Start Latitude']
    start_lon = row['Start Longitude']
    end_lat = row['End Latitude']
    end_lon = row['End Longitude']
    start_address = row['Start Address']
    end_address = row['End Address']

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
        color='blue'
    ).add_to(m)

# Save the map to an HTML file
m.save("map.html")