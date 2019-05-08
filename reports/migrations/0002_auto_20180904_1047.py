# Generated by Django 2.0.7 on 2018-09-04 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='sensor_type',
            field=models.CharField(choices=[('CO2', 'CO2'), ('NH3', 'NH3'), ('TEMPERATURE', 'Temperature'), ('HUMIDITY', 'Humidity')], default='', max_length=11),
        ),
    ]
