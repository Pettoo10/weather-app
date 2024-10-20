from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class WeatherForecast(models.Model):
    """
    Model representing a weather forecast.

    Attributes:
        location (str): The location for which the forecast is made.
        date (datetime): The date and time of the forecast.
        temperature (float): The temperature in degrees Celsius.
        humidity (float, optional): The humidity percentage.
        wind_speed (float, optional): The wind speed in kilometers per hour.
        description (str): A description of the weather.
        forecast_source (str): The source of the forecast.
        created_at (datetime): The date and time when the forecast was created.
        updated_at (datetime): The date and time when the forecast was last updated.
    """
    location = models.CharField(max_length=255, verbose_name=_("Location"))
    date = models.DateTimeField(verbose_name=_("Date of forecast"))
    temperature = models.FloatField(verbose_name=_("Temperature (°C)"))
    humidity = models.FloatField(verbose_name=_("Humidity (%)"), null=True, blank=True)
    wind_speed = models.FloatField(verbose_name=_("Wind Speed (km/h)"), null=True, blank=True)
    description = models.CharField(max_length=255, verbose_name=_("Weather description"))
    forecast_source = models.CharField(max_length=255, verbose_name=_("Forecast source"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        """
        Meta options for the WeatherForecast model.

        Attributes:
            verbose_name (str): The singular name for the model.
            verbose_name_plural (str): The plural name for the model.
            ordering (list): The default ordering for the model.
            indexes (list): The indexes for the model.
        """
        verbose_name = _("Weather Forecast")
        verbose_name_plural = _("Weather Forecasts")
        ordering = ['-date']  # Show the latest forecast first
        indexes = [
            models.Index(fields=['location']),
        ]

    def __str__(self):
        """
        String representation of the WeatherForecast model.

        Returns:
            str: A string representing the location and date of the forecast.
        """
        return f"{self.location} - {self.date}"


class WeatherArticle(models.Model):
    """
    Model representing a weather article.

    Attributes:
        forecast (ForeignKey): The weather forecast associated with the article.
        style (str): The style of the article, either 'factual' or 'tabloid'.
        language (str): The language of the article, either 'en' for English or 'sk' for Slovak.
        title (str): The title of the article.
        preamble (str): A short introduction to the article.
        body (str): The main content of the article.
        created_at (datetime): The date and time when the article was created.
    """
    FACTUAL = 'factual'
    TABLOID = 'tabloid'

    STYLE_CHOICES = [
        (FACTUAL, _("Factual")),
        (TABLOID, _("Tabloid")),
    ]

    ENGLISH = 'en'
    SLOVAK = 'sk'

    LANGUAGE_CHOICES = [
        (ENGLISH, _("English")),
        (SLOVAK, _("Slovak")),
    ]

    forecast = models.ForeignKey(WeatherForecast, on_delete=models.CASCADE, related_name='articles', verbose_name=_("Forecast"))
    style = models.CharField(max_length=50, choices=STYLE_CHOICES, default=FACTUAL, verbose_name=_("Style"))
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=ENGLISH, verbose_name=_("Language"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    preamble = models.TextField(verbose_name=_("Preamble"))  # Short introduction to the article
    body = models.TextField(verbose_name=_("Body"))  # Main content of the article
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        """
        Meta options for the WeatherArticle model.

        Attributes:
            verbose_name (str): The singular name for the model.
            verbose_name_plural (str): The plural name for the model.
            ordering (list): The default ordering for the model.
        """
        verbose_name = _("Weather Article")
        verbose_name_plural = _("Weather Articles")
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of the WeatherArticle model.

        Returns:
            str: A string representing the title and language of the article.
        """
        return f"{self.title} ({self.language})"
