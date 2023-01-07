from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('loginpage', views.loginpage, name="loginpage"),
    path('signout', views.signout, name="signout"),
    path('course/<id>', views.coursePage, name='coursePage'),
    path('viewProfile/<id>', views.viewProfile, name='viewProfile'),
    path('searchResults', views.searchResults, name='searchResults'),
    path('teachingUnit/<id>', views.teachingUnitPage, name='teachingUnitPage'),
    path('chat',views.chat_on,name="chat online"),
    path('own_course',views.own_course_page,name="course"),
    path('course_def',views.course_def,name="Definitions"),
    path('live_chat_def',views.def_chat,name="Chat definitions"),
    path('courseCreated',views.courseCreated,name="courseCreated"),

]
