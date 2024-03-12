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

URL = "dbikes.ckujvx4azj9q.us-east-1.rds.amazonaws.com"
PORT = "3306"

DB = "dbikes"
USER = "liaoliao"
PASSWORD = "12345678"

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URL, PORT, DB), echo=True)


sql = """
CREATE TABLE IF NOT EXISTS currentweather (
    main VARCHAR(40),
    description VARCHAR(40),
    temp FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    pressure INTEGER,
    visibility INTEGER,
    humidity INTEGER,
    dt INTEGER,
    CONSTRAINT dt PRIMARY KEY (dt)
)
"""

try:
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)
