from django.db import models


# Create your models here.
class Setting(models.Model):
    controller_name = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=100)
    value = models.IntegerField(default=20)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.label)


class Weather(models.Model):
    date = models.DateField(unique=True)
    rain = models.FloatField(default=0)
    temp_min = models.FloatField(default=0)
    temp_max = models.FloatField(default=0)
    snow = models.FloatField(default=0)

    def __str__(self):
        return str(self.date)


class Logs(models.Model):
    date_log = models.DateTimeField()
    status = models.CharField(max_length=50, null=True, blank=True)
    title_log = models.CharField(max_length=50)
    description_log = models.CharField(max_length=150)

    def __str__(self):
        return str(self.date_log)


class DHT_MQ(models.Model):
    date_t_h = models.DateTimeField()

    temp_street = models.FloatField(null=True, blank=True)
    humidity_street = models.FloatField(null=True, blank=True)

    temp_voda = models.FloatField(null=True, blank=True)
    humidity_voda = models.FloatField(null=True, blank=True)

    temp_gaz = models.FloatField(null=True, blank=True)
    humidity_gaz = models.FloatField(null=True, blank=True)

    temp_teplica = models.FloatField(null=True, blank=True)
    humidity_teplica = models.FloatField(null=True, blank=True)

    temp_room = models.FloatField(null=True, blank=True)
    humidity_room = models.IntegerField(null=True, blank=True)

    gaz_MQ4 = models.IntegerField(null=True, blank=True)
    gaz_MQ135 = models.IntegerField(null=True, blank=True)

    muve_kitchen = models.IntegerField(null=True, blank=True)
    myData = models.CharField(max_length=50, null=True, blank=True)
    ackData = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.date_t_h)


class Params(models.Model):
    date_t_h = models.DateTimeField()

    poliv = models.IntegerField(null=True, blank=True)
    min_temp_teplica = models.IntegerField(null=True, blank=True)
    max_temp_teplica = models.IntegerField(null=True, blank=True)
    ping = models.FloatField(null=True, blank=True)
    download = models.FloatField(null=True, blank=True)
    upload = models.FloatField(null=True, blank=True)


class Message(models.Model):
    date_message = models.DateTimeField()
    controller_name = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    value_int = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    state = models.BooleanField(default=False)


class Avto(models.Model):
    car_id = models.IntegerField(unique=True)
    link_car = models.CharField(max_length=150, blank=True, null=True)
