from django.contrib import admin

from english.models import Words

from .models import DHT_MQ, Logs, Params, Setting, Weather, Avto


@admin.register(DHT_MQ)
class DHT_MQAdmin(admin.ModelAdmin):
    list_display = (
        "date_t_h",
        "temp_teplica",
        "humidity_teplica",
        "muve_kitchen",
        "temp_street",
        "temp_voda",
        "temp_gaz",
        "gaz_MQ4",
        "gaz_MQ135",
        "humidity_voda",
        "humidity_gaz",
        "myData",
        "ackData",
    )


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "rain",
        "temp_min",
        "temp_max",
        "snow",
    )


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = (
        "date_log",
        "title_log",
        "description_log",
    )
    list_filter = (
        "date_log",
        "status",
    )


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = (
        "controller_name",
        "label",
        "value",
        "date",
    )


@admin.register(Params)
class ParamsAdmin(admin.ModelAdmin):
    list_display = (
        "date_t_h",
        "poliv",
        "min_temp_teplica",
        "max_temp_teplica",
        "ping",
        "download",
        "upload",
    )
    list_filter = (
        "date_t_h",
        "poliv",
        "min_temp_teplica",
        "max_temp_teplica",
    )

@admin.register(Avto)
class AvtoAdmin(admin.ModelAdmin):
    list_display = ("pk", "car_id", "link_car")
