from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
conn = engine.connect
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    last_year_df = pd.DataFrame(last_year, columns=['Date','Precipitation'])
    last_year_df.set_index('Date', inplace=True)
    last_year_dict = last_year_df.to_dict()
    return jsonify(last_year_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_activity = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    return jsonify(station_activity)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    most_active_station = most_active_station[0]
    most_active_station_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).filter(Measurement.station == most_active_station).all()
    return jsonify(most_active_station_temps)

if __name__ == "__main__":
    app.run(debug=True)