# Generated by Django 4.0 on 2022-02-04 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick_car', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_last_roll',
            name='last_rolled_collection',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
