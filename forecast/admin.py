from django.contrib import admin

from .models import WeatherArticle, WeatherForecast

# Register your models here.
admin.site.register(WeatherForecast)
admin.site.register(WeatherArticle)
