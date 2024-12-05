import sqlite3

# Step 1: Connect to the database
conn = sqlite3.connect("weather.sqlite")  # Replace with your database file name

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Execute a SELECT query
cursor.execute("SELECT * FROM WeatherData")  # Replace with your table name

# Step 4: Fetch and process the data
rows = cursor.fetchall()  # Fetch all rows from the executed query
for row in rows:
    print(row)  # Print each row (you can also process the row data as needed)

# Step 5: Close the connection
conn.close()
