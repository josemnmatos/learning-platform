from django.contrib import admin
from .models import User, Admin, Profile, Public, Private, PaymentDetails, Category, CategoriesLiked, Course, CoursesMade, CoursesEnrolled, Rating, TeachingUnit, Material, Written, Photo, Audio, Video, LiveChat, Schedule, Participant

# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Profile)
admin.site.register(Public)
admin.site.register(Private)
admin.site.register(PaymentDetails)
admin.site.register(Category)
admin.site.register(CategoriesLiked)
admin.site.register(Course)
admin.site.register(CoursesMade)
admin.site.register(CoursesEnrolled)
admin.site.register(Rating)
admin.site.register(TeachingUnit)
admin.site.register(Material)
admin.site.register(Written)
admin.site.register(Photo)
admin.site.register(Audio)
admin.site.register(Video)
admin.site.register(LiveChat)
admin.site.register(Schedule)
admin.site.register(Participant)



