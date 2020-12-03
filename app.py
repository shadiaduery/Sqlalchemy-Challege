# Now that you have completed your initial analysis, 
# design a Flask API based on the queries that you have just developed.
# Use Flask to create your routes.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation. Note there may be dupes - why?"""
    # Design a query to retrieve the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert the query results to a dictionary using 'date' as the key and 'prcp' as the value.
    query_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        query_prcp.append(prcp_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(query_prcp)


@app.route("/api/v1.0/stations")
def names1():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations."""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    # Return a JSON list of stations from the dataset.
    return jsonify(all_stations)
  

@app.route("/api/v1.0/tobs")
def names2():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station
    # for the last year of data.
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_dates = list(np.ravel(results))

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(all_dates)
  
  
@app.route("/api/v1.0/start")
def names3():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than 
    # and equal to the start date.
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= '2017-03-01').all()

    session.close()

    # Convert list of tuples into normal list
    vacation_temps = list(np.ravel(results))

    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start date
    return jsonify(vacation_temps) 

@app.route("/api/v1.0/start_end")
def names4():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start and the end date, calculate the 
    # `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= '2017-03-01').filter(Measurement.date <= '2017-03-15').all()

    session.close()

    # Convert list of tuples into normal list
    date_temp = list(np.ravel(results))


    return jsonify(date_temp)   

if __name__ == '__main__':
    app.run(debug=True)
