import googlemaps
import pandas as pd
from datetime import datetime

# Initialize the Google Maps client with API key
gmaps = googlemaps.Client(key='API_Key')
print("API Initialized")
# Load addresses from CSV
csv_file_path = 'C:/Users/censored/Documents/Rightmove Project/sales_data_reading.csv'
df = pd.read_csv(csv_file_path)

# Fixed destination
destination = 'censored'

# List to store travel times
travel_times = []

# Fetch the travel times for each address
for origin in df['Address']:
    result = gmaps.distance_matrix(origin, destination, mode="transit", transit_mode="train", departure_time=datetime.now())
    print(result)

    # Check if the status is OK and duration is available
    if (result['status'] == 'OK' and 
        result['rows'][0]['elements'][0]['status'] == 'OK' and 
        'duration' in result['rows'][0]['elements'][0]):
        duration = result['rows'][0]['elements'][0]['duration']['text']
    else:
        duration = 'N/A' 

    travel_times.append(duration)
print("travel times stored")
# Add the travel times to the DataFrame
df['TrainTime'] = travel_times
print("time taken column added to file")
# Save the updated DataFrame to CSV
df.to_csv(csv_file_path, index=False)
print("file saved")
print("completed")

