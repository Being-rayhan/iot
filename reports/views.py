import csv
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
import datetime

from django.db.models import F, Sum, Avg

from .forms import ExportForm, DeviceForm2
from reports.models import DeviceNetwork, DeviceLocation, Device, Sensor, SensorData
from tenants.views import get_context

from django.utils import timezone
today = timezone.now()

ordinal = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th']

def parse_date(obj):
    d_f = '%Y-%m-%d'
    d_t = '%H:%M:%S %p'

    if type(obj) is datetime.date or type(obj) is datetime.datetime:
        return obj.strftime(d_t)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def retrieve_data(date):
    data = {}
    return data


@login_required(login_url='login')
def export(request):
    if request.method == 'POST':
        """A view that streams a large CSV file."""
        # Generate a sequence of rows. The range is based on the maximum number of
        # rows that can be handled by a single sheet in most spreadsheet
        # applications.
        rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        return response

    else:
        context = retrieve_data(today)
        context['form'] = ExportForm()
        return render(request, 'reports/export.html', context)


@login_required(login_url='login')
def index(request):
    all_data = get_context(request.user, True)
    today = datetime.datetime.now()

    context = {
        'data': all_data['data'],
    }

    if request.method == "GET":
        device_form = DeviceForm2(location_devices=all_data['devices'])
        context['device_form'] = device_form

    else:
        device_form = DeviceForm2(request.POST, location_devices=all_data['devices'])
        if device_form.is_valid():
            selected_device = Device.objects.get(pk=device_form.cleaned_data['device'].pk)
            sensors = Sensor.objects.filter(device=selected_device)
            sensor_data = SensorData.objects.filter(sensor__in=sensors)

            s_date = device_form.cleaned_data['date']

            def get_d_extra(t=False):
                res = {}
                if s_date == 'YEAR':
                    res['end_at'] = 13
                    if t:
                        res['timestamp'] = ordinal[t - 1]
                        res['timestamp_data'] = sensor_data.filter(sensor=s, timestamp__year=today.year, timestamp__month=t).aggregate(Avg('value'))['value__avg']
                elif s_date == 'WEEK':
                    res['end_at'] = 8
                    if t:
                        res['timestamp'] = ordinal[t - 1]
                        res['timestamp_data'] = sensor_data.filter(sensor=s, timestamp__year=today.year, timestamp__month=today.month, timestamp__week=today.isocalendar()[1], timestamp__day=(today.day - t + 1)).aggregate(Avg('value'))['value__avg']
                else:
                    res['end_at'] = 25
                    if t:
                        res['timestamp'] = ordinal[t - 1]
                        res['timestamp_data'] = sensor_data.filter(sensor=s, timestamp__year=today.year, timestamp__month=today.month, timestamp__day=today.day, timestamp__hour=(t - 1)).aggregate(Avg('value'))['value__avg']
                return res

            result = []

            for s in sensors:
                a = []
                for t in range(1, get_d_extra()['end_at']):
                    g = get_d_extra(t)
                    d1 = {
                        'timestamp': g['timestamp'],
                        'value': g['timestamp_data'],
                    }
                    if d1['value']:
                        a.append(d1)
                d2 = {
                    'sensor': {
                        'id': s.id,
                        'sensor_type': s.sensor_type,
                        'upper_threshold': s.upper_threshold,
                        'lower_threshold': s.lower_threshold,
                    },
                    'data': a,
                }
                sd = sensor_data.filter(sensor=s)
                if sd:
                    ld = sd.values('timestamp', 'value').latest('timestamp')
                    d2['latest_data'] = {
                        'timestamp': timezone.localtime(ld['timestamp']).strftime('%H:%M:%S'),
                        'value': ld['value'],
                    }
                result.append(d2)

            context['device_form'] = device_form
            context['sensor_data'] = result,
            context['json_sensor_data'] = json.dumps(result, default=parse_date)
            context['selected_data'] = {
                'network': selected_device.device_location.device_network,
                'location': selected_device.device_location,
                'device': selected_device,
                'date': s_date,
            }
            return render(request, 'reports/reports.html', context)

    return render(request, 'reports/reports.html', context)


@login_required(login_url='login')
def user_update(request):
   
        return render(request, 'reports/user_update.html', context)