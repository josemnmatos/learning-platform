from django.db import models

# Create your models here.
class User (models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class Admin(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Profile(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Public(models.Model):
    profileId = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    avatar = models.SmallIntegerField()
    createdDate = models.DateField(auto_now_add=True)
    
class Private(models.Model):
    profileId = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    
class PaymentDetails(models.Model):
    privateId = models.ForeignKey(Private, on_delete=models.CASCADE)
    cardNumber = models.CharField(max_length=16)
    expirationMonth = models.SmallIntegerField()
    expirationYear = models.SmallIntegerField()
    cvv = models.SmallIntegerField()
    
class Category(models.Model):
    category = models.CharField(max_length=50)
    
class CategoriesLiked(models.Model):
    privateId = models.ForeignKey(Private, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(Category)
        
class Course(models.Model):
    categoryId = models.ForeignKey(Category)
    name = models.CharField(max_length=100)
    averageMasterTime = models.SmallIntegerField()
    price = models.DecimalField(decimal_places=2)
    
class CoursesMade(models.Model):
    publicId = models.ForeignKey(Public, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    
class CoursesEnrolled(models.Model):
    privateId = models.ForeignKey(Private, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    
class Rating(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.SmallIntegerField(min_value=0, max_value=5)
    
class TeachingUnit(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    
class Material(models.Model):
    unitId = models.ForeignKey(TeachingUnit, on_delete=models.CASCADE)
    
class Written(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    content = models.TextField()
    length = models.IntegerField()
    
class Photo(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    width = models.IntegerField()
    height = models.IntegerField()
    label = models.CharField(max_length=50)
    
class Audio(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    time = models.IntegerField()
    
class Video(models.Model):
    materialId = models.ForeignKey(Material, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=20)
    time = models.IntegerField()
    
class LiveChat(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    maxParticipants = models.SmallIntegerField()
    
class Schedule(models.Model):
    liveChatId = models.ForeignKey(LiveChat, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    
class Participants(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    liveChatId = models.ForeignKey(LiveChat, on_delete=models.CASCADE)