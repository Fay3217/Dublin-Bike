import requests
import json
import time
import traceback
import sys
import datetime
import os
import sqlalchemy as sqla
from sqlalchemy import create_engine
import mysql.connector


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
#     file_name = "./data/weather/catchdata{}".format(
#         now).replace(" ", "_")
#     with open(file_name, "w") as f:
#         f.write(r.text)


# to insert weather data into database
def weather_data_to_db(weathers):
    vals = (weathers.get('weather')[0].get('main'), weathers.get('weather')[0].get('description'),
            float(weathers.get('main').get('temp')), float(weathers.get('main').get('temp_min')),
            float(weathers.get('main').get('temp_max')), int(weathers.get('main').get('pressure')),
            int(weathers.get('visibility')), int(weathers.get('main').get('humidity')),int(weathers.get('dt')))
    engine.execute("insert into currentweather values(%s, %s, %s, %s, %s, %s, %s, %s,%s)",vals)
    return

# to get data for every 30 minutes in real time
def main():
    while True:
        try:
            now = datetime.datetime.now()
            weather_data = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=53.35&lon=-6.25&appid'
                                        '=d600a7f76cb55b834000fa6f6e409193')
            # print(weather_data, now)
            weathers = json.loads(weather_data.text)
            # print("----------------------------------------------------")
            # write data into local file.
            # write_to_file(weather_data, now)
            # write data into database
            weather_data_to_db(weathers)
            # time.sleep(30 * 60)
            time.sleep(30*60)

        except:
            print(traceback.format_exc())
            sys.exit()
    return


# run the function automaticlly
if __name__ == "__main__":
    main()
