from reports.models import SensorData

from rest_framework import viewsets
from .serializers import SensorDataSerializer


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    #http_method_names = ['get', 'head', 'post']
