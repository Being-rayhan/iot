from django import forms
from tenants.models import User
from reports.models import DeviceNetwork, DeviceLocation, Device, Sensor


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'contact_number', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Last Name'
        })
        self.fields['contact_number'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Contact Number'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Password'
        })
        self.fields['confirm_password'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Confirm Password'
        })

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'contact_number',)

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Last Name'
        })
        self.fields['contact_number'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Contact Number'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Username'
        })

class UpdateNetworkForm(forms.ModelForm):
    class Meta:
        model = DeviceNetwork
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(UpdateNetworkForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Network Name'
        })


class UpdateLocationForm(forms.ModelForm):
    class Meta:
        model = DeviceLocation
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(UpdateLocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Location Name'
        })

class UpdateDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('device_id',)

    def __init__(self, *args, **kwargs):
        super(UpdateDeviceForm, self).__init__(*args, **kwargs)
        self.fields['device_id'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Device ID'
        })

class UpdateSensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_type', 'upper_threshold', 'lower_threshold',)

    def __init__(self, *args, **kwargs):
        super(UpdateSensorForm, self).__init__(*args, **kwargs)
        self.fields['sensor_id'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Sensor ID'
        })
        self.fields['sensor_type'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Sensor Type'
        })
        self.fields['upper_threshold'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Upper Threshold'
        })
        self.fields['lower_threshold'].widget.attrs.update({
            'class': 'bx--text-input bx--text-input--light',
            'placeholder': 'Enter Lower Threshold'
        })


class DeleteForm(forms.Form):
    USER = 'USER'
    NETWORK = 'NETWORK'
    LOCATION = 'LOCATION'
    DEVICE = 'DEVICE'
    SENSORS = 'SENSORS'

    TYPE_CHOICES = (
        (USER, 'User'),
        (NETWORK, 'Network'),
        (LOCATION, 'Location'),
        (DEVICE, 'Device'),
        (SENSORS, 'Sensor'),
    )

    all_ids = forms.CharField(widget=forms.Textarea)
    id_type = forms.ChoiceField(choices=TYPE_CHOICES)
