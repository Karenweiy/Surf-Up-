# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

#reflect the db into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Fill with your start date after /<br/>"
        f"/api/v1.0/<start><br/>"
        f"Fill with your start and end date after /<br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    date_prcp = []
    # Convert list of tuples into normal list
    for i in range(len(results)):
        date_prcp.append({'date':results[i][0],'precipitation':results[i][1]})

    return jsonify(date_prcp)



@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    session = Session(engine)
    stationresult = session.query(Station.station,Station.name).all()

    return jsonify(stationresult)

@app.route("/api/v1.0/tobs")
def tobs():
    # * query for the dates and temperature observations from a year from the last data point.

    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()[0]
    end_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    start_date = end_date - dt.timedelta(365)
    tobsresult = session.query(Measurement.date,Measurement.tobs).filter(func.datetime(Measurement.date) >= start_date).order_by(Measurement.date).all()
    return jsonify(tobsresult)

@app.route("/api/v1.0/<start>")
def tempstart(start):
  
  # Return a JSON list of the minimum temperature, the average temperature,
  #  and the max temperature for a given start or start-end range.
    session = Session(engine)
    startresult = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start)\
                  .group_by(Measurement.date).all()

    return jsonify(startresult)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    rangeresult = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)\
             .group_by(Measurement.date).all()

    return jsonify(rangeresult)

# run app
if __name__ == '__main__':
    app.run(debug=True)
