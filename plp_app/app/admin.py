from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Admin)
admin.site.register(models.Profile)
admin.site.register(models.Public)
admin.site.register(models.Private)
admin.site.register(models.PaymentDetails)
admin.site.register(models.Category)
admin.site.register(models.CategoriesLiked)
admin.site.register(models.Course)
admin.site.register(models.CoursesMade)
admin.site.register(models.CoursesEnrolled)
admin.site.register(models.Rating)
admin.site.register(models.TeachingUnit)
admin.site.register(models.Material)
admin.site.register(models.Written)
admin.site.register(models.Photo)
admin.site.register(models.Audio)
admin.site.register(models.Video)
admin.site.register(models.LiveChat)
admin.site.register(models.Schedule)
admin.site.register(models.Participant)



