from rest_framework import serializers
from .models import Measurement


class MeasurementCreateSerializer(serializers.Serializer):
    # Обязательные поля
    mac = serializers.CharField(max_length=17)

    # Данные (все могут отсутствовать)
    temperature = serializers.FloatField(required=False, allow_null=True)
    tds = serializers.IntegerField(required=False, allow_null=True)
    turbidity = serializers.FloatField(required=False, allow_null=True)
    ph = serializers.FloatField(required=False, allow_null=True)

    # Координаты
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)

    # Технические
    signal = serializers.IntegerField(required=False, allow_null=True)
    battery = serializers.FloatField(required=False, allow_null=True)