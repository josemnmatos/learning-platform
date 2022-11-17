from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('loginpage',views.loginpage, name="loginpage"),
    path('signout',views.signout, name="signout"),
]
