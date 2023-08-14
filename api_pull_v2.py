import requests
from flask import Flask, jsonify
import sqlite3
import logging
import plotly

app = Flask(__name__)

# Your API key
# Old one#API_KEY = "zyK5oR9gHh0c5ApgkPsAUoAX7KsfneUujZESuLxi"
API_KEY = "Jbyqm6kf6txCRjvjfz6NMXB5OCdtJ4gV9KhlfgPW"
#API_KEY = "yk2ZpqETKnPX5C29VA8kIeI69VaReeb4K2RxUPbw"

# Base URLs for the APIs
PARKS_API_URL = "https://developer.nps.gov/api/v1/parks?limit=450"
TOPICS_API_URL = "https://developer.nps.gov/api/v1/topics?limit=450"


# Function to fetch data from the NPS API
def fetch_data(api_url):
    try:
        params = {"api_key": API_KEY}
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception if the API call fails
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching data from the API: {str(e)}")
        return None

# Function to create the parks database
def create_parks_db():
    try:
        connection = sqlite3.connect("parks.db")
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parks (
                parkCode TEXT PRIMARY KEY,
                fullName TEXT,
                stateCode TEXT,
                latitude REAL,
                longitude REAL
            )
        ''')

        parks_data = fetch_data(PARKS_API_URL)

        if parks_data and "data" in parks_data:
            #for park in parks_data["data"][:100]:
            for park in parks_data["data"]:
                cursor.execute('''
                    INSERT OR IGNORE INTO parks (parkCode, fullName, stateCode, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?)
                ''', (park["parkCode"], park["fullName"], park["states"], park["latitude"], park["longitude"]))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating the parks database: {str(e)}")

# Function to create the topics database
def create_topics_db():
    try:
        connection = sqlite3.connect("topics.db")
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                name TEXT
            )
        ''')

        topics_data = fetch_data(TOPICS_API_URL)

        if topics_data and "data" in topics_data:
            for topic in topics_data["data"]:
                cursor.execute('''
                    INSERT OR IGNORE INTO topics (id, name)
                    VALUES (?, ?)
                ''', (topic["id"], topic["name"]))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating the topics database: {str(e)}")


        
if __name__ == '__main__':
    logging.basicConfig(filename='api.log', level=logging.ERROR)  # Configure logging to write errors to a log file
    create_parks_db()
    create_topics_db()
