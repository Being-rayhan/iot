from reports.models import Sensor, SensorData
from rest_framework import serializers

class SensorDataSerializer(serializers.ModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())
    id = serializers.ReadOnlyField()
    class Meta:
        model = SensorData
        fields = ('id', 'sensor', 'timestamp', 'value')

    def create(self, validated_data):
        sensor_instance = validated_data.pop('sensor')
        sensor_data = SensorData.objects.create(sensor=sensor_instance, **validated_data)
        return sensor_data
