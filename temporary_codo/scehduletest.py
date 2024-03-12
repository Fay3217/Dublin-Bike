import requests
import json
import schedule
import time
  
def func():
    response_API = requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=d79c1a9a1cdfb2eccce41d23f1fdb971eef387f9')
    print(response_API.status_code)

    data = response_API.text
  
schedule.every(5).minutes.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(5)
