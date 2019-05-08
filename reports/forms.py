from django import forms
from .models import DeviceNetwork, DeviceLocation, Device, Sensor


class ExportForm(forms.Form):
    since = forms.DateField(label='From')
    until = forms.DateField(label='To')


class DeviceNetworkForm(forms.ModelForm):
    class Meta:
        model = DeviceNetwork
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super(DeviceNetworkForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter Network Name', 'class': 'bx--text-input bx--text-input--light'})


class DeviceLocationForm(forms.ModelForm):
    class Meta:
        model = DeviceLocation
        fields = ('device_network', 'name', )

    def __init__(self, *args, **kwargs):
        super(DeviceLocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter Location Name', 'class': 'bx--text-input bx--text-input--light'})


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('device_location', 'device_id', 'active', )

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['device_id'].widget.attrs.update({'placeholder': 'Enter Device ID', 'class': 'bx--text-input bx--text-input--light'})
        self.fields['active'].widget = forms.HiddenInput()


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ('device', 'sensor_type', 'sensor_id', 'upper_threshold', 'lower_threshold')

    def __init__(self, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
        self.fields['sensor_id'].widget.attrs.update({'placeholder': 'Enter Sensor ID', 'class': 'bx--text-input bx--text-input--light'})
        self.fields['upper_threshold'].widget.attrs.update({'placeholder': 'Enter Upper Threshold', 'class': 'bx--text-input bx--text-input--light'})
        self.fields['lower_threshold'].widget.attrs.update({'placeholder': 'Enter Lower Threshold', 'class': 'bx--text-input bx--text-input--light'})


class DeviceForm2(forms.Form):
    TODAY = 'TODAY'
    WEEK = 'WEEK'
    YEAR = 'YEAR'

    DATE_TYPE_CHOICES = (
        (TODAY, 'Today'),
        (WEEK, 'This Week'),
        (YEAR, 'This Year'),
    )

    device = forms.ModelChoiceField(queryset=None)
    date = forms.ChoiceField(choices=DATE_TYPE_CHOICES)

    def __init__(self, *args, **kwargs):
        location_devices = kwargs.pop('location_devices', None)
        super(DeviceForm2, self).__init__(*args, **kwargs)
        self.fields['device'].queryset = location_devices
        self.fields['device'].widget.attrs.update({'placeholder': 'Enter Device ID', 'class': 'bx--text-input bx--text-input--light'})
