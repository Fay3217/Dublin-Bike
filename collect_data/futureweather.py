import requests
weather_data = requests.get('https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&exclude=hourly,daily&appid=d600a7f76cb55b834000fa6f6e409193').json()
for i in weather_data.keys():
    print(i,":",(weather_data[i]))