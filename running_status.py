import requests

# Define the location and date for the weather and air quality data
location = "New York City"
date = "2022-10-01"

# Retrieve the weather data from the AccuWeather API
weather_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{date}?apikey=<YOUR_API_KEY>&q={location}"
weather_response = requests.get(weather_url)
weather_data = weather_response.json()
temperature = weather_data["Temperature"]["Maximum"]["Value"]
humidity = weather_data["Day"]["RelativeHumidity"]

# Retrieve the air quality data from the BreezoMeter API
airquality_url = f"https://api.breezometer.com/air-quality/v2/current-conditions?lat=<LATITUDE>&lon=<LONGITUDE>&key=<YOUR_API_KEY>"
airquality_response = requests.get(airquality_url)
airquality_data = airquality_response.json()
pollutants = airquality_data["data"]["pollutants"]

# Determine whether it is suitable for running based on the data
if temperature >= 55 and temperature <= 65:
    if humidity <= 70:
        if pollutants["no2"]["concentration"]["value"] <= 50:
            print("It's a great day for running!")
        else:
            print("Air quality may not be suitable for running.")
    else:
        print("Humidity may make it difficult to run.")
else:
    print("Temperature may not be suitable for running.")

# Use IQair as API

# test
