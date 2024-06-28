import json

# Path to your JSON file
json_doc = 'Data/GeoLocation.json'

# Load the JSON data
with open(json_doc, 'r') as json_file:
    data_dict = json.load(json_file)

# Iterate through the dictionary and remove keys with "EMPTY" values
keys_to_remove = []
for address, coordinates in data_dict.items():
    if coordinates['Latitude'] == "EMPTY" or coordinates['Longitude'] == "EMPTY":
        keys_to_remove.append(address)

for key in keys_to_remove:
    del data_dict[key]

# Save the cleaned data back to the JSON file
with open(json_doc, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

# Print the resulting dictionary for verification
print(len(data_dict))