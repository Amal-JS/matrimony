from django.shortcuts import redirect, render
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages

from auth_app.models import CustomUser


def index(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('admin_login')
    all_users = CustomUser.objects.filter(is_superuser=False)

    return render(request,'admin_app/index.html',{'users':all_users})



def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_index')
    
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
     
        if username == '' or password == '':
            messages.error(request, "Empty form can't be submitted")
            return redirect('admin_login')

        try:
            user = CustomUser.objects.get(username=username)
            if not user.is_superuser:
                messages.error(request, 'You do not have admin privileges.')
                return redirect('admin_login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('admin_login')

        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_index')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('admin_login')

    return render(request, 'admin_app/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')



def user_details(request,id):
    if not request.user.is_superuser :
        return redirect('admin_login')
    user = CustomUser.objects.get(id=id)
    return render(request,'admin_app/user_details.html',{'user':user})

