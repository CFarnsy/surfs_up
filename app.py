# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set-up the database engine for teh FLask application
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into the classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save the references to each table and create a variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to the database
session = Session(engine)

# Set-up Flask (Create a new Flask instance)
app = Flask(__name__)

# Create the Flask routes
# The 1st route will be the most important. To ensure all the investors
# can easily access all of the analysis, the welcome route will 
# essentially be the entryway to the rest of the analysis
# ***All of the routes should go after the app = Flask(__name__) line
# of code, otherwise the code may not run properly.***

# The 1st task of creating a Flask route is to define what the route
# will be.  The Welcome route will be the root, essentially the homepage
# When creating routes, follow the naming convention /api/v1.0/ followed
# by the name of the route (stations)

# Define the welcome route
@app.route("/")
# Create the function welcome() with a return statement
def welcome():
    return(
    # add the precipitation, stations, tobs, and temp routes using a f-strings
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Run the Flask now
# type flask run in the active terminal window below, ensure the terminal is
# in the same folder the file is saved in

# Every time a new route is created, the code should be aligned to the 
# left in order to avoid errors

# Notice the .\ in the code below, this is used to signify the query 
# continues on the next line and doesn't result in an error.

# Create the precipitation route
@app.route("/api/v1.0/precipitation")
# Create the precipitation() function, add a query to get the date and
# precipitation for the previous year
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
   # Create a dictionary (above) with the data as the key and the 
   # precipitation as the value.  To do this "Jsonify" the 
   # dictionary. Jsonify() is a function that converts the
   # dictionary to a JSON file.

# Create the stations route
@app.route("/api/v1.0/stations")
# Create the stations() function, add a query to get all of the 
# stations in the database.
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
    # We started by unraveling the results int a 1-dimensional
    # array using the function np.ravel() with results as the 
    # parameter. Then converted the unraveled results into a list
    # using the list() function, then convert the array into a list.
    # Next we'll jsonify the list and return it as JSON by adding
    # stations = stations

# Create the temperature observations for the previous year route
@app.route("/api/v1.0/tobs")
# Create the temp_monthly() function and calculate the date one year
# ago from the last date in the database. Then query the primary 
# station for all the temperature observations from the previous year.
# Then unravel the results in a 1 dimensional array, convert the array
# to a list, jsonify the list and return the results and jsonify the 
# temps list and return it
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create the temperature start and end route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create the stats() function, add start and end parameters to
# stats() function. Then create a query to select the minimum,
# average, and maximum temperatures from the SQLite database.
# Create a list called sel and determine the starting and ending
# date using a if-not statement to queary the database. Then unravel
# the results int a 1-dimensional array and convert then to a list.
# Then jsonify the results and return them.
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

