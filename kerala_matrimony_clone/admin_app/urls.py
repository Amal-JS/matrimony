
from django.urls import include, path
from . views import *

urlpatterns = [
    path('',index,name='admin_index'),
    path('admin_login/',admin_login,name='admin_login'),
    path('admin_logout/',admin_logout,name='admin_logout'),
     path('user_details/<int:id>/', user_details, name='user_details'),
]

