from django.urls import path

from . import views

app_name = 'tenants'

urlpatterns = [
    path('', views.index, name='index'),
    path('device_network/', views.device_network, name='device_network'),
    path('device_location/', views.device_location, name='device_location'),
    path('device/', views.device, name='device'),
    path('sensor/', views.sensor, name='sensor'),
    path('org_user/', views.org_user, name='org_user'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.users, name='users'),
    path('networks/', views.networks, name='networks'),
    path('locations/', views.locations, name='locations'),
    path('devices/', views.devices, name='devices'),
    path('sensors/', views.sensors, name='sensors'),
    path('update_network/<int:network_id>/', views.update_network, name='update_network'),
    path('update_location/<int:location_id>/', views.update_location, name='update_location'),
    path('update_device/<int:device_id>/', views.update_device, name='update_device'),
    path('update_sensor/<int:sensor_id>/', views.update_sensor, name='update_sensor'),

    path('delete_entry', views.delete_entry, name='delete_entry'),

    path('change_password', views.change_password, name='change_password'),
]
