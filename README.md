# Weather API Documentation

## Overview

Weather API is a Django-based application that provides weather forecasts and historical weather data for selected locations. The API supports multiple languages and styles of reporting.

## Base URL

The base public URL for the API is:

http://13.48.225.1:8000/api/


## Endpoints

### 1. Get Current Weather Forecast

**Endpoint:**

GET /forecast/current/{location}

**Description:**

Retrieves the current weather forecast for the specified location.

**Path Parameters:**

- `location` (string): The name of the city or location (e.g., `Bratislava`).

**Response:**

```json
{
    "location": "Bratislava",
    "date": "2024-10-20 16:50:45",
    "temperature": 12.47,
    "humidity": 63,
    "wind_speed": 3.92,
    "description": "broken clouds"
}
```

### 2. Get Historical Weather Forecast

**Endpoint:**

GET /forecast/historical/{location}

**Description:**

Retrieves historical weather data for the specified location.

**Path Parameters:**

- `location` (string): The name of the city or location (e.g., `Bratislava`).

**Response:**

```json
[
    {
        "id": 2,
        "location": "Bratislava",
        "date": "2024-10-20T16:50:45.318631Z",
        "temperature": 12.47,
        "humidity": 63.0,
        "wind_speed": 3.92,
        "description": "broken clouds",
        "forecast_source": "OpenWeatherMap"
    }
]
```

### 3. Generate Weather Article

**Endpoint:**

POST /forecast/article

**Description:**

Generates a weather article based on the current weather forecast and allows for selection of style and language.

**Request Body:**

```json
{
    "location": "Bratislava",
    "style": "factual", // or "tabloid"
    "language": "en"    // or "sk"
}

```

**Response:**

```json
{
    "title": "Weather in Bratislava on 2024-10-20",
    "preamble": "Current weather in Bratislava is clear sky with a temperature of 11.94°C.",
    "body": "On October 20, 2024, Bratislava is experiencing clear skies with a temperature of 11.94°C..."
}
```

## Error Handling
The API may return the following error responses:

- **400 Bad Request**: The request is invalid or missing required parameters.
```json
{
    "error": "Unable to fetch weather data"
}

```

- **404 Not Found**: The requested resource was not found.
```json
{
    "error": "Location not found"
}
```

- **500 Internal Server Error**: An unexpected error occurred on the server.
```json
{
    "error": "Internal server error"
}
```

- **Translation failed**: The translation failed due to some reason.
```json
{
    "error": "Language not supported",
    "original_text": text,
}
```
Return original text if translation fails

# Development Environment Setup

## Overview

This section provides instructions on how to set up the development environment for the Weather API application. The application is built using Django and requires Python and Docker for local development.

## Prerequisites

Before setting up the development environment, ensure that you have the following installed:

- [Python 3.11](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/downloads)

## Setting Up the Development Environment

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/pettoo10/weather-app.git
cd weather-app
```

### Set Up a Virtual Environment (Optional)

While not strictly necessary if you use Docker, it's a good practice to use a virtual environment for Python development:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
If you're not using Docker, install the required Python dependencies:
    
```bash
pip install -r requirements.txt
```

### Step 4: Create a .env File
Create a .env file in the project root directory to store your environment variables. Here’s a sample structure:
```env
OPENAI_API_KEY=your_openai_api_key
WEATHER_API_KEY=your_openweather_api_key
BASE_URL=http://13.48.255.1:8000/api
```

### Step 5: Run Migrations
If you are running the application for the first time, you'll need to run the database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Run the Development Server
If you are running the application locally (not in Docker), start the development server:
```bash
python manage.py runserver
```

### Step 7: Using Docker (Alternative)
If you prefer to run the application using Docker:
```bash
# Build the Docker image
docker build -t weather-app .

# Run the Docker container
docker run -d -p 8000:8000 --name weather-app \
    -e OPENAI_API_KEY=your_openai_api_key_here \
    -e WEATHER_API_KEY=your_weather_api_key_here \
    weather-app:latest
```

### Step 8: Access the API
Once the server is running, you can access the API at:
```bash
http://localhost:8000/api/
```

### Step 9. Run Tests
To run the tests, use the following command:
```bash
python manage.py test forecast.tests
```