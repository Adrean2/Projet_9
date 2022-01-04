from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.login_page,name="login"),
    path('logout/',views.logout_user,name='logout'),
    path('signup/',views.signup_page,name='signup')
]