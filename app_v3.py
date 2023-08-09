# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///parks.db")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Parks = Base.classes.parks

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route('/')

@app.route('/api/parks', methods=['GET'])
def get_parks():
     #create a session link
    session = Session(engine)
    
    #Query for precipitation analysis
    results = session.query(Parks)
    
    session.close()

    parks = []
    for park in results:
        park_dict = {
            "parkCode": park[0],
            "fullName": park[1],
            "stateCode": park[2],
            "latitude": park[3],
            "longitude": park[4]
        }
        parks.append(park_dict)
    return jsonify({"data": parks})
    

if __name__ == '__main__':
    app.run(debug=True)
