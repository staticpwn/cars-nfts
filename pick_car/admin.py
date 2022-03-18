from django.contrib import admin

# Register your models here.

from .models import user_last_roll, car_part


@admin.register(user_last_roll)
class user_last_rollAdmin(admin.ModelAdmin):
    list_display = ['last_roll_time','last_rolled_collection', 'user']
    

    fields = ['last_roll_time','last_rolled_collection', 'user']



@admin.register(car_part)
class ucar_partAdmin(admin.ModelAdmin):
    list_display = ['id','URI_address', 'locked', 'locked_for', 'locked_time']
    read_only_fields = ['id', 'locked', 'locked_for', 'locked_time']
    list_filter = ['locked_for']
    fields = ['id','URI_address', 'locked', 'locked_for', 'locked_time']