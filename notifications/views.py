from django.shortcuts import render
from reports.models import DeviceNetwork, DeviceLocation, Device, Sensor
from .forms import SensorNotificationForm, SensorNotificationEmailForm
from .models import SensorNotificationEmail, SensorNotification
from django.contrib.auth.decorators import login_required
# from django.forms.formsets import formset_factory

@login_required(login_url='login')
def notify(request):
        deviceNetwork_list = DeviceNetwork.objects.filter(organization=request.user.orgs)
        deviceLocation_list = DeviceLocation.objects.filter(device_network__in=deviceNetwork_list)
        device_list = Device.objects.filter(device_location__in=deviceLocation_list)
        sensor_list = Sensor.objects.filter(device__in=device_list)

        if request.method == "POST":
            form1 = SensorNotificationForm(request.POST)
            form2 = SensorNotificationEmailForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                # print("==================save==================")
            else:
                print("xxxxxxxxxxxxxxxxx",form1.errors)
                # print("-========================")
                # print("xxxxxxxxxxxxxxxxx",form2.errors)
        context = {
            'deviceNetwork_list': deviceNetwork_list,
            'deviceLocation_list': deviceLocation_list,
            'device_list': device_list,
            'sensor_list': sensor_list         
        }

        return render(request, 'notifications/test.html', context)

@login_required(login_url='login')
def sensor_notify(request, sensor_id):
         # SensorNotificationEmailFormSet = formset_factory(SensorNotificationEmailForm, extra=3)
        deviceNetwork_list = DeviceNetwork.objects.filter(organization=request.user.orgs)
        deviceLocation_list = DeviceLocation.objects.filter(device_network__in=deviceNetwork_list)
        device_list = Device.objects.filter(device_location__in=deviceLocation_list)
        sensor_list = Sensor.objects.filter(device__in=device_list)

        form1 = SensorNotificationForm()
        form2 = SensorNotificationEmailForm()

        context = {
             'deviceNetwork_list': deviceNetwork_list,
             'deviceLocation_list': deviceLocation_list,
             'device_list': device_list,
             'sensor_list': sensor_list,
             'form1': form1,
             'form2': form2
             }

        return render(request, 'notifications/test.html', context)

