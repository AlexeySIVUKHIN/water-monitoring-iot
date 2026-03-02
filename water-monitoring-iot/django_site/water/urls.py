from django.urls import path
from . import views

urlpatterns = [
    path('api/measurement/', views.add_measurement, name='add_measurement'),
    path('', views.sensor_list, name='sensor_list'),
    path('sensor/<int:sensor_id>/', views.sensor_detail, name='sensor_detail'),
    path('sensor/<int:sensor_id>/all/', views.sensor_all_measurements, name='sensor_all'),
    path('sensor/<int:sensor_id>/by-date/', views.sensor_by_date, name='sensor_by_date'),
]