from django.db import models
from reports.models import Sensor
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class SensorNotification(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    min_optimal_value = models.FloatField(null=True)
    max_optimal_value = models.FloatField(null=True)
    enabled = models.BooleanField(default=True)
    
    @receiver(post_save, sender=Sensor)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
          SensorNotification.objects.create(sensor=instance)


class SensorNotificationEmail(models.Model):
    sensor_notification = models.ForeignKey(SensorNotification, on_delete=models.CASCADE)
    from_email = models.EmailField(max_length=100)
    to_email = models.EmailField(max_length=100)
