from django import forms
from .models import SensorNotification, SensorNotificationEmail
from django.forms.widgets import HiddenInput



class SensorNotificationForm(forms.ModelForm):
    class Meta:
        model = SensorNotification
        fields = ('sensor', 'min_optimal_value', 'max_optimal_value', 'enabled')


    # def __init__(self, *args, **kwargs):
    #     super(SensorNotificationForm, self).__init__(*args, **kwargs)
    #     self.fields['sensor'].widget = HiddenInput()


class SensorNotificationEmailForm(forms.ModelForm):
    class Meta:
        model = SensorNotificationEmail
        fields = ('sensor_notification', 'from_email', 'to_email')


    # def __init__(self, *args, **kwargs):
    #     super(SensorNotificationEmailForm, self).__init__(*args, **kwargs)
    #     self.fields['sensor_notification'].widget = HiddenInput()

    
