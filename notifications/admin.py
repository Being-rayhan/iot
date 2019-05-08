from django.contrib import admin

from .models import SensorNotification, SensorNotificationEmail



class SensorNotificationEmailAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sensor Notification Email', {'fields': ['from_email', 'to_email', 'sensor_notification']}),
    ]

admin.site.register(SensorNotificationEmail,SensorNotificationEmailAdmin)



class SensorNotificationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sensor Notification', {'fields': ['sensor','min_optimal_value', 'max_optimal_value', 'enabled']}),
    ]

admin.site.register(SensorNotification,SensorNotificationAdmin)
