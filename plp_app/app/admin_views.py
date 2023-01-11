from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import models
import sweetify as s
from . import views
from django.http import HttpResponseNotFound


def adminDashboard(request):
    if request.user.is_staff == False:
        return HttpResponseNotFound()
    return render(request, 'app/adminDashboard.html')


def addUser(request):
    if request.user.is_staff == False:
        return HttpResponseNotFound()
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password1']

        if password1 == password2:
            try:
                myuser = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
                myuser.save()
            except:
                s.error(request, "Could not create the account.")
                return redirect('adminDashboard')

            if request.POST['isStaff'] == 'on':
                myuser.is_staff = True
                myuser.is_superuser = True

            # create public and private profile views for the user
            newprofile = models.Profile(userId=myuser)
            newprofile.save()

            newpublic = models.Public(
                profileId=newprofile, name=first_name, surname=last_name, avatar=1)
            newprivate = models.Private(profileId=newprofile, email=email)
            newpublic.save()
            newprivate.save()

            s.success(
                request, "User created.")

            return redirect('adminDashboard')

        else:
            s.error(request, "Passwords do not match.")

    return render(request, 'app/addUser.html')


def deleteUser(request):
    if request.user.is_staff == False:
        return HttpResponseNotFound()
    return render(request, "app/deleteUser.html")
