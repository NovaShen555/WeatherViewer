from django.db import models

class CityInfo(models.Model):
    cityname = models.CharField(max_length=10)
    cityurl = models.URLField()
    WeatherUpdateDate = models.DateField()
    
class UpdateTime(models.Model):
    timeid = models.CharField(max_length=50)
    deltatime = models.DateField()

class bulletinData(models.Model):
    tid = models.IntegerField()
    title = models.CharField(max_length=50)
    content = models.TextField()

class weatherData(models.Model):
    city_id = models.IntegerField()
    upper_content = models.TextField()
    lower_content = models.TextField()
    update_date = models.DateField()
