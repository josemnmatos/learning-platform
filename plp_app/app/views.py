from itertools import chain
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import models

# Create your views here.


def home(request):
    return render(request, "app/landing.html")


def register(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password1']

        if password1 == password2:
            myuser = User.objects.create_user(username, email, password1)

            myuser.save()

            messages.success(
                request, "Your account has been sucessfully created.")

            return redirect('loginpage')

        else:
            messages.error(request, "Passwords do not match.")

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
        teachingUnits = models.TeachingUnit.objects.filter(
            courseId__exact=course[0])
        # Find the Live Chat
        liveChat = models.LiveChat.objects.filter(courseId__exact=course[0])
        # If it doesn't exist yet
        if not liveChat:
            liveChat = [None]
        # Find the ratings
        ratings = models.Rating.objects.filter(courseId__exact=course[0])
        return render(request, "app/coursePage.html", {'course': course[0],
                                                       'teachingUnits': teachingUnits,
                                                       'liveChat': liveChat[0],
                                                       'ratings': ratings})

def teachingUnitPage(request, id):
    # Gets the unit with the exact id passed in
    unit = models.TeachingUnit.objects.filter(id__exact=id)
    # If it doesn't find any
    if not unit:
        messages.error(request, "Teaching unit doesn't exist.")
        return redirect('home')
    else:
        # Find the materials
        materials = models.Material.objects.filter(unitId__exact=unit[0])
        # return page
        return render(request, "app/teachingUnit.html", {'unit': unit[0],
                                                         'materials': materials})


def searchResults(request):
    # Get the name of the course through the GET request
    if request.method == 'GET':
        name = request.GET['name']
        
        # Get all the public objects that contain the name in name
        names = models.Public.objects.filter(name__icontains=name)
        # Get all the public objects that contain the name in surname
        surnames = models.Public.objects.filter(surname__icontains=name)
        # Join them and sort by name
        publics = sorted(names.union(surnames), key=lambda profile: profile.name)
        
        # Get all the course objects that contain the name in name
        courses = models.Course.objects.filter(name__icontains=name).order_by('name')
        
        return render(request, "app/searchResults.html", {'courses': courses, 'publics': publics})
    # If it isn't a GET request go to home page
    return redirect('home')


def viewProfile(request, id):
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
            coursesMade = models.CoursesMade.objects.filter(publicId__exact=public[0].id)
            return render(request, "app/viewProfile.html", {'public': public[0], 'coursesMade': coursesMade})

def chat_on(request):
    return render(request,"app/chat.html")

def own_course_page(request):
    return render(request,"app/own_course.html")

def course_def(request):
    return render(request,"app/course_def.html")

def def_chat(request):
    return render(request,"app/live_chat_def.html")
