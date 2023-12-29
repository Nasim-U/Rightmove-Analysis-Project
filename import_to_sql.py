import pandas as pd
import mysql.connector
import numpy as np


# Database connection parameters
server = 'localhost' 
database = 'database' 
username = 'username' 
password = 'password'

# Establishing the connection
conn = mysql.connector.connect(
    host=server,
    user=username,
    passwd=password,
    database=database
)

# Path to your CSV file
csv_file_path = 'C:/Users/censored/Documents/Rightmove Project/sales_data_reading.csv'

# Read CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Replace 'nan' with 'None' in the DataFrame
df = df.replace({np.nan: None})
# Specify the name of the target table in your database
table_name = 'rightmove_scraped'

# Import the data from DataFrame to SQL table

for index, row in df.iterrows():
    cursor = conn.cursor()
    insert_query = f"INSERT INTO {table_name} (Links,Address,Description,Price,DrivingTimeE15,TrainTimeE15,DrivingTimeLE5,TrainTimeLE5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (row['Links'], row['Address'], row['Description'], row['Price'], row['Time taken to home'], row['Train time taken to home'], row['DrivingTimeLE5'], row['TrainTimeLE5']))
    conn.commit()
    cursor.close()

# Close the connection
conn.close()
print("complete")
