import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import api_key

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

# The function not have been called at all!


@app.route("/index", methods=["POST"])
def running_suitability():
    city = 'London'  # request.form.get("city")
    date = request.form.get("date")
    units = 'metric'  # request.form.get("units")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    response = requests.get(url)
    data = response.json()
    print(data)

    # Get weather and air quality data from the API response
    # have to check the api agian!
    temperature = data["main"]["temp"]
    humidity = data["data"]["current"]["weather"]["hu"]
    pm25 = data["data"]["current"]["pollution"]["pm2_5"]["conc"]
    uv_index = data["data"]["current"]["weather"]["uv"]
    precipitation = data["data"]["current"]["weather"]["precipitation"]

# info check needed
    if temperature >= 12.8 and temperature <= 25:
        if uv_index <= 5:
            if humidity <= 70:
                if pm25 <= 25:
                    message = "It's a great day for running!"
                else:
                    message = f"Air quality may not be suitable for running. The PM2.5 level is {pm25} µg/m³."
            else:
                message = "Humidity may make it difficult to run."
        else:
            message = f"UV_index may not be suitable for running: {uv_index} "
    else:
        message = "Temperature may not be suitable for running."

    return render_template("index.html", city=city, date=date, message=message)


if __name__ == "__main__":
    app.run(debug=True)
