# IoT Water Quality Monitoring System

A complete, production-ready IoT system for real-time water quality monitoring. This project combines an ESP32-based sensor station with a Django web application to collect, store, and visualize water parameters from rivers, lakes, or any water body.

Website: http://publicwater.ru
Admin Panel: http://publicwater.ru/admin

## System Overview

The system consists of two main components:

1. ESP32 Sensor Station
- Measures temperature, TDS (total dissolved solids), and turbidity
- Sends data via Wi-Fi to Django server every 5 minutes
- Energy-efficient design with controlled sensor power

2. Django Web Application
- REST API endpoint for data ingestion (/api/measurement/)
- SQLite/MySQL database for storing measurements
- Interactive dashboards with charts and filters
- Public access to all data (admin-only for sensor management)

## Key Features

Hardware Features:
- Automatic TDS sensor power control – GPIO-controlled to prevent electrolysis (extends sensor life)
- Temperature compensation – Accurate TDS readings corrected for temperature
- Deep sleep mode – Configurable intervals for battery-powered operation
- GPS coordinates – Each measurement can include location data

Web Application Features:
- Public access – No login required to view water quality data
- Real-time charts – Interactive graphs powered by Chart.js
- Historical data – Filter by date, view all measurements with pagination
- Daily averages – Automatic calculation of average values per day
- Mobile responsive – Works on phones, tablets, and desktops
- REST API – Simple JSON endpoint for IoT devices

## Hardware Requirements

ESP32 Development Board (ESP32-WROOM-32, DevKitC) - Main controller with Wi-Fi
TDS Sensor (Analog 0-1000ppm) - Measures total dissolved solids
Turbidity Sensor (Analog output) - Measures water clarity
Temperature Sensor (NTC thermistor 10k? or DS18B20) - Measures water temperature
Resistors (10k? for NTC, 4.7k? for DS18B20) - Pull-up / voltage divider
Power Supply (5V USB or 5-12V battery pack) - Powers the system

### Pin Configuration

TDS VCC - GPIO17 - Digital output (power control)
TDS Signal - GPIO36 (VP) - Analog input
Turbidity Signal - GPIO34 - Analog input
NTC Signal - GPIO39 (VN) - Analog input (with 10k? to GND)
DS18B20 Data - GPIO4 - Digital (with 4.7k? pull-up)
Common GND - Any GND - All sensors

## Installation

Prerequisites:
- Python 3.8 or higher
- pip and virtualenv
- Git
- Arduino IDE with ESP32 board support

### 1. Clone the Repository

git clone https://github.com/AlexeySIVUKHIN/water-monitoring-iot.git
cd water-monitoring-iot

### 2. Django Web Application Setup

cd django_site
python -m venv venv
source venv/bin/activate (On Windows: venv\Scripts\activate)
pip install -r ../requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000

Access the site at http://127.0.0.1:8000

### 3. ESP32 Firmware Upload

Install Arduino IDE libraries:
- ArduinoJson (by Benoit Blanchon)
- OneWire (by Paul Stoffregen)
- DallasTemperature (by Miles Burton)

Configure Wi-Fi credentials:
- Copy esp32_firmware/secrets_example.h to secrets.h
- Edit secrets.h with your Wi-Fi SSID and password

Upload to ESP32:
- Open esp32_firmware/WATERapi.ino in Arduino IDE
- Select board: ESP32 Dev Module
- Select correct COM port
- Click Upload

## API Reference

POST /api/measurement/

Request Headers:
Content-Type: application/json

Request Body:
{
    "mac": "94:51:dc:30:44:1c",
    "temperature": 18.5,
    "tds": 245,
    "turbidity": 3.29,
    "signal": -67,
    "latitude": 55.755826,
    "longitude": 37.617300
}

Response (201 Created):
{
    "status": "ok",
    "id": 123,
    "message": "Данные приняты"
}

## Project Structure

water-monitoring-iot/
+-- django_site/
¦   +-- manage.py
¦   +-- water_monitor/
¦   ¦   +-- settings.py
¦   ¦   +-- urls.py
¦   ¦   L-- wsgi.py
¦   L-- water/
¦       +-- models.py
¦       +-- views.py
¦       +-- serializers.py
¦       +-- urls.py
¦       L-- templates/
¦           L-- water/
¦               +-- base.html
¦               +-- sensor_list.html
¦               +-- sensor_detail.html
¦               +-- sensor_all.html
¦               L-- sensor_by_date.html
¦
+-- esp32_firmware/
¦   +-- WATERapi.ino
¦   L-- secrets_example.h
¦
+-- requirements.txt
+-- .gitignore
+-- README.md
L-- LICENSE

## Configuration

Django Settings (django_site/water_monitor/settings.py):

For development:
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

For production:
DEBUG = False
ALLOWED_HOSTS = ['publicwater.ru', 'www.publicwater.ru']

ESP32 Settings (esp32_firmware/WATERapi.ino):

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
String serverName = "http://publicwater.ru/api/measurement/";
const unsigned long measurementInterval = 300000; // 5 minutes

## Deployment to Production (Beget Hosting)

1. Copy all Django files to ~/publicwater.ru/public_html/
2. Create virtual environment: python3.7 -m venv venv
3. Install dependencies: pip install -r requirements.txt

Configure .htaccess:
PassengerEnabled On
PassengerPython /home/username/publicwater.ru/venv/bin/python
PassengerLogFile /home/username/publicwater.ru/tmp/passenger.log
PassengerLogLevel 3

Configure passenger_wsgi.py:
import os, sys
sys.path.insert(0, '/home/username/publicwater.ru/public_html')
os.environ['DJANGO_SETTINGS_MODULE'] = 'water_monitor.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

Restart application:
cd ~/publicwater.ru
touch tmp/restart.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: https://github.com/AlexeySIVUKHIN/water-monitoring-iot
