# Generated by Django 4.0.2 on 2022-02-17 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick_car', '0004_car_part'),
    ]

    operations = [
        migrations.AddField(
            model_name='car_part',
            name='locked_time',
            field=models.FloatField(default=0),
        ),
    ]
