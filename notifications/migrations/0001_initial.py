# Generated by Django 2.0.7 on 2018-09-05 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0002_auto_20180904_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_optimal_value', models.FloatField()),
                ('max_optimal_value', models.FloatField()),
                ('enabled', models.BooleanField(default=True)),
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reports.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='SensorNotificationEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_email', models.EmailField(max_length=100)),
                ('to_email', models.EmailField(max_length=100)),
                ('sensor_notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.SensorNotification')),
            ],
        ),
    ]
