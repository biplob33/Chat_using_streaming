from django.urls import path
from log_reg.views import login,auth_my_user,auth_register,register,logout
urlpatterns = [
    path(r'login/', login),
    path(r'auth/',auth_my_user),
    path(r'register/',register),
    path(r'auth_register/',auth_register),
    path(r'logout/',logout),
]