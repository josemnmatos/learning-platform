from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import models

# Create your views here.


def home(request):
    return render(request, "app/landing.html")


def register(request):

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
                print("1")
                newUserId=myuser.id
                print("1")
                #create public and private profile views for the user
                newprofile=models.Profile(userId=myuser)
                print("2")
                newprofile.save()
                print("2")
                newpublic=models.Public(profileId=newprofile,name=first_name,surname=last_name,avatar=1)
                print("3")
                newprivate=models.Private(profileId=newprofile,email=email)
                print("3")
                newpublic.save()
                print("3")
                newprivate.save()
                print("4")


            except:
                messages.error(
                    request, "Something went wrong when creating your account")

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
            return render(request, "app/landing.html", {'fname': fname})

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
        # Find the creator
        courseMade = models.CoursesMade.objects.filter(courseId__exact=id)
        # Check if the current user is the user of the profile
        thisUser = False
        if request.user.is_authenticated:
            if courseMade[0].publicId.profileId.userId.id == request.user.id:
                thisUser = True
        print(thisUser)
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
                                                       'creator': courseMade[0].publicId,
                                                       'teachingUnits': teachingUnits,
                                                       'liveChat': liveChat[0],
                                                       'ratings': ratings,
                                                       'thisUser': thisUser})


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
        written = models.Written.objects.filter(materialId__exact=materials[0])
        video = models.Video.objects.filter(materialId__exact=materials[0])
        # return page
        return render(request, "app/teachingUnit.html", {'unit': unit[0],
                                                         'materials': materials,
                                                         'written': written,
                                                         'video': video})


def searchResults(request):
    # Get the name of the course through the GET request
    if request.method == 'GET':
        name = request.GET['name']

        # Get all the public objects that contain the name in name
        names = models.Public.objects.filter(name__icontains=name)
        # Get all the public objects that contain the name in surname
        surnames = models.Public.objects.filter(surname__icontains=name)
        # Join them and sort by name
        publics = sorted(names.union(surnames),
                         key=lambda profile: profile.name)

        # Get all the course objects that contain the name in name
        courses = models.Course.objects.filter(
            name__icontains=name).order_by('name')

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
        # Check if the current user is the user of the profile
        thisUser = False
        if request.user.is_authenticated:
            if profile[0].userId.id == request.user.id:
                thisUser = True

        coursesMade = models.CoursesMade.objects.filter(
            publicId__exact=public[0].id)
        # Get the number of students
        students = 0
        for courseMade in coursesMade:
            students += models.CoursesEnrolled.objects.filter(
                courseId__exact=courseMade.courseId).count()
        # Get the average rating
        ratings = models.Rating.objects.none()
        for courseMade in coursesMade:
            ratings = ratings | models.Rating.objects.filter(
                courseId__exact=courseMade.courseId)

        numRatings = 0
        totalRatings = 0
        for rating in ratings:
            numRatings += 1
            totalRatings += rating.rating
        avgRating = 0
        if numRatings > 0:
            avgRating = totalRatings/numRatings
        return render(request, "app/viewProfile.html", {'public': public[0], 'coursesMade': coursesMade, 'thisUser': thisUser,
                                                        'students': students, 'numRatings': numRatings, 'avgRating': avgRating})


def chat_on(request):
    return render(request, "app/chat.html")


def own_course_page(request):
    return render(request, "app/own_course.html")


def course_def(request):
    return render(request, "app/course_def.html")


def def_chat(request):
    return render(request, "app/live_chat_def.html")


def courseCreated(request, id):
    profile = models.Profile.objects.filter(userId__exact=id)
    public = models.Public.objects.filter(profileId__exact=profile[0].id)
    coursesMade = models.CoursesMade.objects.filter(
        publicId__exact=public[0].id)

    # Check if the current user is the user of the profile
    thisUser = False
    if request.user.is_authenticated:
        if profile[0].userId.id == request.user.id:
            thisUser = True

    students = []
    liveChats = []
    moneyEarned = []
    for courseMade in coursesMade:
        # Students
        numStudents = models.CoursesEnrolled.objects.filter(
            courseId__exact=courseMade.courseId).count()
        students.append(numStudents)
        # Live chats
        liveChat = models.LiveChat.objects.filter(
            courseId__exact=courseMade.courseId)
        liveChats.append(liveChat)
        # Money Earned
        moneyEarned.append(numStudents * courseMade.courseId.price)

    data = zip(coursesMade, students, liveChats, moneyEarned)
    return render(request, "app/courseCreated.html", {'coursesMade': coursesMade, 'data': data, 'thisUser': thisUser, 'userId': id})


def payments(request):
    if request.user.is_authenticated:
        profile = models.Profile.objects.filter(userId__exact=request.user.id)
        private = models.Private.objects.filter(profileId__exact=profile[0].id)
        enrolledCourses = models.CoursesEnrolled.objects.filter(
            privateId__exact=private[0].id)
        paymentDetails = models.PaymentDetails.objects.filter(
            privateId__exact=private[0].id)
        # Get the total amount spent
        total = 0
        for course in enrolledCourses:
            total += course.courseId.price

        return render(request, "app/payments.html", {'enrolledCourses': enrolledCourses, 'paymentDetails': paymentDetails, 'total': total, 'thisUser': True, 'userId': request.user.id})
    return redirect('home')


def rateCourse(request, id):
    course = models.Course.objects.filter(id__exact=id)
    if not course:
        messages.error(request, "Course doesn't exist.")
        return redirect('home')

    return render(request, "app/rateCourse.html", {'course': course[0]})


def saveRating(request):
    if request.method == "POST":
        userId = request.POST['userId']
        courseId = request.POST['courseId']
        rating = request.POST['rating']
        comment = request.POST['comment']

        user = models.User.objects.filter(id__exact=userId)
        course = models.Course.objects.filter(id__exact=courseId)

        newRating = models.Rating(
            userId=user[0], courseId=course[0], comment=comment, rating=rating)
        newRating.save()

    return redirect('coursePage', courseId)


def createNewCourse(request):
    categories = models.Category.objects.all()
    return render(request, "app/createNewCourse.html", {'categories': categories})


def saveNewCourse(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST['name']
            averageMasterTime = request.POST['averageMasterTime']
            price = request.POST['price']
            category = request.POST['category']
            # Get the category
            categoryId = models.Category.objects.filter(id__exact=category)
            # Create the new Course
            newCourse = models.Course(
                name=name, averageMasterTime=averageMasterTime, price=price, categoryId=categoryId[0])
            newCourse.save()
            # Add it to the courses made
            profileId = models.Profile.objects.filter(
                userId__exact=request.user.id)
            publicId = models.Public.objects.filter(
                profileId__exact=profileId[0])
            newCourseMade = models.CoursesMade(
                publicId=publicId[0], courseId=newCourse)
            newCourseMade.save()
            return redirect('coursePage', newCourse.id)
    return redirect('home')


def coursesEnrolled(request):
    if request.user.is_authenticated:
        profile = models.Profile.objects.filter(userId__exact=request.user.id)
        private = models.Private.objects.filter(profileId__exact=profile[0].id)
        coursesEnrolled = models.CoursesEnrolled.objects.filter(
            privateId__exact=private[0].id)

        return render(request, "app/coursesEnrolled.html", {'coursesEnrolled': coursesEnrolled, 'thisUser': True, 'userId': request.user.id})
    return redirect('home')


def editCourse(request, id):
    if request.user.is_authenticated:
        # Check the course
        course = models.Course.objects.filter(id__exact=id)
        # If course doesn't exist
        if not course:
            messages.error(request, "Course doesn't exist.")
            return redirect('home')
        # Check if the user was the one who made it
        profile = models.Profile.objects.filter(userId__exact=request.user.id)
        public = models.Public.objects.filter(profileId__exact=profile[0].id)
        courseMade = models.CoursesMade.objects.filter(
            publicId__exact=public[0].id, courseId__exact=id)
        print(courseMade)
        # If it's not theirs
        if not courseMade:
            messages.error(request, "You can't edit this course")
            return redirect('home')
        # Get all the categories except the one the course has
        categories = models.Category.objects.all().exclude(
            id=course[0].categoryId.id)
        # If all okay load the page to edit it
        return render(request, "app/editCourse.html", {'course': course[0], 'categories': categories, 'thisUser': True, 'userId': request.user.id})

    return redirect('home')


def saveCourseChanges(request):
    if request.method == "POST":
        name = request.POST['name']
        averageMasterTime = request.POST['averageMasterTime']
        price = request.POST['price']
        category = request.POST['category']
        courseId = request.POST['courseId']
        # Get the category
        categoryId = models.Category.objects.filter(id__exact=category)
        # Get the course
        course = models.Course.objects.get(id=courseId)
        course.name = name
        course.averageMasterTime = averageMasterTime
        course.price = price
        course.categoryId = categoryId[0]
        course.save()
        return redirect('coursePage', courseId)

    return redirect('home')
