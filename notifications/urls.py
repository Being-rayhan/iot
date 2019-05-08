from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notify, name='notify'),
    # path('<int:sensor_id>/', views.sensor_notify, name='sensor_notify'),
]