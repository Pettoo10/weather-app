from rest_framework import serializers
from .models import WeatherForecast

class WeatherForecastSerializer(serializers.ModelSerializer):
    """
    Serializer for the WeatherForecast model.

    This serializer converts WeatherForecast model instances to JSON format and vice versa.

    Meta:
        model (WeatherForecast): The model that is being serialized.
        fields (list): The list of fields to be included in the serialization.
    """
    class Meta:
        model = WeatherForecast
        fields = ['id', 'location', 'date', 'temperature', 'humidity', 'wind_speed', 'description', 'forecast_source']
