#import geocoder
import time
import json
from geopy.geocoders import Nominatim


def geocode_address(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        g = geolocator.geocode(address, timeout=10)
        if g:
            return (g.latitude, g.longitude)
        else:
            return None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None
    

    # Main function to read, process, and save the updated DataFrame
def main(unknown_addresses):

    data_dict = {}
    # Iterate through each row in the DataFrame
    for unknown_address in unknown_addresses:

        new_location = geocode_address(unknown_address)
        time.sleep(1)  # Introduce a delay between geocoding requests

        if new_location:
            loc_lat, loc_lon = new_location
            data_dict[unknown_address] = {
                "Latitude": loc_lat,
                "Longitude": loc_lon
            }

    if data_dict:
        json_file_path = 'Data/GeoLocation.json'
        try:
            with open(json_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = {}

        # Update existing data with new data
        existing_data.update(data_dict)

        # Write updated data back to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        
        print(f"Dictionary successfully saved to {existing_data}")


# Run the main function
if __name__ == "__main__":
    main()