import os
import sqlite3
import plotly
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Function to fetch data from the parks database
def fetch_parks_data():
    connection = sqlite3.connect("parks.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM parks")
    parks_data = cursor.fetchall()
    connection.close()
    return parks_data

# Function to fetch campground data for a specific park
def fetch_campgrounds_for_park(park_code):
    connection = sqlite3.connect("campgrounds.db")
    cursor = connection.cursor()
    cursor.execute("SELECT campgroundName, occupancy FROM campgrounds WHERE parkCode = ?", (park_code,))
    campgrounds_data = cursor.fetchall()
    connection.close()
    return [{"name": campground[0], "occupancy": campground[1]} for campground in campgrounds_data]
    
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

@app.route('/api/get_topics', methods=['GET'])
def get_topics():
    # Fetch all topics from your database
    connection = sqlite3.connect("topics.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM topics")
    all_topics = cursor.fetchall()
    connection.close()

    # Convert the topics to a list of dictionaries
    topics = [{"id": topic[0], "name": topic[1]} for topic in all_topics]

    return jsonify({"data": topics})
    
@app.route('/api/parks/<string:park_code>/campgrounds', methods=['GET']) 
def get_campgrounds(park_code):
    campgrounds = fetch_campgrounds_for_park(park_code)
    return jsonify({"data": campgrounds})
    
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