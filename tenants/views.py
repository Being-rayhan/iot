from django.shortcuts import render, redirect, get_object_or_404
from reports.models import DeviceNetwork, DeviceLocation, Device, Sensor
from .models import User
from django.contrib.auth.decorators import login_required
import json
from reports.forms import DeviceNetworkForm, DeviceLocationForm, DeviceForm, SensorForm
from tenants.forms import UserForm, UpdateUserForm, UpdateNetworkForm, UpdateSensorForm, UpdateDeviceForm, UpdateLocationForm, DeleteForm

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

# from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def get_context(user, data_only=False):
    user_form = UserForm(prefix='user_form')
    device_network_form = DeviceNetworkForm(prefix='device_network_form')
    device_location_form = DeviceLocationForm(prefix='device_location_form')
    device_form = DeviceForm(prefix='device_form')
    sensor_form = SensorForm(prefix='sensor_form')
    delete_form = DeleteForm(prefix='delete_form')

    all_u = User.objects.filter(orgs=user.orgs)
    all_dn = DeviceNetwork.objects.filter(organization=user.orgs)
    all_dl = DeviceLocation.objects.filter(device_network__in=all_dn)
    all_d = Device.objects.filter(device_location__in=all_dl)
    all_s = Sensor.objects.filter(device__in=all_d)

    data = {
        'sensors': [{'name': s.sensor_id, 'id': s.id, 'device_id': s.device.id} for s in all_s],
        'devices': [{'name': d.device_id, 'id': d.id, 'location_id': d.device_location.id} for d in all_d],
        'locations': [{'name': dl.name, 'id': dl.id, 'network_id': dl.device_network.id} for dl in all_dl],
        'networks': [{'name': dn.name, 'id': dn.id, 'organization_id': dn.organization.id} for dn in all_dn],
    }

    context = {
        'data': data,
        'json_data': json.dumps(data),
        'users': all_u,
        'networks': all_dn,
        'locations': all_dl,
        'devices': all_d,
        'sensors': all_s,
    }

    if not data_only:
        context['user_form'] = user_form
        context['device_network_form'] = device_network_form
        context['device_location_form'] = device_location_form
        context['device_form'] = device_form
        context['sensor_form'] = sensor_form
        context['delete_form'] = delete_form

    return context


@login_required(login_url='login')
def index(request):
    if not request.user.is_client:
        return redirect('reports:index')
    return render(request, 'tenants/settings.html', get_context(request.user))


@login_required(login_url='login')
def device_network(request):
    if request.method == 'POST':
        if request.user.is_client:
            device_network_form = DeviceNetworkForm(request.POST, prefix='device_network_form')
            if device_network_form.is_valid():
                f = device_network_form.save(commit=False)
                f.organization = request.user.orgs
                f.save()
            else:
                context = get_context(request.user)
                context['device_network_form'] = device_network_form
                return render(request, 'tenants/settings.html', context)

    return redirect('tenants:index')


@login_required(login_url='login')
def device_location(request):
    if request.method == 'POST':
        if request.user.is_client:
            device_location_form = DeviceLocationForm(request.POST, prefix='device_location_form')
            if device_location_form.is_valid():
                f = device_location_form.save(commit=False)
                f.save()
            else:
                context = get_context(request.user)
                context['device_location_form'] = device_location_form
                return render(request, 'tenants/settings.html', context)

    return redirect('tenants:index')


@login_required(login_url='login')
def device(request):
    if request.method == 'POST':
        if request.user.is_client:
            device_form = DeviceForm(request.POST, prefix='device_form')
            if device_form.is_valid():
                f = device_form.save(commit=False)
                f.save()
            else:
                context = get_context(request.user)
                context['device_form'] = device_form
                return render(request, 'tenants/settings.html', context)

    return redirect('tenants:index')


@login_required(login_url='login')
def sensor(request):
    if request.method == 'POST':
        if request.user.is_client:
            sensor_form = SensorForm(request.POST, prefix='sensor_form')
            if sensor_form.is_valid():
                f = sensor_form.save(commit=False)
                f.save()
            else:
                context = get_context(request.user)
                context['sensor_form'] = sensor_form
                context['selected_data'] = {
                    'device': sensor_form.data['sensor_form-device'],
                    'sensor_type': sensor_form.data['sensor_form-sensor_type'],
                }
                context['selected_data']['location'] = Device.objects.get(pk=context['selected_data']['device']).device_location.id
                context['selected_data']['network'] = DeviceLocation.objects.get(pk=context['selected_data']['location']).device_network.id
                return render(request, 'tenants/settings.html', context)

    return redirect('tenants:index')


@login_required(login_url='login')
def org_user(request):
    if request.method == 'POST':
        if request.user.is_client:
            form = UserForm(request.POST, prefix='user_form')
            if form.is_valid():
                user = form.save(commit=False)
                user.orgs = request.user.orgs
                user.set_password(form.cleaned_data['password'])
                user.save()
            else:
                context = get_context(request.user)
                context['user_form'] = form
                return render(request, 'tenants/settings.html', context)

    return redirect('tenants:index')


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST or None, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('tenants:index')
    user_form = UpdateUserForm(instance=request.user)
    form = PasswordChangeForm(user=request.user)
    return render(request, 'tenants/profile.html', {'user_form': user_form, 'form': form})


@login_required(login_url='login')
def users(request):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        context = get_context(request.user)

        sort_param = request.GET.get('q', None)
        if sort_param and hasattr(User, sort_param.replace("-", "")):
            context['users'] = context['users'].order_by(sort_param)
        return render(request, 'tenants/users.html', context)


@login_required(login_url='login')
def networks(request):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        context = get_context(request.user)

        sort_param = request.GET.get('q', None)
        if sort_param and hasattr(DeviceNetwork, sort_param.replace("-", "")):
            context['networks'] = context['networks'].order_by(sort_param)
        return render(request, 'tenants/networks.html', context)


@login_required(login_url='login')
def update_network(request, network_id):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        instance = DeviceNetwork.objects.get(pk=network_id)
        network_form = UpdateNetworkForm(request.POST or None, instance=instance)
        if request.method == 'POST':
            if network_form.is_valid():
                network_form.save()
                return redirect('tenants:index')
        return render(request, 'tenants/update_info.html', {'network_form': network_form})


@login_required(login_url='login')
def locations(request):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        context = get_context(request.user)

        sort_param = request.GET.get('q', None)
        if sort_param and hasattr(DeviceLocation, sort_param.replace("-", "")):
            context['locations'] = context['locations'].order_by(sort_param)
        return render(request, 'tenants/locations.html', context)


@login_required(login_url='login')
def update_location(request, location_id):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        instance = DeviceLocation.objects.get(pk=location_id)
        location_form = UpdateLocationForm(request.POST or None, instance=instance)
        if request.method == 'POST':
            if location_form.is_valid():
                location_form.save()
                return redirect('tenants:index')
        return render(request, 'tenants/update_info.html', {'location_form': location_form})


@login_required(login_url='login')
def devices(request):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        context = get_context(request.user)
        sort_param = request.GET.get('q', None)
        if sort_param and hasattr(Device, sort_param.replace("-", "")):
            context['devices'] = context['devices'].order_by(sort_param)
        return render(request, 'tenants/devices.html', context)


@login_required(login_url='login')
def update_device(request, device_id):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        instance = Device.objects.get(pk=device_id)
        device_form = UpdateDeviceForm(request.POST or None, instance=instance)
        if request.method == 'POST':
            if device_form.is_valid():
                device_form.save()
                return redirect('tenants:index')
        return render(request, 'tenants/update_info.html', {'device_form': device_form})


@login_required(login_url='login')
def sensors(request):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        context = get_context(request.user)
        sort_param = request.GET.get('q', None)
        if sort_param and hasattr(Sensor, sort_param.replace("-", "")):
            context['sensors'] = context['sensors'].order_by(sort_param)
        return render(request, 'tenants/sensors.html', context)


@login_required(login_url='login')
def update_sensor(request, sensor_id):
    if not request.user.is_client:
        return redirect('tenants:index')
    else:
        instance = Sensor.objects.get(pk=sensor_id)
        sensor_form = UpdateSensorForm(request.POST or None, instance=instance)
        if request.method == 'POST':
            if sensor_form .is_valid():
                sensor_form .save()
                return redirect('tenants:index')
        return render(request, 'tenants/update_info.html', {'sensor_form': sensor_form})


def delete_entry(request):
    context = get_context(request.user)
    if request.method == 'POST':
        delete_form = DeleteForm(request.POST, prefix='delete_form')
        if delete_form.is_valid():
            ids = delete_form.cleaned_data['all_ids'].split(',')

            if delete_form.cleaned_data['id_type'] == 'USER':
                u = User.objects.filter(id__in=ids)
                u.delete()
                return redirect('tenants:users')
            elif delete_form.cleaned_data['id_type'] == 'NETWORK':
                u = DeviceNetwork.objects.filter(id__in=ids)
                u.delete()
                return redirect('tenants:networks')
            elif delete_form.cleaned_data['id_type'] == 'LOCATION':
                u = DeviceLocation.objects.filter(id__in=ids)
                u.delete()
                return redirect('tenants:locations')
            elif delete_form.cleaned_data['id_type'] == 'DEVICE':
                u = Device.objects.filter(id__in=ids)
                u.delete()
                return redirect('tenants:devices')
            elif delete_form.cleaned_data['id_type'] == 'SENSORS':
                u = Sensor.objects.filter(id__in=ids)
                u.delete()
                return redirect('tenants:sensors')
        else:
            context['delete_form'] = delete_form

    return render(request, 'tenants/users.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('tenants:index'))
        else:
            user_form = UpdateUserForm(instance=request.user)
            return render(request, 'tenants/profile.html', {'user_form': user_form, 'form': form})
    else:
        form = PasswordChangeForm(user=request.user)
        user_form = UpdateUserForm(instance=request.user)
        return render(request, 'tenants/profile.html', {'form': form, 'user_form': user_form})
