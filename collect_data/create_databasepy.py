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

# connect to database
URL = "dbikes.ckujvx4azj9q.us-east-1.rds.amazonaws.com"
PORT = "3306"
# the first time try to create a database, you need to write the database name in your ec2 database, that should be 'sys', the defualt database.
DB = "dbikes"
USER = "liaoliao"
PASSWORD = "12345678"

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URL, PORT, DB), echo=True)

# create dbikes database
sql = """
CREATE DATABASE IF NOT EXISTS dbikes;
"""
engine.execute(sql)

# create station table
sql = """
CREATE TABLE IF NOT EXISTS station (
    address VARCHAR(256),
    banking INTEGER,
    bike_stands INTEGER,
    bonus INTEGER,
    contract_name VARCHAR(256),
    name VARCHAR(256),
    number INTEGER,
    position_lat REAL,
    position_lng REAL,
    status VARCHAR(256),
    CONSTRAINT station_number PRIMARY KEY (number)
)
"""

try:
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)

# create availability table   
sql = """
CREATE TABLE IF NOT EXISTS availability (
    number INTEGER,
    available_bikes INTEGER,
    available_stands INTEGER,
    last_update VARCHAR(256),
    FOREIGN KEY (number) REFERENCES station(number)
)
"""

try:
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)
