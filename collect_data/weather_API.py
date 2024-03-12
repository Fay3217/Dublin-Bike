#openweather
import requests
weather_data = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=53.35&lon=-6.25&appid=d600a7f76cb55b834000fa6f6e409193')
for i in weather_data.keys():
    print(i,":",(weather_data[i]))
