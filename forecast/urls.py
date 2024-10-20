from django.urls import path
from . import views

urlpatterns = [
    path('current/<str:location>/', views.get_current_weather, name='get_current_weather'),
    path('historical/<str:location>/', views.get_historical_weather, name='get_historical_weather'),
    path('article/', views.generate_weather_article, name='generate_weather_article'),
]