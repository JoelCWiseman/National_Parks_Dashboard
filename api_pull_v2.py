import requests
from flask import Flask, jsonify
import sqlite3
import logging

app = Flask(__name__)

# Your API key
# Old one#API_KEY = "zyK5oR9gHh0c5ApgkPsAUoAX7KsfneUujZESuLxi"
#API_KEY = "Jbyqm6kf6txCRjvjfz6NMXB5OCdtJ4gV9KhlfgPW"
API_KEY = "yk2ZpqETKnPX5C29VA8kIeI69VaReeb4K2RxUPbw"

# Base URLs for the APIs
PARKS_API_URL = "https://developer.nps.gov/api/v1/parks?limit=450"
#ACTIVITIES_API_URL = "https://developer.nps.gov/api/v1/activities/parks?limit=450"
#AMENITIES_API_URL = "https://developer.nps.gov/api/v1/amenities?limit=450"
CAMPGROUNDS_API_URL = "https://developer.nps.gov/api/v1/campgrounds?limit=450"
#EVENTS_API_URL = "https://developer.nps.gov/api/v1/events?limit=450"

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

# Function to create the activities database
#def create_activities_db():
 #   try:
  #      connection = sqlite3.connect("activities.db")
   #     cursor = connection.cursor()

    #    cursor.execute('''
     #       CREATE TABLE IF NOT EXISTS activities (
      #          parkCode TEXT,
       #         activityName TEXT,
        #        FOREIGN KEY (parkCode) REFERENCES parks (parkCode)
         #   )
     #   ''')
#
 #       parks_data = fetch_data(PARKS_API_URL)
#
 #       if parks_data and "data" in parks_data:
  #          #for park in parks_data["data"][:100]:
   ##         for park in parks_data["data"]:
     #           park_code = park["parkCode"]
      #          activities_data = fetch_data(f"{ACTIVITIES_API_URL}/{park_code}")
       #         if activities_data and "data" in activities_data:
        #            activities = [activity["name"] for activity in activities_data["data"]]
         #           for activity in activities:
          #              cursor.execute('''
           #                 INSERT INTO activities (parkCode, activityName)
            #                VALUES (?, ?)
   #          #           ''', (park_code, activity))
#
 #       connection.commit()
  #      connection.close()
   # except sqlite3.Error as e:
    #    logging.error(f"An error occurred while creating the activities database: {str(e)}")

# Function to create the amenities database
#def create_amenities_db():
 #   try:
  #      connection = sqlite3.connect("amenities.db")
   #     cursor = connection.cursor()
#
 #       cursor.execute('''
  #          CREATE TABLE IF NOT EXISTS amenities (
   #             parkCode TEXT,
    #            amenityName TEXT,
     #           FOREIGN KEY (parkCode) REFERENCES parks (parkCode)
      #      )
       # ''')

        #parks_data = fetch_data(PARKS_API_URL)
#
 #       if parks_data and "data" in parks_data:
            #for park in parks_data["data"][:200]:
  #          for park in parks_data["data"]:
   #             park_code = park["parkCode"]
    #            amenities_data = fetch_data(f"{AMENITIES_API_URL}/{park_code}")
     #           if amenities_data and "data" in amenities_data:
      #              amenities = [amenity["name"] for amenity in amenities_data["data"]]
       #             for amenity in amenities:
        #                cursor.execute('''
         #                   INSERT INTO amenities (parkCode, amenityName)
          #                  VALUES (?, ?)
           #             ''', (park_code, amenity))

  #      connection.commit()
   #     connection.close()
  #  except sqlite3.Error as e:
   #     logging.error(f"An error occurred while creating the amenities database: {str(e)}")

# Function to create the campgrounds database
def create_campgrounds_db():
    try:
        connection = sqlite3.connect("campgrounds.db")
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campgrounds (
                parkCode TEXT PRIMARY KEY,
                campgroundName TEXT,
                description TEXT,
                campsites INTEGER
            )
        ''')

        parks_data = fetch_data(CAMPGROUNDS_API_URL)

        if parks_data and "data" in parks_data:
            for park in parks_data["data"]:
                park_code = park["parkCode"]
                cursor.execute('''
                    INSERT OR IGNORE INTO campgrounds (parkCode)
                    VALUES (?)
                ''', (park_code,))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating the campgrounds database: {str(e)}")

# Function to create the events database
#def create_events_db():
 #   try:
  #      connection = sqlite3.connect("events.db")
   #     cursor = connection.cursor()

    #    cursor.execute('''
     #       CREATE TABLE IF NOT EXISTS events (
      #          parkCode TEXT,
       #         category TEXT,
        #        FOREIGN KEY (parkCode) REFERENCES parks (parkCode)
         #   )
        #''')

        #parks_data = fetch_data(PARKS_API_URL)

        #if parks_data and "data" in parks_data:
            #for park in parks_data["data"][:200]:
         #   for park in parks_data["data"]:
          #      park_code = park["parkCode"]
           #     events_data = fetch_data(f"{EVENTS_API_URL}/{park_code}")
            #    if events_data and "data" in events_data:
             #       events = [event["category"] for event in events_data["data"]]
              #      for event in events:
               #         cursor.execute('''
                #            INSERT INTO events (parkCode, category)
                 #           VALUES (?, ?)
                  #      ''', (park_code, event))

        #connection.commit()
        #connection.close()
    #except sqlite3.Error as e:
     #   logging.error(f"An error occurred while creating the amenities database: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(filename='api.log', level=logging.ERROR)  # Configure logging to write errors to a log file
    create_parks_db()
   # create_activities_db()
    #create_amenities_db()
    create_campgrounds_db()  
   # create_events_db()
