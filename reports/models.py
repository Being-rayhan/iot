from django.db import models
from django.contrib.auth import get_user_model
from tenants.models import Organization

User = get_user_model()


class DeviceNetwork(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    inserted_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "    Device Networks"

    def __str__(self):
        return self.name

class DeviceLocation(models.Model):
    device_network = models.ForeignKey(DeviceNetwork, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    inserted_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name_plural = "   Device Locations"


    def __str__(self):
        return self.name

class Device(models.Model):
    device_location = models.ForeignKey(DeviceLocation, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    inserted_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name_plural = "  Devices"


    def __str__(self):
        return self.device_id


class Sensor(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    sensor_id = models.CharField(max_length=10) # should be unique

    CO2 = 'CO2'
    NH3 = 'NH3'
    TEMPERATURE = 'TEMPERATURE'
    HUMIDITY = 'HUMIDITY'

    SENSOR_TYPE_CHOICES = (
        (CO2, 'CO2'),
        (NH3, 'NH3'),
        (TEMPERATURE, 'Temperature'),
        (HUMIDITY, 'Humidity'),
    )

    sensor_type = models.CharField(
        choices=SENSOR_TYPE_CHOICES,
        max_length=11,
        default='',
    )

    upper_threshold = models.FloatField()
    lower_threshold = models.FloatField()

    inserted_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = " Sensors"

    def __str__(self):
        return self.sensor_id

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

    inserted_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name_plural = "Sensor Data"

    def __str__(self):
        return str(self.timestamp)
