import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display
import dbinfo

# connect to database
URL = "dbikes.ckujvx4azj9q.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbikes"
USER = "liaoliao"
PASSWORD = "12345678"

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URL, PORT, DB), echo=True)

r = requests.get(dbinfo.STATIONS_URI,
                             params={"apiKey": dbinfo.JCKEY,
                                     "contract": dbinfo.NAME})
bike_data = json.loads(r.text)

# insert static station infomation onece.
def stations_to_db(stations):

    for station in stations:
       
        vals = (station.get("address"), int(station.get("banking")), int(station.get("bike_stands")), int(station.get("bonus")), station.get(
            "contract_name"), station.get("name"), int(station.get("number")), station.get("position").get("lat"), station.get("position").get("lng"), station.get("status"))
        engine.execute(
            "insert into station values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)
        

    return

stations_to_db(bike_data)

