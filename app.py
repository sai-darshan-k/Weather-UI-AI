import os
from flask import Flask, render_template, jsonify, request
import requests  # For weather API integration
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Route for the home page
@app.route('/')
def index():
    return render_template('weather.html')

# Route to handle weather data requests
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'default_city')
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        logging.error("Weather API key not set in environment variables.")
        return jsonify({'error': 'API key is missing'}), 500

    # Call the weather API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        weather_data = response.json()

        # Parse essential weather information
        result = {
            'city': weather_data.get('name', 'Unknown location'),
            'temperature': weather_data['main'].get('temp', 'N/A'),
            'description': weather_data['weather'][0].get('description', 'N/A'),
            'humidity': weather_data['main'].get('humidity', 'N/A')
        }
        logging.info(f"Weather data fetched for {city}: {result}")
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {str(e)}")
        return jsonify({'error': 'Error fetching weather data'}), 500

if __name__ == '__main__':
    app.run(debug=False)
