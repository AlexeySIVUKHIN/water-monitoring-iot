from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sensor, Measurement
from .serializers import MeasurementCreateSerializer
from django.db.models import Avg
from datetime import date

@api_view(['POST'])
def add_measurement(request):
    """API для приёма данных от ESP32"""
    serializer = MeasurementCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        sensor = Sensor.objects.get(mac_address=data['mac'])
    except Sensor.DoesNotExist:
        return Response(
            {'error': 'Датчик не зарегистрирован. Сначала добавьте его в админке.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Обновляем время последнего подключения
    sensor.last_seen = timezone.now()

    # Обновляем координаты, если прислали
    if 'latitude' in data and data['latitude'] is not None:
        sensor.latitude = data['latitude']
    if 'longitude' in data and data['longitude'] is not None:
        sensor.longitude = data['longitude']

    sensor.save()

    # Создаём измерение
    measurement_data = {
        'sensor': sensor,
        'signal_strength': data.get('signal'),
        'battery_level': data.get('battery'),
    }

    if 'temperature' in data and data['temperature'] is not None:
        measurement_data['temperature'] = data['temperature']
    if 'tds' in data and data['tds'] is not None:
        measurement_data['tds'] = data['tds']
    if 'turbidity' in data and data['turbidity'] is not None:
        measurement_data['turbidity'] = data['turbidity']
    if 'ph' in data and data['ph'] is not None:
        measurement_data['ph'] = data['ph']

    measurement = Measurement.objects.create(**measurement_data)

    return Response({
        'status': 'ok',
        'id': measurement.id,
        'message': 'Данные приняты'
    }, status=status.HTTP_201_CREATED)


#@login_required
def sensor_list(request):
    """Страница со списком датчиков"""
    #sensors = Sensor.objects.filter(user=request.user, is_active=True)
    sensors = Sensor.objects.filter(is_active=True)
    for sensor in sensors:
        latest = sensor.measurements.order_by('-timestamp').first()
        if latest:
            sensor.last_temp = latest.temperature
            sensor.last_tds = latest.tds
            sensor.last_turbidity = latest.turbidity
            sensor.last_ph = latest.ph
            sensor.last_time = latest.timestamp

    return render(request, 'water/sensor_list.html', {'sensors': sensors})


#@login_required
def sensor_detail(request, sensor_id):
    """Детальная страница датчика"""
    sensor = get_object_or_404(Sensor, id=sensor_id)

    # Средние значения за сегодня
    today = date.today()
    today_measurements = sensor.measurements.filter(
        timestamp__date=today
    )

    avg_temperature = today_measurements.aggregate(Avg('temperature'))['temperature__avg']
    avg_tds = today_measurements.aggregate(Avg('tds'))['tds__avg']
    avg_turbidity = today_measurements.aggregate(Avg('turbidity'))['turbidity__avg']

    # Последние 10 измерений
    recent_measurements = sensor.measurements.order_by('-timestamp')[:10]

    context = {
        'sensor': sensor,
        'recent_measurements': recent_measurements,
        'avg_temperature': avg_temperature,
        'avg_tds': avg_tds,
        'avg_turbidity': avg_turbidity,
    }
    return render(request, 'water/sensor_detail.html', context)


#@login_required
def sensor_all_measurements(request, sensor_id):
    """Страница со всеми измерениями датчика"""
    sensor = get_object_or_404(Sensor, id=sensor_id)

    # Все измерения датчика
    measurements = sensor.measurements.all().order_by('-timestamp')

    # Пагинация (по 50 на странице)
    paginator = Paginator(measurements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Для графика берём последние 100 измерений (по возрастанию времени)
    chart_data = sensor.measurements.all().order_by('timestamp')[:100]

    context = {
        'sensor': sensor,
        'page_obj': page_obj,
        'chart_data': chart_data,
    }
    return render(request, 'water/sensor_all.html', context)

#@login_required
def sensor_by_date(request, sensor_id):
    """Страница с измерениями за конкретную дату"""
    sensor = get_object_or_404(Sensor, id=sensor_id)

    # Получаем дату из GET-параметра
    date_str = request.GET.get('date')
    if not date_str:
        return redirect('sensor_detail', sensor_id=sensor.id)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return redirect('sensor_detail', sensor_id=sensor.id)

    # Фильтруем измерения за эту дату
    measurements = sensor.measurements.filter(
        timestamp__date=selected_date
    ).order_by('timestamp')  # По возрастанию для графика

    # Пагинация
    paginator = Paginator(measurements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sensor': sensor,
        'page_obj': page_obj,
        'chart_data': measurements,  # Все данные за дату для графика
        'selected_date': selected_date,
    }
    return render(request, 'water/sensor_by_date.html', context)