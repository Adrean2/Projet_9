from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('',views.logout_user,name='logout'),
    path('signup/',views.signup_page,name='signup')
]