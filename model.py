import pandas as pd
import requests
import time

def get_coordinates(park_name):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': park_name,
        'format': 'json',
        'limit': 1
    }

    try:
        response = requests.get(url, params=params)
        print("Response content:", response.content)  # Print response content for debugging
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            print("Error: Park not found")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Load the park sizes data into a DataFrame
sizes_df = pd.read_csv('park_sizes.csv')  # Replace 'park_sizes.csv' with the actual filename

# Create an empty list to store park locations
park_locations = []

# Loop through each row in the park sizes DataFrame
for index, row in sizes_df.iterrows():
    park_name = row['location']
    park_size = row['gis_acres']
    
    # Get latitude and longitude coordinates for the park
    latitude, longitude = get_coordinates(park_name)
    
    if latitude is not None and longitude is not None:
        # Add park location to the list
        park_locations.append({'name': park_name, 'latitude': latitude, 'longitude': longitude, 'size': park_size})
    time.sleep(1)

# Convert the list of park locations into a DataFrame
park_locations_df = pd.DataFrame(park_locations)

# Save the DataFrame to a new CSV file
park_locations_df.to_csv('park_locations.csv', index=False)  # Replace 'park_locations.csv' with the desired filename
