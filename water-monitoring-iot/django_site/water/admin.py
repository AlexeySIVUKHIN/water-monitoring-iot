from django.contrib import admin
from .models import Sensor, Measurement

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['name', 'mac_address', 'user', 'last_seen', 'latitude', 'longitude']
    list_filter = ['user', 'is_active']
    search_fields = ['name', 'mac_address', 'device_id']

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'timestamp', 'temperature', 'tds', 'turbidity', 'ph']
    list_filter = ['sensor', 'timestamp']
    date_hierarchy = 'timestamp'