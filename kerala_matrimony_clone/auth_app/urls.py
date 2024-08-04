
from django.urls import path
from . views import *

urlpatterns = [
    path('',index,name='index'),
    path('sign_up/',sign_up,name='sign_up'),
    path('register2/',register2,name='register2'),
    path('register3/',register3,name='register3'),
    path('register4/',register4,name='register4'),
    path('register5/',register5,name='register5'),
    path('register6/',register6,name='register6'),
    path('create_user_account/',create_user_account,name='create_user_account'),
    path('login_user/',login_user,name='login_user'),
    path('check_values/',check_values),
    path('logout_user/',logout_user,name='logout_user'),
    path('update_profile/<int:id>/',update_profile),
    path('edit_profile/<int:id>/',edit_profile,name='edit_profile'),
    
]
