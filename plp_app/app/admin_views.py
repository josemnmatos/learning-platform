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
                s.error(request, "Could not create the user.",
                        button="OK", timer=2000)
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

            s.success(request, "User created.",
                      button="OK", timer=2000)

            return redirect('adminDashboard')

        else:
            s.error(request, "Passwords do not match.",
                    button="OK", timer=2000)

    return render(request, 'app/addUser.html')


def deleteUser(request):

    current_user = request.user

    if current_user.is_staff == False:
        return HttpResponseNotFound()

    # check if user is trying to delete itself
    if request.method == "POST":
        username = request.POST['username']
        if current_user.get_username() == username:
            s.error(request, "You cannot delete your own account.",
                    button="OK", timer=2000)
            return redirect('adminDashboard')
        else:
            # delete user, rest will follow as model is cascade
            try:
                # delete all courses created by that user
                user = models.User.objects.get(username=username)
                profile = models.Profile.objects.get(userId=user.id)
                public= models.Public.objects.get(profileId=profile.id)
                courses_created=models.CoursesMade.objects.filter(publicId=public.id)
                for course_created in courses_created:
                    course=models.Course.objects.get(pk=course_created.courseId.id)
                    course.delete()
                user.delete()

            except:

                s.error(request, "User could not be deleted.",
                        button="OK", timer=2000)
                return redirect('adminDashboard')

            s.success(request, "User deleted.",
                      button="OK", timer=2000)
            return redirect('adminDashboard')

    return render(request, "app/deleteUser.html")
