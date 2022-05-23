from secrets import choice
from django import forms
from django.db import models
import requests

# Create your models here.
class Inventory(models.Model):
    CITIES = (
        ('New York','New York'),
        ('Atlanta', 'Atlanta'),
        ('Hong Kong', 'Hong Kong'),
        ('Los Angeles', 'Los Angeles'),
        ('Buenos Aires', 'Buenos Aires'),
    )
    name =  models.CharField(max_length=200, blank=False)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    per_value = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=False, blank=False)
    storage_city = models.CharField(max_length=40, choices=CITIES, blank=False)
    
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_created',)
    
    def total_inventory_value(self):
        return self.quantity * self.per_value

    def get_current_weather(self):
        openweather_api_key = '06d437156d3cb2f8c0f7d16dcbc93d4a'
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(self.storage_city, openweather_api_key)
        city_weather = requests.get(url.format(self.storage_city)).json()

        if city_weather['cod'] == 401:
            description = "Error 401"
        else:
            description = city_weather['weather'][0]['description']
            

        return description

    def __str__(self):
        return "{}".format(self.name)

