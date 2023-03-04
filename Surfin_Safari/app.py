#import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#create engine and reflect db with "hawaii.sqlite"
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

#create variables for tables
measurements = Base.classes.measurement
stations = Base.classes.station

#find date of 12 months prior to most recent date in data
def find_last_12_date(session):
    #order dates
    date_descending = session.query(measurements.date).order_by(measurements.date.desc())
    #find 12 months prior date and convert to string
    date_last_12 = str(dt.date.fromisoformat((date_descending[0][0]))-dt.timedelta(days=365))
    return date_last_12

#create Flask app
app = Flask(__name__)

#define routes from homepage
@app.route("/")
def homepage():
    print("Requesting Homepage")
    return (f"Welcome to the Surfin Safari Climate Data Homepage!<br>"
            f"Use the available routes below:<br>"
            f"<li>/api/v1.0/precipitation"
            f"<li>/api/v1.0/stations"
            f"<li>/api/v1.0/tobs"
            f"<li>/api/v1.0/tobs/start_date"
            f"<li>/api/v1.0/tobs/start_date/end_date"
            )

#define static routes
@app.route("/api/v1.0/precipitation")
def get_precipitation():
    print("Requesting last 12 months precipitation data")
    #connect session
    session = Session(engine)
    date_last_12 = find_last_12_date(session)
    #all stations combined sum of daily precipitation data for last 12 months
    prcp_last_12 = session.query(measurements.date, func.sum(measurements.prcp))\
        .group_by(measurements.date)\
        .filter(measurements.date > date_last_12)
    #close session
    session.close()
    return jsonify(dict(prcp_last_12))

@app.route("/api/v1.0/stations")
def get_stations():
    print("Requesting all stations ID")
    #connect session
    session = Session(engine)
    #all stations id
    total_stations = session.query(stations.id, stations.station)
    total_stations = dict(total_stations)
    #close session
    session.close()
    return jsonify(total_stations)

@app.route("/api/v1.0/tobs")
def get_tobs():
    print("Requesting TOBS of most active station")
    #connect session
    session = Session(engine)
    #query for most active station
    active_stations = session.query(measurements.station, func.count(measurements.date))\
        .group_by(measurements.station)\
        .order_by(func.count(measurements.date).desc())
    #USC00519281 is most active
    most_active = active_stations[0][0]
    date_last_12 = find_last_12_date(session)
    #query and filter last 12 months tobs of most active station
    most_active_tobs_last_12 = session.query(measurements.date, measurements.tobs)\
        .filter(measurements.station == most_active)\
        .filter(measurements.date > date_last_12)
    #create list of dictionaries for date and temp
    tobs_list = []
    for _ in most_active_tobs_last_12:
        tobs_list.append({"date": _[0], "temp": _[1]})
    #create list to jsonify
    tobs_jsonify = [most_active, tobs_list]
    #close session
    session.close()
    return jsonify(tobs_jsonify)

#define dynamic routes
@app.route("/api/v1.0/tobs/<start_date>")
def get_tobs_start_date(start_date):
    #connect session
    session = Session(engine)
    
    #close session
    session.close()
    return "incomplete code"

#calculate min, max, avg temps for all stations from start date to end date in data
@app.route("/api/v1.0/tobs/<start_date>/<end_date>")
def get_tobs_start_end_date(start_date, end_date):
    #connect session
    session = Session(engine)
    
    #close session
    session.close()

    return "incomplete code"

if __name__ == "__main__":
    app.run(debug=True)