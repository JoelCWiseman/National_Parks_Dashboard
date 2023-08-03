import requests
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Your API key
API_KEY = "yk2ZpqETKnPX5C29VA8kIeI69VaReeb4K2RxUPbw"

# Base URLs for the APIs
PARKS_API_URL = "https://developer.nps.gov/api/v1/parks"
ACTIVITIES_API_URL = "https://developer.nps.gov/api/v1/activities/parks"
AMENITIES_API_URL = "https://developer.nps.gov/api/v1/amenities"

# Function to fetch data from the NPS API
def fetch_data(api_url):
    params = {"api_key": API_KEY}
    response = requests.get(api_url, params=params)
    return response.json()

# Function to create the parks database
def create_parks_db():
    connection = sqlite3.connect("parks.db")
    cursor = connection.cursor()

    # Create a table for parks data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parks (
            parkCode TEXT PRIMARY KEY,
            fullName TEXT,
            stateCode TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    # Fetch park data from the API
    parks_data = fetch_data(PARKS_API_URL)

    # Insert park data into the table
    for park in parks_data["data"]:
        cursor.execute("""
            INSERT OR IGNORE INTO parks (parkCode, fullName, stateCode, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """, (park["parkCode"], park["fullName"], park["states"], park["latitude"], park["longitude"]))

    connection.commit()
    connection.close()

# Function to create the activities database
def create_activities_db():
    connection = sqlite3.connect("activities.db")
    cursor = connection.cursor()

    # Create a table for activities data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            parkCode TEXT,
            activityName TEXT,
            FOREIGN KEY (parkCode) REFERENCES parks (parkCode)
        )
    """)

    # Fetch activities data from the API for each park
    parks_data = fetch_data(PARKS_API_URL)

    for park in parks_data["data"]:
        park_code = park["parkCode"]
        activities_data = fetch_data(f"{ACTIVITIES_API_URL}/{park_code}")
        activities = [activity["name"] for activity in activities_data["data"]]
        for activity in activities:
            cursor.execute("""
                INSERT INTO activities (parkCode, activityName)
                VALUES (?, ?)
            """, (park_code, activity))

    connection.commit()
    connection.close()

# Function to create the amenities database
def create_amenities_db():
    connection = sqlite3.connect("amenities.db")
    cursor = connection.cursor()

    # Create a table for amenities data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS amenities (
            parkCode TEXT,
            amenityName TEXT,
            FOREIGN KEY (parkCode) REFERENCES parks (parkCode)
        )
    """)

    # Fetch amenities data from the API for each park
    parks_data = fetch_data(PARKS_API_URL)

    for park in parks_data["data"]:
        park_code = park["parkCode"]
        amenities_data = fetch_data(f"{AMENITIES_API_URL}/{park_code}")
        amenities = [amenity["name"] for amenity in amenities_data["data"]]
        for amenity in amenities:
            cursor.execute("""
                INSERT INTO amenities (parkCode, amenityName)
                VALUES (?, ?)
            """, (park_code, amenity))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_parks_db()
    create_activities_db()
    create_amenities_db()