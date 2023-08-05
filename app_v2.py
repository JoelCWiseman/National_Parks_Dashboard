import os
import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Function to create and populate the parks database
def create_parks_database():
    connection = sqlite3.connect("parks.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS parks (parkCode TEXT, fullName TEXT, stateCode TEXT, latitude REAL, longitude REAL)")
    cursor.execute("INSERT INTO parks VALUES ('ABC', 'Park 1', 'NY', 40.7128, -74.0060)")
    cursor.execute("INSERT INTO parks VALUES ('DEF', 'Park 2', 'CA', 34.0522, -118.2437)")
    # Add more parks as needed
    connection.commit()
    connection.close()

# Function to create and populate the activities database
def create_activities_database():
    connection = sqlite3.connect("activities.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS activities (parkCode TEXT, activityName TEXT)")
    cursor.execute("INSERT INTO activities VALUES ('ABC', 'Hiking')")
    cursor.execute("INSERT INTO activities VALUES ('ABC', 'Camping')")
    cursor.execute("INSERT INTO activities VALUES ('DEF', 'Fishing')")
    # Add more activities as needed
    connection.commit()
    connection.close()

# Function to create and populate the amenities database
def create_amenities_database():
    connection = sqlite3.connect("amenities.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS amenities (parkCode TEXT, amenityName TEXT)")
    cursor.execute("INSERT INTO amenities VALUES ('ABC', 'Restrooms')")
    cursor.execute("INSERT INTO amenities VALUES ('DEF', 'Picnic Area')")
    # Add more amenities as needed
    connection.commit()
    connection.close()

# Check if the databases exist, if not create and populate them
if not os.path.exists("parks.db"):
    create_parks_database()

if not os.path.exists("activities.db"):
    create_activities_database()

if not os.path.exists("amenities.db"):
    create_amenities_database()

# Rest of the code remains the same...
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/parks', methods=['GET'])
def get_parks():
    parks_data = fetch_parks_data()
    parks = []
    for park in parks_data:
        park_dict = {
            "parkCode": park[0],
            "fullName": park[1],
            "stateCode": park[2],
            "latitude": park[3],
            "longitude": park[4]
        }
        parks.append(park_dict)
    return jsonify({"data": parks})

@app.route('/api/parks/<string:park_code>/activities', methods=['GET'])
def get_activities(park_code):
    activities = fetch_activities_for_park(park_code)
    return jsonify({"data": activities})

@app.route('/api/parks/<string:park_code>/amenities', methods=['GET'])
def get_amenities(park_code):
    amenities = fetch_amenities_for_park(park_code)
    return jsonify({"data": amenities})

if __name__ == '__main__':
    app.run(debug=True)