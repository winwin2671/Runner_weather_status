import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/running-suitability", methods=["POST"])
def running_suitability():
    location = request.form.get("location")
    date = request.form.get("date")
    api_key = "<YOUR_IQAIR_API_KEY>"

    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    response = requests.get(url)
    data = response.json()

    # Get weather and air quality data from the API response
    temperature = data["data"]["current"]["weather"]["tp"]
    humidity = data["data"]["current"]["weather"]["hu"]
    pm25 = data["data"]["current"]["pollution"]["pm2_5"]["conc"]
    uv_index = data["data"]["current"]["weather"]["uv"]

# info check needed
    if temperature >= 12.8 and temperature <= 25:
        if humidity <= 70:
            if pm25 <= 25:
                message = f"It's a great day for running! The PM2.5 level is {pm25} µg/m³."
            else:
                message = f"Air quality may not be suitable for running. The PM2.5 level is {pm25} µg/m³."
        else:
            message = "Humidity may make it difficult to run."
    else:
        message = "Temperature may not be suitable for running."

    return render_template("index.html", location=location, date=date, message=message)


if __name__ == "__main__":
    app.run(debug=True)
