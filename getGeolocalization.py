import pandas as pd
import geocoder
import time
from openpyxl import load_workbook

# Function to read addresses from Excel
def read_addresses_from_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

# New comment to test commit

# Define a function to geocode an address
def geocode_address(address):
    g = geocoder.osm(address)
    if g.ok:
        print(g.lat + " - " + g.lng + ": OK")
        return (g.lat, g.lng)
    else:
        return None

# Main function to read, process, and save the updated DataFrame
def main():
    file_path = 'Geolocalization.xlsx'
    
    # Read addresses from the Excel file
    df = read_addresses_from_excel(file_path)
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        start_address = row['Address']
        start_lat = row['Latitude']
        start_lon = row['Longitude']
        
        # Check if geolocation is missing and needs to be filled
        if pd.isna(start_lat) or pd.isna(start_lon):
            start_location = geocode_address(start_address)
            
            if start_location:
                start_lat, start_lon = start_location
                df.at[index, 'Latitude'] = start_lat
                df.at[index, 'Longitude'] = start_lon
                time.sleep(1)  # Introduce a delay between geocoding requests
    
    
    # Save the updated DataFrame back to the Excel file
    df.to_excel(file_path, index=False, engine='openpyxl')

# Run the main function
if __name__ == "__main__":
    main()
