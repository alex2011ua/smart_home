from django.db import models


# Create your models here.
class Setting(models.Model):
    controller_name = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=100)
    value = models.IntegerField(default=20)


class WeatherRain(models.Model):
    date = models.DateField(unique = True)
    rain = models.IntegerField(default=0)
    temp_min = models.IntegerField(default=0)
    temp_max = models.IntegerField(default=0)
    snow = models.IntegerField(default=0)

class Logs(models.Model):
    date_log = models.DateTimeField()
    title_log = models.CharField(max_length=50)
    description_log = models.CharField(max_length=150)


class Temp1(models.Model):
    date_temp = models.DateTimeField()
    temp = models.IntegerField()
    humidity = models.IntegerField()

class Temp_out(models.Model):
    date_temp = models.DateTimeField()
    temp = models.IntegerField()
    humidity = models.IntegerField()
