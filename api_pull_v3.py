import requests
from flask import Flask, jsonify
import sqlite3
import logging

app = Flask(__name__)

# Your API key
API_KEY = "zyK5oR9gHh0c5ApgkPsAUoAX7KsfneUujZESuLxi"

# Base URLs for the APIs
PARKS_API_URL = "https://developer.nps.gov/api/v1/parks?"
ACTIVITIES_API_URL = "https://developer.nps.gov/api/v1/activities/parks?"
AMENITIES_API_URL = "https://developer.nps.gov/api/v1/amenities?"


# Data retrieval functions to handle pagination and create db
def create_parks_db():
    try:
        connection = sqlite3.connect("parks.db")
        cursor = connection.cursor()

        page = 1
        while True:
            parks_data = fetch_data(PARKS_API_URL, page)
            if parks_data and "data" in parks_data:
                for park in parks_data["data"]:
                    cursor.execute('''
                        INSERT OR IGNORE INTO parks (parkCode, fullName, stateCode, latitude, longitude)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (park["parkCode"], park["fullName"], park["states"], park["latitude"], park["longitude"]))

            if "next" in parks_data["links"]:
                page += 1
            else:
                break

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating the parks database: {str(e)}")


def create_activities_db():
    try:
        connection = sqlite3.connect("activities.db")
        cursor = connection.cursor()

        page = 1
        while True:
            # Fetching activities for each park requires using the parkCode obtained from the parks_data.     
            parks_data = fetch_data(PARKS_API_URL, page)
            if parks_data and "data" in parks_data:
                for park in parks_data["data"]:
                    park_code = park["parkCode"]
                    activities_data = fetch_data(f"{ACTIVITIES_API_URL}/{park_code}")
                    if activities_data and "data" in activities_data:
                        activities = [activity["name"] for activity in activities_data["data"]]
                        for activity in activities:
                            cursor.execute('''
                                INSERT INTO activities (parkCode, activityName)
                                VALUES (?, ?)
                            ''', (park_code, activity))

            if "next" in parks_data["links"]:
                page += 1
            else:
                break

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating the activities database: {str(e)}")

def create_amenities_db():
    try:
        connection = sqlite3.connect("amenities.db")
        cursor = connection.cursor()

        page = 1
        while True:
            # Similar logic for amenities retrieval as with activities
            parks_data = fetch_data(PARKS_API_URL, page)
            if parks_data and "data" in parks_data:
                for park in parks_data["data"]:
                    park_code = park["parkCode"]
                    amenities_data = fetch_data(f"{AMENITIES_API_URL}/{park_code}")
                    if amenities_data and "data" in amenities_data:
                        amenities = [amenity["name"] for amenity in amenities_data["data"]]
                        for amenity in amenities:
                            cursor.execute('''
                                INSERT INTO amenities (parkCode, amenityName)
                                VALUES (?, ?)
                            ''', (park_code, amenity))

            if "next" in parks_data["links"]:
                page += 1
            else:
                break

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating the amenities database: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(filename='api.log', level=logging.ERROR)
    create_parks_db()
    create_activities_db()
    create_amenities_db()