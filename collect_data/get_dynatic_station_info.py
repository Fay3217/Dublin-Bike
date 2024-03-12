# dbinfo is not a package, is a python file write the basic API information.
import dbinfo
import requests
import json
import time
import traceback
import sys
import datetime
import os
import sqlalchemy as sqla
from sqlalchemy import create_engine

# get data at once
# r = requests.get(dbinfo.STATIONS_URI,
#                  params={"apiKey": dbinfo.JCKEY,
#                         "contract": dbinfo.NAME})
# r = json.loads(r.text)


# connect to database
URL = "dbikes.ckujvx4azj9q.us-east-1.rds.amazonaws.com"
PORT = "3306"
# before run this code, create database by python first.
DB = "dbikes"
USER = "liaoliao"
PASSWORD = "12345678"

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URL, PORT, DB), echo=True)


# write the API data file to a folder, finally we will put the file into google drive for backup
# it will create a lot of files
# def write_to_file(r, now):
#     # remember to write the path, if not, it cause error.
#     file_name = "./data/dynatic_station/bikes_{}".format(now).replace(" ", "_")
#     with open(file_name, "w") as f:
#         f.write(r.text)


# to insert dynamic bike data into database
def dynamic_bike_data_to_db(stations):
    for station in stations:
        vals = (int(station.get("number")), station.get("available_bikes"), station.get("available_bike_stands"), station.get("last_update"))
        engine.execute("insert into availability values(%s, %s, %s, %s)", vals)
        

    return
    
    
# one data sample
# [{"number":42,"contract_name":"dublin","name":"SMITHFIELD NORTH","address":"Smithfield North",
#   "position":{"lat":53.349562,"lng":-6.278198},"banking":false,"bonus":false,"bike_stands":30,
#   "available_bike_stands":9,"available_bikes":21,"status":"OPEN","last_update":1677109602000},


# to get data for every 5 minutes in real time
def main():
    
    while True:
        try:
            now = datetime.datetime.now()
            r = requests.get(dbinfo.STATIONS_URI,
                             params={"apiKey": dbinfo.JCKEY,
                                     "contract": dbinfo.NAME})
            print(r, now)
            dynamic_bike_data = json.loads(r.text)
            # print("----------------------------------------------------")
            # write data into local file.
            # write_to_file(r, now)
            # write data into database
            dynamic_bike_data_to_db(dynamic_bike_data)
            time.sleep(5*60)
            # firstly, try to run the code in every 3 seconds to check it works well.
            # time.sleep(3)
            
            
        except:
            print(traceback.format_exc())
            sys.exit()
    return

# run the function automaticlly
if __name__ == "__main__":
    main()