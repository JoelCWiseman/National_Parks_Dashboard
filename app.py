import os
import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Function to fetch data from the parks database
def fetch_parks_data():
    connection = sqlite3.connect("parks.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM parks")
    parks_data = cursor.fetchall()
    connection.close()
    return parks_data

# Function to fetch activities for a specific park
def fetch_activities_for_park(park_code):
    connection = sqlite3.connect("activities.db")
    cursor = connection.cursor()
    cursor.execute("SELECT activityName FROM activities WHERE parkCode = ?", (park_code,))
    activities_data = cursor.fetchall()
    connection.close()
    return [activity[0] for activity in activities_data]

# Function to fetch amenities for a specific park
def fetch_amenities_for_park(park_code):
    connection = sqlite3.connect("amenities.db")
    cursor = connection.cursor()
    cursor.execute("SELECT amenityName FROM amenities WHERE parkCode = ?", (park_code,))
    amenities_data = cursor.fetchall()
    connection.close()
    return [amenity[0] for amenity in amenities_data]

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