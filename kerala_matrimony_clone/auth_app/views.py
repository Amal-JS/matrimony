from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.files.base import ContentFile
from django.conf import settings
import os
import base64
from django.contrib.auth import authenticate, login,logout
from .models import CustomUser
import json
from datetime import datetime, date
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile




# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        
        return redirect('sign_up')
    print('user logged :',request.user.username)
    users = CustomUser.objects.filter(is_superuser=False)
    return render(request,'auth_app/index.html',{'users':users})

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'auth_app/signup.html')
def register2(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'auth_app/register2.html')
def register3(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'auth_app/register3.html')
def register4(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'auth_app/register4.html')
def register5(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'auth_app/register5.html')
def register6(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'auth_app/register6.html')
def logout_user(request):
    logout(request)
    return redirect('sign_up')

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        

def check_values(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('valid')
            return JsonResponse({'isValid':True})
        else:
            return JsonResponse({'isValid':False})

def create_user_account(request):
    if request.method == 'POST':
        data = request.POST.dict()

        # Handle base64 encoded profile picture
        profile_picture_base64 = data.pop('profilePicture', None)
        if profile_picture_base64:
            format, imgstr = profile_picture_base64.split(';base64,')
            ext = format.split('/')[-1]
            profile_picture = ContentFile(base64.b64decode(imgstr), name=f"profile_picture.{ext}")

            # Save the profile picture to a desired location
            profile_picture_path = os.path.join(settings.MEDIA_ROOT, profile_picture.name)
            with open(profile_picture_path, 'wb') as f:
                f.write(profile_picture.read())
                data['profile_picture'] = profile_picture.name
            # Include the path to the saved profile picture in the data dictionary
            del data['csrfmiddlewaretoken']
            try:
                new_user  = CustomUser(**data)
                new_user.set_password(data.get('password'))
                new_user.save()
                
                return JsonResponse({'isCreated':True})
            except Exception as e:
                print(e)
                return JsonResponse({'isCreated':False,'error':e})
    else :
        return JsonResponse({'isCreated':False})

def update_profile(request,id):

    if not request.user.is_authenticated:
        return redirect('sign_up')
    
    if request.method == 'POST':
        user = CustomUser.objects.get(id=id)
        
        new_data = request.POST.dict()
        print(new_data)
        old_data = {}
        fields = CustomUser._meta.get_fields()
        for field in fields:
            field_name = field.name
            if hasattr(user, field_name):
                old_data[field_name] = getattr(user, field_name)

        for field in request.POST:

            if field == 'profile_picture' :
            # Handle base64 encoded profile picture
                profile_picture_base64 = new_data.pop('profilePicture', None)
                if profile_picture_base64:
                    format, imgstr = profile_picture_base64.split(';base64,')
                    ext = format.split('/')[-1]
                    profile_picture = ContentFile(base64.b64decode(imgstr), name=f"profile_picture.{ext}")

                    # Save the profile picture to a desired location
                    profile_picture_path = os.path.join(settings.MEDIA_ROOT, profile_picture.name)
                    with open(profile_picture_path, 'wb') as f:
                        f.write(profile_picture.read())
                        new_data['profile_picture'] = profile_picture.name
                        user.profile_picture = profile_picture.name
            elif field == 'password':
                pass
            else :
                new_data[field] = request.POST.get(field, '')

            for field in new_data:
                
                if field == 'password' and new_data.get(field,'') != '':
                    user.set_password(new_data[field])
                elif new_data[field].isdigit() :
                    value = int(new_data[field])
                    if value != new_data[field]:
                        setattr(user, field, new_data[field])
                elif old_data[field] != new_data[field]:

                    setattr(user, field, new_data[field])
            try:
                user.save()
                print('data updated')
                return JsonResponse({'userDetailsUpdated':True})
            except Exception as e:
                print(e)
                return JsonResponse({'userDetailsUpdated':False,'error':e})
    else :
        return JsonResponse({'userDetailsUpdated':False})
    



    
def edit_profile(request,id):

    if not request.user.is_authenticated:
        return redirect('sign_up')
    old_data = {}
    user = CustomUser.objects.get(id=id)
    fields = CustomUser._meta.get_fields()
    for field in fields:
        field_name = field.name
        if hasattr(user, field_name):
            value = getattr(user, field_name)
            if isinstance(value, (datetime, date, Decimal)):
                old_data[field_name] = value.isoformat() if isinstance(value, (datetime, date)) else str(value)
            elif isinstance(value, ImageFieldFile):
                old_data[field_name] = value.url if value else ''
            else:
                old_data[field_name] = value

    return render(request,'auth_app/update.html',{'oldData':old_data})