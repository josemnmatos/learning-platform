from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('loginpage',views.loginpage, name="loginpage"),
    path('signout',views.signout, name="signout"),
    path('course/<id>', views.coursePage, name='coursePage'),
    path ('viewProfile/<id>', views.viewProfile, name='viewProfile'),
]
