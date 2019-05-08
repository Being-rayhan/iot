from urllib.parse import urljoin
import requests
import config
from datetime import datetime, timedelta
import sys
import os
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

sys.path.append(config.web_project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = config.web_project_name + '.settings'
django.setup()

from reports.models import Device, Sensor, SensorData


date_format = '%Y-%m-%d %H:%M:%S'


def get_devices(url, payload):
    url = urljoin(url, 'devices')
    devices = requests.get(url, params=payload)
    print(devices,"xxxxxx1")
    return devices.json()


def get_sensors(url, payload):
    url = urljoin(url, 'sensors')

    sensors = requests.get(url, params=payload)
    print(sensors,"xxxxxx2")
    return sensors.json()


def get_data(url, payload):
    url = urljoin(url, 'projects')
    url = url + '/getData'
    data = requests.get(url, params=payload)
    print(data,"xxxxxx3")
    return data.json()


def get_api_tokens():
    return config.api_tokens


def save_data(data):
    if len(data['data']) > 0:
        try:
            device = Device.objects.get(device_id=data['data'][0]['deviceIdentifier'])
        except Device.DoesNotExist:
            print('Device ', data['data'][0]['deviceIdentifier'], 'not registered! Skipping all sensors of this device entirely!')

        for d in data['data']:
            print(d)
            sensor = Sensor.objects.get(device=device, sensor_id=d['sensorIdentifier'])
            ts = timezone.make_aware(datetime.fromtimestamp(d['loggedTime'] / 1000))
            sd = SensorData(sensor=sensor, timestamp=ts, value=d['value'])
            sd.save()


if __name__ == '__main__':
    tokens = get_api_tokens()
    for token in tokens:
        payload = {
            'api_token': token
        }

        devices = get_devices(config.remote_url, payload)
        print("device--------------",devices)
        sensors = get_sensors(config.remote_url, payload)
        print("sensors--------------",sensors)

        for device in devices['data']:
            for sensor in device['deviceChannels']:

                s_data = SensorData.objects.filter(sensor__sensor_id=sensor['sensorIdentifier'])

                if s_data:
                    start_date = (timezone.localtime(s_data.latest('timestamp').timestamp) + timedelta(0, 1)).strftime(date_format)
                else:
                    start_date = datetime.today().replace(minute=0, hour=0, second=0, microsecond=0).strftime(date_format)
                 
                print("s====================",start_date)
    

                end_date = datetime.now().strftime(date_format)
                print("e====================",end_date)

                payload = {
                    'api_token': token,
                    'device_identifier': device['deviceIdentifier'],
                    'sensor_identifier': sensor['sensorIdentifier'],
                    'start': start_date,
                    'end': end_date,
                    'per_page': 50000,
                    'page_no': 1,

                }

                data = get_data(config.remote_url, payload)

                print("====================",data)

                save_data(data)
