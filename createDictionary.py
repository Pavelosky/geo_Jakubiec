import pandas as pd
import json

# Function to read addresses from Excel
def read_addresses_from_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df




# Main function to read, process, and save the updated DataFrame
def main():
    file_path = 'Geolocalization.xlsx'
    
    # Read addresses from the Excel file
    df = read_addresses_from_excel(file_path)


    df.fillna('EMPTY', inplace=True)
    dict_data = df.to_dict(orient='index')

    json_file_path = 'GeoLocation.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(dict_data, json_file, indent=4)
    
    print(f"Dictionary successfully saved to {json_file_path}")

    # Save the updated DataFrame back to the Excel file
    #df.to_excel(file_path, index=False, engine='openpyxl')

# Run the main function
if __name__ == "__main__":
    main()
