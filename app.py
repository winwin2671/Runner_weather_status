import requests
from flask import Flask, render_template, request
import config

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/running-suitability", methods=["POST"])
def running_suitability():
    location = request.form.get("location")
    date = request.form.get("date")

    url = f"https://api.airvisual.com/v2/nearest_city?key={config.api_key}"
    response = requests.get(url)
    data = response.json()

    # Get weather and air quality data from the API response
    temperature = data["data"]["current"]["weather"]["tp"]
    humidity = data["data"]["current"]["weather"]["hu"]
    pm25 = data["data"]["current"]["pollution"]["pm2_5"]["conc"]
    uv_index = data["data"]["current"]["weather"]["uv"]
    precipitation = data["data"]["current"]["weather"]["precipitation"]

# info check needed
    if temperature >= 12.8 and temperature <= 25:
        if uv_index <= 5:
            if humidity <= 70:
                if pm25 <= 25:
                    message = f"It's a great day for running! The PM2.5 level is {pm25} µg/m³."
                else:
                    message = f"Air quality may not be suitable for running. The PM2.5 level is {pm25} µg/m³."
            else:
                message = "Humidity may make it difficult to run."
        else:
            message = f"UV_index may not be suitable for running: {uv_index} "
    else:
        message = "Temperature may not be suitable for running."

    return render_template("index.html", location=location, date=date, message=message)


if __name__ == "__main__":
    app.run(debug=True)
