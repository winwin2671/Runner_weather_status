import json
import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import api_key

app = Flask(__name__)


@app.route("/")
def index():
    city = 'Bangkok' # request.form.get("city")
    units = 'metric'  # request.form.get("units")
    lat = 13.75  #will make it convert later
    lon = 100.5167 #will make it convert later
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
 
    weather_response = requests.get(weather_url)
    air_response = requests.get(air_url)

    data = weather_response.json()
    data_air = air_response.json()

    print(json.dumps(data, indent=4))
    print(json.dumps(data_air, indent=4))

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    feels_like = data["main"]["feels_like"]
    aqi = data_air["list"][0]["main"]["aqi"]
    #uv_index = data["list"][0]["components"]["uvi"] #openweather Deprecated it for the free version
    #precipitation = data["list"][0]["components"]["precipitation"] 

    if temperature >= 35 and temperature <= -27:
        message = f"Temperature may make it difficult to run: {temperature}°"
    elif humidity <= 70:
        message = f"Humidity may make it difficult to run as it feels like {feels_like}°"
    elif aqi >= 4:
           message = f"Air quality may not be suitable for running. The AQI level is {aqi}"
    else:
        message = "It's a great day for running. Enjoy!"
      

    print(message)

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
