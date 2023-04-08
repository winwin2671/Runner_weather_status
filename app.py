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
    no2 = data["data"]["current"]["pollution"]["no2"]["conc"]

    if temperature >= 55 and temperature <= 65:
        if humidity <= 70:
            if no2 <= 50:
                message = "It's a great day for running!"
            else:
                message = "Air quality may not be suitable for running."
        else:
            message = "Humidity may make it difficult to run."
    else:
        message = "Temperature may not be suitable for running."

    return render_template("running_suitability.html", location=location, date=date, message=message)


if __name__ == "__main__":
    app.run(debug=True)
