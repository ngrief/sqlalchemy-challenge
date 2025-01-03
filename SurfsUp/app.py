# Import the dependencies
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Set up the SQLite database
database_path = "resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# Reflect the database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data as JSON."""
    session = Session(engine)
    # Find the most recent date in the data set
    latest_date = session.query(func.max(Measurement.date)).scalar()
    # Calculate the date one year ago from the most recent date
    year_ago = pd.to_datetime(latest_date) - pd.DateOffset(years=1)
    year_ago = year_ago.strftime("%Y-%m-%d")
    # Query for the date and precipitation data
    precipitation_data = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= year_ago)
        .all()
    )
    session.close()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations."""
    session = Session(engine)
    # Query all stations
    stations_data = session.query(Station.station).all()
    session.close()

    # Convert the query results to a list
    stations_list = [station[0] for station in stations_data]
    return jsonify(stations_list)

# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the previous year."""
    session = Session(engine)
    # Find the most active station
    most_active_station = (
        session.query(Measurement.station)
        .group_by(Measurement.station)
        .order_by(func.count(Measurement.station).desc())
        .first()
    )[0]
    # Find the most recent date and calculate one year back
    latest_date = session.query(func.max(Measurement.date)).scalar()
    year_ago = pd.to_datetime(latest_date) - pd.DateOffset(years=1)
    year_ago = year_ago.strftime("%Y-%m-%d")
    # Query for the temperature observations
    tobs_data = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == most_active_station)
        .filter(Measurement.date >= year_ago)
        .all()
    )
    session.close()

    # Return the data as JSON
    return jsonify(tobs_data)

# Start route
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return min, avg, and max temperatures from the start date."""
    session = Session(engine)
    temps = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )
    session.close()

    # Return the results as JSON
    return jsonify({"start_date": start, "temps": temps[0]})

# Start and end route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return min, avg, and max temperatures between start and end dates."""
    session = Session(engine)
    temps = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )
    session.close()

    # Return the results as JSON
    return jsonify({"start_date": start, "end_date": end, "temps": temps[0]})

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
