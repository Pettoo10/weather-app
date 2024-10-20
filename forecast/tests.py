import os
from unittest.mock import patch
import requests
from django.test import TestCase
from rest_framework import status

from forecast.models import WeatherForecast

base_url= os.getenv('BASE_URL')

class WeatherApiTests(TestCase):
    def setUp(self):
        """Set up test data for the API tests."""
        WeatherForecast.objects.create(
            location='Bratislava',
            date='2024-10-18T12:00:00Z',
            temperature=15,
            humidity=90.0,
            wind_speed=10.0,
            description='clear sky',
        )
        WeatherForecast.objects.create(
            location='Bratislava',
            date='2024-10-17T20:00:00Z',
            temperature=12,
            humidity=85.0,
            wind_speed=15.0,
            description='overcast',
        )

    @patch('requests.get')
    def test_get_current_weather(self, mock_get):
        """
        Test the current weather endpoint.

        This test checks if the 'get_current_weather' endpoint returns the expected
        data for the location 'Bratislava'.

        Assertions:
            - The response status code should be 200 OK.
            - The response data should include 'location'.
            - The response data should include 'date'.
            - The response data should include 'temperature'.
            - The response data should include 'humidity'.
            - The response data should include 'wind_speed'.
            - The response data should include 'description'.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'location': 'Bratislava',
            'date': '2024-10-18',
            'temperature': 15,
            'humidity': 90.0,
            'wind_speed': 10.0,
            'description': 'clear sky',

        }
        response = requests.get(f"{base_url}/forecast/current/Bratislava")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('location', response.json())
        self.assertIn('date', response.json())
        self.assertIn('temperature', response.json())
        self.assertIn('humidity', response.json())
        self.assertIn('wind_speed', response.json())
        self.assertIn('description', response.json())


    @patch('requests.get')
    def test_get_historical_weather(self, mock_get):
        """
        Test the historical weather endpoint.

        This test checks if the 'get_historical_weather' endpoint returns the expected
        data for the location 'Bratislava'.

        Assertions:
            - The response status code should be 200 OK.
            - Each item in the response data should include 'id'.
            - Each item in the response data should include 'location'.
            - Each item in the response data should include 'date'.
            - Each item in the response data should include 'temperature'.
            - Each item in the response data should include 'humidity'.
            - Each item in the response data should include 'wind_speed'.
            - Each item in the response data should include 'description'.
            - Each item in the response data should include 'forecast_source'.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'location': 'Bratislava',
            'date': '2024-10-18',
            'temperature': 15,
            'humidity': 90.0,
            'wind_speed': 10.0,
            'description': 'clear sky',
            'forecast_source': 'OpenWeatherMap'
        }

        response = requests.get(f"{base_url}/forecast/current/Bratislava")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.json())
        self.assertIn('location', response.json())
        self.assertIn('date', response.json())
        self.assertIn('temperature', response.json())
        self.assertIn('humidity', response.json())
        self.assertIn('wind_speed', response.json())
        self.assertIn('description', response.json())
        self.assertIn('forecast_source', response.json())


    @patch('requests.post')
    def test_generate_weather_article(self, mock_post):
        """
        Test the generate weather article endpoint.

        This test checks if the 'generate_weather_article' endpoint returns the expected
        data for the given payload.

        Payload:
            - location (str): The location for which the weather article is generated.
            - style (str): The style of the article, either 'factual' or 'tabloid'.
            - language (str): The language of the article, either 'en' for English or 'sk' for Slovak.

        Assertions:
            - The response status code should be 200 OK.
            - The response data should include 'title'.
            - The response data should include 'preamble'.
            - The response data should include 'body'.
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "title": "Weather in Bratislava on 2024-10-18",
            "preamble": "Current weather in Bratislava is clear sky with a temperature of 15°C.",
            "body": "Today in Bratislava, the weather is warm and sunny..."
        }

        payload = {
            "location": "Bratislava",
            "style": "factual",
            "language": "en"
        }
        response = requests.post(f"{base_url}/forecast/article", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.json())
        self.assertIn('preamble', response.json())
        self.assertIn('body', response.json())
