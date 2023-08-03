import requests
import sqlite3

# API URL and your API key
PARKS_API_URL = "https://developer.nps.gov/api/v1/parks"
API_KEY = "yk2ZpqETKnPX5C29VA8kIeI69VaReeb4K2RxUPbw"

# Fetch data from the API
response = requests.get(PARKS_API_URL, params={"api_key": API_KEY})
data = response.json()

# Connect to the SQLite database (create a new database if it doesn't exist)
conn = sqlite3.connect("national_parks.db")
cursor = conn.cursor()

# Create a table to store the park data
cursor.execute('''CREATE TABLE IF NOT EXISTS parks (
                    parkCode TEXT PRIMARY KEY,
                    fullName TEXT,
                    description TEXT,
                    states TEXT
                  )''')

# Insert the data into the parks table
for park in data["data"]:
    park_data = (park["parkCode"], park["fullName"], park["description"], ",".join(park["states"]))
    cursor.execute("INSERT OR REPLACE INTO parks VALUES (?, ?, ?, ?)", park_data)

# Commit the changes and close the connection
conn.commit()
conn.close()