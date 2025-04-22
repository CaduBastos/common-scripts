import requests
from datetime import datetime 

open_wheather_api_key = "96b420e3fb1703c366657ad85a4de20e"

#Pelotas-RS latitude and longitude
lat = "-31.776"
lon = "-52.3594"

open_weather_Url = "https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid="+open_wheather_api_key

answer = requests.get(open_weather_Url)

if answer.status_code == 200:
    data = answer.json()

    timestamp = data["dt"]
    date = datetime.fromtimestamp(timestamp)

    print(data["name"])
    print(date)

    print(" ")

    print("Temperatura:"+str(int(data["main"]["temp"])/10)+"ºC")
    print("Temperatura mínima:"+str(int(data["main"]["temp_min"])/10)+"ºC")
    print("Temperatura máxima:"+str(int(data["main"]["temp_max"])/10)+"ºC")
    print("Sensação térmica:"+str(int(data["main"]["feels_like"])/10)+"ºC")

    print("Umidade:"+str(data["main"]["humidity"])+"%")
else:
    print("ERROR:", answer.status_code)

    
