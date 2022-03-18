
from django.shortcuts import render
import os
from random import randint
from django.contrib.staticfiles.storage import staticfiles_storage
from pandas import to_datetime
from time import time
from .models import user_last_roll, car_part
from rest_framework import views
from rest_framework.response import Response
from ast import literal_eval
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.

MINTNG_WINDOW = 30 # in seconds
USER_LOCKUP = 60 # in seconds
def front_page(request):
    
    
    image_dirs = list(car_part.objects.filter(locked_time__lt= time() - MINTNG_WINDOW))
    
    try:
        image_dirs.remove("blank.jpg")
        image_dirs.remove("locked.jpg")
    except:
        pass

    if len(user_last_roll.objects.filter(user=request.user.get_username())) != 0:
        if user_last_roll.objects.filter(user=request.user.get_username())[0].last_roll_time < (time() - USER_LOCKUP):
            user_last_roll.objects.get(user=request.user.get_username()).delete()
            to_unlock = car_part.objects.filter(locked_for=request.user.get_username())
            if len(to_unlock) >0:
                for part in to_unlock:
                    part.locked = False
                    part.locked_for = ""
                    part.locked_time = 0
                    part.save()
    
    
    if request.method == "GET":
        # print(user_last_roll.objects.filter(user=request.user.get_username()))   
        if len(user_last_roll.objects.filter(user=request.user.get_username())) == 0:#
            to_unlock = car_part.objects.filter(locked_for=request.user.get_username())
            if len(to_unlock) >0:
                for part in to_unlock:
                    part.locked = False
                    part.locked_for = ""
                    part.locked_time = 0
                    part.save()
            images = ["blank.jpg" for i in range(6)]
            context = {
                'images' : images,
                'user_name': request.user.get_username()
            }
            return render(request, 'front_page.html', context=context)
        else:

            if user_last_roll.objects.filter(user=request.user.get_username(), last_roll_time__gt = (time() - MINTNG_WINDOW)):
                image_ids = literal_eval(user_last_roll.objects.get(user=request.user.get_username()).last_rolled_collection)
                images = car_part.objects.filter(id__in = image_ids).values_list('URI_address', flat=True)
                context = {
                    'images' : images,
                    'user_name': request.user.get_username(),
                    'next_roll_date': to_datetime(user_last_roll.objects.get(user=request.user.get_username()).last_roll_time + USER_LOCKUP,unit="s",utc=True)
                }
                
                return render(request, 'front_page.html', context=context)
            else:
                images = ["locked.jpg" for i in range(6)]
                to_unlock = car_part.objects.filter(locked_for=request.user.get_username())
                for part in to_unlock:
                    part.locked = False
                    part.locked_for = ""
                    part.locked_time = 0
                    part.save()
                context = {
                    'images' : images,
                    'user_name': request.user.get_username(),
                    'next_roll_date': to_datetime(user_last_roll.objects.get(user=request.user.get_username()).last_roll_time + USER_LOCKUP,unit="s",utc=True)
                }
                
                return render(request, 'front_page.html', context=context)                
            
    elif request.method == "POST":

            if request.POST["button"] == "Roll":
                if len(user_last_roll.objects.filter(user=request.user.get_username())) == 0:
                    images = []
                    image_ids = []
                    for i in range(6):
                        idx = randint(0,len(image_dirs)-1)
                        images.append(image_dirs[idx].URI_address)
                        image_ids.append(str(image_dirs[idx]))
                        
                        image_dirs[idx].locked = True
                        image_dirs[idx].locked_for = request.user.get_username()
                        image_dirs[idx].locked_time = time()
                        image_dirs[idx].save()
                        del image_dirs[idx]
                    image_ids.sort(key = int)

                    context = {
                        'images' : car_part.objects.filter(id__in = image_ids).values_list('URI_address', flat=True),
                        'user_name': request.user.get_username(),
                        'next_roll_date': to_datetime(user_last_roll.objects.create(
                            user=request.user.get_username(), 
                            last_roll_time=time(), 
                            last_rolled_collection=str(image_ids)).last_roll_time + USER_LOCKUP,unit="s")
                    }
                    return render(request, 'front_page.html', context=context)
                else:
                    image_ids = literal_eval(user_last_roll.objects.get(user=request.user.get_username()).last_rolled_collection)
                    images = car_part.objects.filter(id__in = image_ids).values_list('URI_address', flat=True)
                    context = {
                        'images' : images,
                        'user_name': request.user.get_username(),
                        'next_roll_date': to_datetime(user_last_roll.objects.get(user=request.user.get_username()).last_roll_time + USER_LOCKUP,unit="s",utc=True),
                        'message': "You have already rolled. Please mint your collection, or wait out the clock before trying again."
                    }
                    return render(request, 'front_page.html', context=context)

            elif request.POST["button"] == "Mint":
                
                image_ids = literal_eval(user_last_roll.objects.get(user=request.user.get_username()).last_rolled_collection)
                images = car_part.objects.filter(id__in = image_ids).values_list('URI_address', flat=True)
                context = {
                    'images' : images,
                    'user_name': request.user.get_username(),
                    'next_roll_date': to_datetime(user_last_roll.objects.get(user=request.user.get_username()).last_roll_time + USER_LOCKUP,unit="s",utc=True),
                    'message': "You have already rolled. Please mint your collection, or wait out the clock before trying again."
                }
                
                # try:
                #     print("test" in request.session)
                #     print(request.session["test"])
                #     del request.session["test"]

                #     print("test" in request.session)
                # except:
                #     pass
                return render(request, 'front_page.html', context=context)




class test_api(views.APIView):
    
    def get(self, request):
        hash = "test_hash"
        request.session["hash"] = hash
       
        return Response(hash)

    def post(self, request):
        
        _input = request.query_params.get("input")
        _hash = request.query_params.get("hash")
        
        if request.session["hash"] != _hash.replace('"', ''):
            del request.session["hash"]
            return Response("Hash doesn't match.")
             
        del request.session["hash"]    

        if len(User.objects.filter(username=_input)) == 0:
            if len(_input) >0:
                if not any(not c.isalnum() for c in _input):
                    new_user = User.objects.create(username=_input)
                    new_user.set_unusable_password()
                    new_user.save()
                    
                    login(request, new_user)
                else:
                    return Response("Address can only be alpha-numeric.")

                return Response(f"Successfully created account for address: {_input}.")
            else:
                return Response("Please connect your metamask.")
        else:
            to_login = User.objects.get(username=_input)
            login(request, to_login)
            return Response("Address {} logged in.".format(_input))


def my_login(request):
    return render(request, template_name="login.html")





if car_part.objects.count() == 0:
    car_parts_path =   staticfiles_storage.path('') + staticfiles_storage.url('car_parts')
    image_dirs = os.listdir(car_parts_path)
    image_dirs.remove("blank.jpg")
    image_dirs.remove("locked.jpg")


    for i in range(10*6):
        car_part.objects.create(id=car_part.objects.count()+1, URI_address=image_dirs[randint(0,len(image_dirs)-1)])



