from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import models

# Create your views here.


def home(request):
    return render(request, "app/index.html")


def register(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        myuser = User.objects.create_user(username, email, password1)

        myuser.save()

        messages.success(request, "Your account has been sucessfully created.")

        return redirect('loginpage')

    return render(request, "app/register.html")


def loginpage(request):

    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            fname = user.username
            return render(request, "app/index.html", {'fname': fname})

        else:
            messages.error(request, "Wrong credentials.")
            return redirect('home')

    return render(request, "app/loginpage.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out sucessfully.")
    return redirect('home')


def coursePage(request, id):
    # Gets the course with the exact id passed in
    course = models.Course.objects.filter(id__exact=id)
    # If it doesn't find any
    if not course:
        messages.error(request, "Course doesn't exist")
        return redirect('home')
    else:
        # Find the teaching Units
        teachingUnits = models.TeachingUnit.objects.filter(courseId__exact = course[0])
        #Find the Live Chat
        liveChat = models.LiveChat.objects.filter(courseId__exact = course[0])
        if not liveChat:
            liveChat = [None]
        # Find the ratings
        ratings = models.Rating.objects.filter(courseId__exact = course[0])
        return render(request, "app/coursePage.html", {'course': course[0], 
                                                       'teachingUnits': teachingUnits,
                                                       'liveChat': liveChat[0],
                                                       'ratings': ratings})
        
def viewProfile (request, id):
    # Gets the profile with the exact id passed in
    profile = models.Profile.objects.filter(userId__exact=id)
    # If it doesn't find any profile
    if not profile:
        messages.error(request, "User doesn't exist")
        return redirect('home')
    else:
        public = models.Public.objects.filter(profileId__exact=profile[0].id)
        if not public:
            messages.error(request, "Error finding public profile")
            return redirect('home')
        else:
            return render(request, "app/viewProfile.html", {'public': public[0]})

def searchCourse(request):
    if request.method == 'GET':
        name = request.GET['name'] 
        courses = models.Course.objects.filter(name__icontains=name)
        if not courses:
            messages.error(request, "No Course with that name found")
            return redirect('home')
        else:
            return render(request, "app/searchCourse.html", {'courses': courses})
    return redirect('home')

def searchUser(request):
    if request.method == 'GET':
        name = request.GET['name'] 
        publics = models.Public.objects.filter(name__icontains=name)
        if not publics:
            messages.error(request, "No User with that name found")
            return redirect('home')
        else:
            return render(request, "app/searchUser.html", {'publics': publics})
    return redirect('home')
