from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('loginpage', views.loginpage, name="loginpage"),
    path('signout', views.signout, name="signout"),
    path('course/<id>', views.coursePage, name='coursePage'),
    path('viewProfile/<id>', views.viewProfile, name='viewProfile'),
    path('searchResults', views.searchResults, name='searchResults'),
    path('teachingUnit/<id>', views.teachingUnitPage, name='teachingUnitPage'),
    path('chat',views.chat_on,name="chat online"),
    path('own_course',views.own_course_page,name="course"),
    path('course_def',views.course_def,name="Definitions"),
    path('live_chat_def',views.def_chat,name="Chat definitions"),
    path('courseCreated/<id>',views.courseCreated,name="courseCreated"),
    path('createNewCourse',views.createNewCourse,name="createNewCourse"),
    path('saveNewCourse',views.saveNewCourse,name="saveNewCourse"),
    path('coursesEnrolled',views.coursesEnrolled,name="coursesEnrolled"),
    path('editCourse/<id>',views.editCourse,name="editCourse"),
    path('saveCourseChanges',views.saveCourseChanges,name="saveCourseChanges"),
    path('enrollCourse/<id>',views.enrollCourse,name="enrollCourse"),
    path('saveEnrollment',views.saveEnrollment,name="saveEnrollment"),
    path('rateCourse/<id>',views.rateCourse,name="rateCourse"),
    path('saveRating',views.saveRating,name="saveRating"),
    path('payments',views.payments,name="payments"),
    path('addTeachingUnitWritten/<id>',views.addTeachingUnitWritten,name="add TUW"),
    path('addTeachingUnitVideo/<id>',views.addTeachingUnitVideo,name="add TUV"),
    path('editProfile',views.editProfile,name="editProfile"),
    path('saveProfileChanges',views.saveProfileChanges,name="saveProfileChanges"),
    path('managePaymentDetails',views.managePaymentDetails,name="managePaymentDetails"),
    path('saveNewPaymentDetail',views.saveNewPaymentDetail,name="saveNewPaymentDetail"),
    path('deletePaymentDetail',views.deletePaymentDetail,name="deletePaymentDetail"),
    
    
]
