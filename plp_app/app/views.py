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
        # If it doesn't exist yet
        if not liveChat:
            liveChat = [None]
        # Find the ratings
        ratings = models.Rating.objects.filter(courseId__exact = course[0])
        return render(request, "app/coursePage.html", {'course': course[0], 
                                                       'teachingUnits': teachingUnits,
                                                       'liveChat': liveChat[0],
                                                       'ratings': ratings})

def searchCourse(request):
    # Get the name of the course through the GET request
    if request.method == 'GET':
        name = request.GET['name'] 
        # Get all the course objects that contain the name in name
        courses = models.Course.objects.filter(name__icontains=name)
        # If it doesn't have a match return to home page
        if not courses:
            messages.error(request, "No Course with that name found")
            return redirect('home')
        # If found return the searchUser page with the results
        else:
            return render(request, "app/searchCourse.html", {'courses': courses})
    # If it isn't a GET request go to home page
    return redirect('home')

def searchUser(request):
    # Get the name of the user through the GET request
    if request.method == 'GET':
        name = request.GET['name'] 
        # Get all the public objects that contain the name in name
        publics = models.Public.objects.filter(name__icontains=name)
        # If it doesn't find anything search for the name in surname
        if not publics:
            publics = models.Public.objects.filter(surname__icontains=name)
        # If it doesn't have a match at all return to home page
        if not publics:
            messages.error(request, "No User with that name found")
            return redirect('home')
        # If found return the searchUser page with the results
        else:
            return render(request, "app/searchUser.html", {'publics': publics})
    # If it isn't a GET request go to home page
    return redirect('home')
        
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
            coursesMade = models.CoursesMade.objects.filter(publicId__exact = public[0].id)
            return render(request, "app/viewProfile.html", {'public': public[0], 'coursesMade': coursesMade})
