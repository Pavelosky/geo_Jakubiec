#import geocoder
import time
import json
# from geopy.geocoders import Nominatim
import googlemaps
import API


#Paid option with google maps 
api_key = API.Key()
gmaps = googlemaps.Client(key=api_key)
def geocode_address(address):
    geocode_result = gmaps.geocode(address)
    
    # Extract latitude and longitude from the geocode result
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None, None

# Free option with limits for request
# def geocode_address(address):
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     try:
#         g = geolocator.geocode(address, timeout=10)
#         if g:
#             return (g.latitude, g.longitude)
#         else:
#             return None
#     except Exception as e:
#         print(f"Error geocoding {address}: {e}")
#         return None
    

# Main function to read, process, and save the updated DataFrame
def main(unknown_addresses):

    i = 1 # nie obraz sie za i xd 
    print(f"------ Start geocoding of {len(unknown_addresses)} address(es) --------")
    data_dict = {}
    # Iterate through each row in the DataFrame
    for unknown_address in unknown_addresses:
        print(f"{i}: {unknown_address}")
        new_location = geocode_address(unknown_address)

        if new_location:
            loc_lat, loc_lon = new_location
            data_dict[unknown_address] = {
                "Latitude": loc_lat,
                "Longitude": loc_lon
            }
        i = i + 1

    

    if len(data_dict) != 0:
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
        
        print(f"Dictionary successfully saved - ({len(existing_data)} rows - {len(data_dict)} new)")
    
    else:
        print(f"----- Geocoding non-successful ------")


# Run the main function
if __name__ == "__main__":
    main()