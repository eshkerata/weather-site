from flask import Flask, render_template_string
import requests

app = Flask(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 55.75 
LONGITUDE = 37.62
PARAMETERS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "temperature_2m,relative_humidity_2m,windspeed_10m,wind_direction_10m,pressure_msl",
    "timezone": "Europe/Moscow"
}

def wind_direction_to_string(degree):
    if degree >= 337.5 or degree < 22.5:
        return "N"
    elif 22.5 <= degree < 67.5:
        return "NE"
    elif 67.5 <= degree < 112.5:
        return "E"
    elif 112.5 <= degree < 157.5:
        return "SE"
    elif 157.5 <= degree < 202.5:
        return "S"
    elif 202.5 <= degree < 247.5:
        return "SW"
    elif 247.5 <= degree < 292.5:
        return "W"
    elif 292.5 <= degree < 337.5:
        return "NW"

@app.route('/')
def weather():
    response = requests.get(API_URL, params=PARAMETERS)
    weather_data = response.json()

    hour_data = weather_data['hourly']['time'][12]
    temperature = weather_data['hourly']['temperature_2m'][12]
    humidity = weather_data['hourly']['relative_humidity_2m'][12]
    windspeed = weather_data['hourly']['windspeed_10m'][12]
    wind_direction = wind_direction_to_string(weather_data['hourly']['wind_direction_10m'][12])
    pressure = weather_data['hourly']['pressure_msl'][12]

    weather_card = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <div class="weather-card">
            <div class="weather-date">
                Четверг 08
            </div>
            <div class="weather-info">
                <div class="weather-item">
                    <img src="https://img.icons8.com/?size=100&id=q08BODJHMGe1&format=png&color=000000" alt="Thermometer"/>
                    <span>{temperature}°</span>
                </div>
                <div class="weather-item">
                    <img src="https://img.icons8.com/?size=100&id=5ZAexOoJNxiy&format=png&color=000000" alt="Wind">
                    <span>{wind_direction} {windspeed}м/с</span>
                </div>
                <div class="weather-item">
                    <img src="https://img.icons8.com/?size=100&id=xX3hAGmqS7LE&format=png&color=000000" alt="Humidity">
                    <span>{humidity}%</span>
                </div>
                <div class="weather-item">
                    <img src="https://img.icons8.com/?size=100&id=heJXkbP4i1Pe&format=png&color=000000" alt="Pressure">
                    <span>{pressure} мм рт.ст.</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    weather_card += """
        <style>
        .weather-card {
            width: auto;
            background-color: white;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            font-family: Arial, sans-serif;
            text-align: center;
        }

        .weather-date {
            background-color: #ff3b3b;
            color: white;
            padding: 25px;
            font-weight: bold;
            font-style: italic;
            font-size: 36px;
        }

        .weather-info {
            padding: 10px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-gap: 10px;
        }

        .weather-info span {
            font-size: 24px;
        }

        .weather-item {
            background-color: rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 10px;
            font-size: 12px;
            border-radius: 10px;
        }

        .weather-item img {
            width: 50px;
            height: 50px;
            margin-bottom: 5px;
        }

        @media (min-width: 720px) {
            .weather-card {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }
        }
        </style>
        """

    return render_template_string(weather_card)

if __name__ == '__main__':
    app.run(debug=True)
