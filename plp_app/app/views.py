from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
