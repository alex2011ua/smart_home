from django.db import models


# Create your models here.
class Setting(models.Model):
    controller_name = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=100)
    value = models.IntegerField(default=20)


class Weather(models.Model):
    date = models.DateField(unique = True)
    rain = models.IntegerField(default=0)
    temp_min = models.IntegerField(default=0)
    temp_max = models.IntegerField(default=0)
    snow = models.IntegerField(default=0)


class Logs(models.Model):
    date_log = models.DateTimeField()
    title_log = models.CharField(max_length=50)
    description_log = models.CharField(max_length=150)


class DHT_MQ(models.Model):
    date_t_h = models.DateTimeField()

    temp_street = models.FloatField(null=True)
    humidity_street = models.FloatField(null=True)

    temp_voda = models.FloatField(null=True)
    humidity_voda = models.FloatField(null=True)

    temp_gaz = models.FloatField(null=True)
    humidity_gaz = models.FloatField(null=True)

    temp_teplica = models.FloatField(null=True)
    humidity_teplica = models.FloatField(null=True)

    temp_room = models.IntegerField(null=True)
    humidity_room = models.IntegerField(null=True)

    gaz_MQ4 = models.IntegerField(null=True)
    gaz_MQ135 = models.IntegerField(null=True)

