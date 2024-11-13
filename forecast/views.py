import os
from datetime import datetime

import requests
from deep_translator import GoogleTranslator
from django.utils import timezone
from dotenv import load_dotenv
from openai import OpenAI
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WeatherForecast
from .serializers import WeatherForecastSerializer

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")


@api_view(["GET"])
def get_current_weather(request, location):
    """
    Retrieves the current weather forecast for the specified location from the OpenWeatherMap API
    and saves the data to the database for historical viewing.

    Args:
        request (Request): The HTTP request object.
        location (str): The location for which to retrieve the weather forecast.

    Returns:
        Response: A Response object containing the current weather data or an error message.
    """
    try:
        # Fetch weather forecast from OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return Response(
                {"error": "Unable to fetch weather data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prepare data for saving
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data.get("main", {}).get("humidity")
        wind_speed = data.get("wind", {}).get("speed")

        # Use timezone.now() to get an aware datetime object
        date = timezone.now()

        # Save data to the database if it does not already exist
        if not WeatherForecast.objects.filter(location=location, date=date).exists():
            WeatherForecast.objects.create(
                location=location,
                date=date,
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
                description=description,
                forecast_source="OpenWeatherMap",
            )

        # Return the current forecast
        return Response(
            {
                "location": location,
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "description": description,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_historical_weather(request, location):
    """
    Retrieves historical weather forecasts from the database for the specified location.
    Can be filtered by date using the start_date and end_date parameters.

    Args:
        request (Request): HTTP request object containing optional start_date and end_date parameters.
        location (str): The location for which to retrieve historical weather data.

    Returns:
        Response: A Response object containing serialized historical weather data or an error message.
    """
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    try:
        # Filter by dates if provided
        forecasts = WeatherForecast.objects.filter(location=location)
        if start_date and end_date:
            forecasts = forecasts.filter(date__range=[start_date, end_date])

        # Serialize the results
        serializer = WeatherForecastSerializer(forecasts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def generate_weather_article(request):
    """
    Generates a weather article based on data from the OpenWeatherMap API and GPT.
    The user can choose the style: factual or tabloid, and the language: Slovak or English.

    Args:
        request (Request): The HTTP request object containing the location, style, and language.

    Returns:
        Response: A Response object containing the generated weather article or an error message.
    """
    try:
        location = request.data.get("location")
        style = request.data.get("style", "factual")  # Select 'factual' a 'tabloid'
        language = request.data.get("language", "en")  # Select 'en' a 'sk'

        # Fetch weather forecast from OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code != 200:
            return Response(
                {"error": "Unable to fetch weather data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prepare data for GPT
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        location_name = weather_data["name"]
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Create prompt for GPT
        if style == "factual":
            prompt = (
                f"Write a factual weather report for {location_name} on {current_date}. "
                f"The weather is {description} with a temperature of {temperature}°C."
            )
        elif style == "tabloid":
            prompt = (
                f"Write a dramatic and entertaining weather article for {location_name} on {current_date}. "
                f"The weather is {description} and the temperature is {temperature}°C. Make it fun and sensational."
            )

        # Call OpenAI API to generate the article using the client
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
        )

        # The response returns an object accessible via attributes
        title_text = f"Weather in {location_name} on {current_date}"
        preamble_text = f"Current weather in {location_name} is {description} with a temperature of {temperature}°C."
        article_text = chat_completion.choices[0].message.content.strip()

        # Translate the article (if the chosen language is not English)
        if language != "en":
            title_text = translate_text(title_text, language)
            preamble_text = translate_text(preamble_text, language)
            article_text = translate_text(article_text, language)

        # Return the generated article
        return Response(
            {"title": title_text, "preamble": preamble_text, "body": article_text},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def translate_text(text, target_language):
    """
    Translates text into the target language using the deep_translator library.

    Args:
        text (str): The text to be translated.
        target_language (str): The target language code (e.g., 'en' for English, 'sk' for Slovak).

    Returns:
        str: The translated text. If translation fails, returns the original text.
    """
    try:
        # Perform translation using GoogleTranslator
        translation = GoogleTranslator(source="auto", target=target_language).translate(
            text
        )
        return translation
    except Exception as e:

        print(f"Translation failed: {e}")
        return {
            "error": "Language not supported",
            "original_text": text,
        }  # Return original text if translation fails
