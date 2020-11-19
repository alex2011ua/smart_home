from django.contrib import admin
from .models import Weather, Logs, Setting, DHT_MQ


@admin.register(DHT_MQ)
class DHT_MQAdmin(admin.ModelAdmin):
    list_display = ('date_t_h',
                    'temp_street',
                    'temp_voda',
                    'humidity_street',
                    'humidity_voda',
                    'temp_room',
                    'temp_gaz',
                    'humidity_gaz',
                    'gaz_MQ4',
                    'gaz_MQ135',

                    )
    list_filter = (
        'date_t_h',
    )
@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('date',
                    'rain',
                    'temp_min',
                    'temp_max',
                    'snow',
                    )
    list_filter = (
        'date',
    )
@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('date_log',
                    'title_log',
                    'description_log',

                    )
    list_filter = (
        'date_log',
    )

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('controller_name',
                    'label',
                    'value',
                    )

