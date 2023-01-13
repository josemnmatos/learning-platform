from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.userId.username


class Profile(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.userId.username


class Public(models.Model):
    profileId = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    avatar = models.SmallIntegerField()
    createdDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name + ' ' + self.surname


class Private(models.Model):
    profileId = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.email


class PaymentDetails(models.Model):
    privateId = models.ForeignKey(Private, on_delete=models.CASCADE, null=True, blank=True)
    cardNumber = models.CharField(max_length=16)
    expirationMonth = models.SmallIntegerField()
    expirationYear = models.SmallIntegerField()
    cvv = models.SmallIntegerField()

    def __str__(self):
        return '**** ' + self.cardNumber[-4:]


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class CategoriesLiked(models.Model):
    privateId = models.ForeignKey(Private, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.privateId.profileId.userId.username + ' - ' + self.categoryId.category


class Course(models.Model):
    categoryId = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    averageMasterTime = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.name


class CoursesMade(models.Model):
    publicId = models.ForeignKey(Public, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.publicId.profileId.userId.username + ' <- ' + self.courseId.name


class CoursesEnrolled(models.Model):
    privateId = models.ForeignKey(Private, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.PROTECT)
    paymentMethod = models.ForeignKey(PaymentDetails, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.privateId.profileId.userId.username + ' -> ' + self.courseId.name


class Rating(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.SmallIntegerField()

    def __str__(self):
        return str(self.rating) + '/5 - ' + self.comment

 
class TeachingUnit(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.courseId.name + ' - ' + self.name


class Material(models.Model):
    unitId = models.ForeignKey(TeachingUnit, on_delete=models.CASCADE)
    materialName = models.CharField(max_length=100)
    content = models.TextField(null=True)
    type=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.unitId.courseId.name + ' - ' + self.unitId.name


class Written(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    
    title = models.TextField(default="No text")

    def __str__(self):
        return self.title


class Photo(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)



class Audio(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    time = models.IntegerField()

    def __str__(self):
        return self.time


class Video(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    time = models.IntegerField()


class LiveChat(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    maxParticipants = models.SmallIntegerField()
    chat_enable = models.BooleanField(default=False)

    def __str__(self):
        return self.courseId.name + ' - ' + str(self.maxParticipants)


class Schedule(models.Model):
    liveChatId = models.ForeignKey(LiveChat, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.liveChatId.courseId.name + ' - ' + self.date + ' ' + self.time


class Participant(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    liveChatId = models.ForeignKey(LiveChat, on_delete=models.CASCADE)

    def __str__(self):
        return self.userId.username + ' - ' + self.liveChatId.courseId.name
