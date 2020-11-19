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
        'gaz_MQ4',
        'gaz_MQ135',
        'temp_street',
        'temp_room',

    )

#admin.site.register(Weather)
#admin.site.register(Logs)
#admin.site.register(DHT_MQAdmin)
#admin.site.register(Setting)