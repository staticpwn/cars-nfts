from django.db import models

# Create your models here.

class user_last_roll(models.Model):
    last_roll_time = models.FloatField(max_length=100)
    last_rolled_collection = models.TextField(max_length=1000, blank=True)
    user = models.CharField(max_length=255)

class car_part(models.Model):
    id = models.PositiveIntegerField(primary_key=True, editable=False, blank=False)
    URI_address = models.TextField(max_length=1000, blank=False)
    locked = models.BooleanField(default=False)
    locked_for = models.CharField(max_length=255, default="", blank=True)
    locked_time = models.FloatField(default=0)


    def __str__(self):

        return str(self.id)