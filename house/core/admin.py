from django.contrib import admin
from .models import Weather, Logs, Setting, DHT_MQ


@admin.register(DHT_MQ)
class DHT_MQAdmin(admin.ModelAdmin):
    list_display = ('date_t_h',
                    'temp_street',
                    'humidity_street',
                    'temp_voda',
                    'humidity_voda',
                    'temp_gaz',
                    'humidity_gaz',
                    'gaz_MQ4',
                    'gaz_MQ135',
                    )


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('date',
                    'rain',
                    'temp_min',
                    'temp_max',
                    'snow',
                    )


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('date_log',
                    'title_log',
                    'description_log',

                    )


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('controller_name',
                    'label',
                    'value',
                    )

