from django.db import models
from django.contrib.auth.models import User


class Sensor(models.Model):
    # Основная информация
    name = models.CharField(max_length=100, verbose_name='Название датчика')
    description = models.TextField(blank=True, verbose_name='Описание')

    # Идентификация
    mac_address = models.CharField(max_length=17, unique=True, verbose_name='MAC-адрес')
    device_id = models.CharField(max_length=50, unique=True, verbose_name='ID устройства')

    # Координаты
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Долгота'
    )

    # Владелец
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sensors',
        verbose_name='Владелец'
    )

    # Служебные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    last_seen = models.DateTimeField(null=True, blank=True, verbose_name='Последнее соединение')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        unique_together = ('user', 'name')
        ordering = ['-last_seen']

    def __str__(self):
        return f"{self.name} ({self.mac_address})"


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name='Датчик'
    )

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время измерения')

    # Данные (могут быть пустыми, если датчик отсутствует)
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Температура (°C)'
    )

    tds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='TDS (ppm)'
    )

    turbidity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Мутность (NTU)'
    )

    ph = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='pH'
    )

    # Техническая информация
    signal_strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Уровень сигнала (dBm)'
    )
    battery_level = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Заряд батареи (В)'
    )

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.sensor.name} - {self.timestamp}"