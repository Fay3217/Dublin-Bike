from flask import Flask, g, render_template, jsonify
import sqlalchemy as sqla
import json
from sqlalchemy import text
import traceback
import config
from sqlalchemy import create_engine
import functools
import pandas as pd
import time
import requests
import datetime
import pickle
import pandas as pd



app = Flask(__name__, static_url_path='')
app.config.from_object('config')

# actions related to database
def connect_to_database( ):
 engine = create_engine("mysql://{}:{}@{}:{}/{}".format(config.USER,
                                                        config.PASSWORD,
                                                         config.URI,
                                                         config.PORT,
                                                         config.DB), echo=True)
 Connection= engine.connect()
 return Connection

def get_db():
 db = getattr(g, '_database', None)
 if db is None:
   db = g._database = connect_to_database()
 return db

@app.teardown_appcontext
def close_connection(exception):
 db = getattr(g, '_database', None)
 if db is not None:
  db.close()


# read station data
@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
 engine = get_db()
 sql = "select * from station;"
 try:
   with engine.connect() as conn:
     rows = conn.execute(text(sql)).fetchall()
     print('#found {} stations', len(rows), rows)
     return jsonify([row._asdict() for row in rows]) # use this formula to turn the rows into a list of dicts
 except:
     print(traceback.format_exc())
     return "error in get_stations", 404


# connect to main page
@app.route("/")
def map():
    # return app.send_static_file('index.html')
    return render_template('index.html')



@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
  engine = get_db()
  df = pd.read_sql_query("select * from availability where number = %(number)s", engine, params={"number":
station_id})
  
  df['last_update'] = pd.to_datetime(df.last_update, unit='ms')
  df.set_index('last_update', inplace=True)
  res = df['available_bikes'].resample('1H').mean()
  res_stands = df['available_stands'].resample('1H').mean()

  hourly_res = []
  for hour in range(24):
      hourly_res.append([hour,
                         res[res.index.hour == hour].mean(),
                         res_stands[res_stands.index.hour == hour].mean()])
  return jsonify(data=hourly_res)


@app.route("/real_time_data")
def get_heatmap_real_time():
    now = datetime.datetime.now()
    r = requests.get(config.STATIONS_URI,
                             params={"apiKey": config.JCKEY,
                                     "contract": config.NAME})
    dynamic_bike_data = json.loads(r.text)
    return jsonify(dynamic_bike_data)


@app.route("/predicted_data_24/<int:station_id>")
def get_predicted_data_24(station_id):

    with open('./model_available_bikes.pkl', 'rb') as f:
        model_available_bikes = pickle.load(f)

    with open('./model_available_stands.pkl', 'rb') as f:
        model_available_stands = pickle.load(f)

    # Fake data
    fake_data = [station_id, 22817, 1038, 10000, 73, 6.55, 6.29, 6.88, 0, 0, 0, 0, 0, 0, 0, 
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 

    
    position_index = 15
    hour_list = []
    for hour in range(24):
      fake_data[position_index] = 1
      input_data = pd.DataFrame([fake_data])
      result_bikes = model_available_bikes.predict(input_data)
      result_stands = model_available_stands.predict(input_data)
      # result is a one number list. we can't append list, so we append the first number of list.
      hour_list.append([hour, 
                       result_bikes[0],
                       result_stands[0]])
      fake_data[position_index] = 0
      position_index += 1


    return jsonify(data=hour_list)

    
    
@app.route("/predicted_data_7/<int:station_id>")
def get_predicted_data_7(station_id):

    with open('./model_available_bikes.pkl', 'rb') as f:
        model_available_bikes = pickle.load(f)

    with open('./model_available_stands.pkl', 'rb') as f:
        model_available_stands = pickle.load(f)

    # Fake data
    fake_data = [station_id, 22817, 1038, 10000, 73, 6.55, 6.29, 6.88, 0, 0, 0, 0, 0, 0, 0, 
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    
    position_index = 8
    week_list = []
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for hour in week:
      fake_data[position_index] = 1
      input_data = pd.DataFrame([fake_data])
      result_bikes = model_available_bikes.predict(input_data)
      result_stands = model_available_stands.predict(input_data)
      # result is a one number list. we can't append list, so we append the first number of list.
      week_list.append([hour, 
                       result_bikes[0],
                       result_stands[0]])
      fake_data[position_index] = 0
      position_index += 1


    return jsonify(data=week_list)


  



if __name__ == "__main__":
 app.run(debug=True)