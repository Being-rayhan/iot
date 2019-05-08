from django.contrib import admin
from .models import DeviceNetwork, DeviceLocation, Device, Sensor, SensorData
from tenants.models import Organization

from django.shortcuts import redirect
from django.utils.safestring import mark_safe


class OrganizationAdmin(admin.ModelAdmin):
    #list_display = ('name', )
    exclude = ('modified_by', )

admin.site.register(Organization, OrganizationAdmin)




class DeviceNetworkAdmin(admin.ModelAdmin):
    #list_display = ('name', )
    exclude = ('modified_by', )

admin.site.register(DeviceNetwork, DeviceNetworkAdmin)



class DeviceLocationAdmin(admin.ModelAdmin):
    #list_display = ('name', )
    exclude = ('modified_by', )

admin.site.register(DeviceLocation, DeviceLocationAdmin)



class DeviceAdmin(admin.ModelAdmin):
    #list_display = ('name', )
    exclude = ('modified_by', )

admin.site.register(Device, DeviceAdmin)



class SensorAdmin(admin.ModelAdmin):
    #list_display = ('name', )
    exclude = ('modified_by', )

admin.site.register(Sensor, SensorAdmin)



class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'timestamp', 'value', 'inserted_date', 'last_modified', 'modified_by',)


admin.site.register(SensorData, SensorDataAdmin)
