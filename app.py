import json
import requests
from flask import Flask, render_template, request
from config import api_key

app = Flask(__name__)

def check_city_existence(city):
    location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    location_response = requests.get(location_url)
    data_loc = location_response.json()
    if data_loc:
        return True
    else:
        return False

@app.route("/" ,methods = ['POST', 'GET'])
def index_get():
    city = 'London' #try type random word to see the erorr page
    units = 'metric'
    
    if not check_city_existence(city):
        message="City not found."
        print("City not found.")
        return render_template("error.html", message=message)
    
    location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    location_response = requests.get(location_url)
    data_loc = location_response.json()
    lat = data_loc[0]["lat"]
    lon = data_loc[0]["lon"]


    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    map_url = f"https://tile.openweathermap.org/map/precipitation_new/10/100/200.png?appid={api_key}"   

    weather_response = requests.get(weather_url)
    air_response = requests.get(air_url)
    map_response = requests.get(map_url)

    data = weather_response.json()
    data_air = air_response.json()
    data_map = map_response.content

    image_data = data_map

    print(json.dumps(data, indent=4))
    print(json.dumps(data_air, indent=4))

    if "rain" in data:
        rain = True
    else:
        rain = False
    
    weather = {
        'city': city,
        'temperature': data["main"]["temp"],
        'humidity': data["main"]["humidity"],
        'feels_like' : data["main"]["feels_like"],
        'aqi' : data_air["list"][0]["main"]["aqi"],
        'icon': data['weather'][0]['icon'],
    }


    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    feels_like = data["main"]["feels_like"]
    aqi = data_air["list"][0]["main"]["aqi"]

    if aqi == 1:
        aqi_stat = 'Good'
    elif aqi == 2:
        aqi_stat = 'Fair'
    elif aqi == 3:
        aqi_stat = 'Moderate'
    elif aqi == 4:
        aqi_stat = 'Poor'
    else:
        aqi_stat = 'Very Poor'

    messages = []

    if temperature >= 35 or temperature <= -27:
        messages.append(f"Temperature may make it difficult to run: {temperature}°")

    if aqi >= 4:
        messages.append(f"Air quality may not be suitable for running. The AQI level is {aqi}, {aqi_stat}")

    if rain:
        messages.append("It is raining, be mindful of your running session")

    if humidity > 70 and (feels_like >= 35 or feels_like <= -27):
        messages.append(f"Humidity may make it difficult to run as it feels like {feels_like}°")

    if feels_like >= 35 or feels_like <= -27:
        messages.append(f"It feels like {feels_like}°, may make it difficult to run")

    if not messages:
        messages.append("It's a great day for running. Enjoy!")


    for message in messages:
        print(message)

    return render_template("index.html", messages=messages, image_data=image_data, weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
