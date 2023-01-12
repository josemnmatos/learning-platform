from django.test import TestCase, Client
from django.urls import reverse
from .. import models

# Create your tests here.

class TestRegister(TestCase):

    def setUp(self):
        # Get the client object and the url
        self.client = Client()
        self.register_url = reverse('register')
        # Create test data
        self.userData = {'first_name': 'Test',
                        'last_name': 'User',
                        'username': 'testUser',
                        'email': 'testUser@test.com',
                        'password1': 'testUser',
                        'password2': 'testUser'}
        
    def test_create_new_user(self):
        # Get the response to a POST request on the register page
        response = self.client.post(self.register_url, self.userData)
        # Because it is a redirect it has code 302
        self.assertEqual(response.status_code, 302)
        # Check if a user was created as well as a profile, public and private
        user = models.User.objects.get(id=1)
        profile = models.Profile.objects.get(userId=user.id)
        public = models.Public.objects.get(profileId=profile.id)
        private = models.Private.objects.get(profileId=profile.id)
        # Assert results
        self.assertEqual(user.username,'testUser')
        self.assertEqual(public.name,'Test')
        self.assertEqual(private.email, 'testUser@test.com')
        

class TestLogin(TestCase):
    
    def setUp(self):
        # Get the client object and the url
        self.client = Client()
        self.login_url = reverse('loginpage')
        # Create test data
        self.userData = {'username': 'testUser',
                        'password1': 'testUser'}
        self.badUserData = {'username': 'wrongCredentials',
                            'password1': 'wrongCredentials'}
        # Create a user
        self.user = models.User.objects.create_user(username=self.userData['username'], password=self.userData['password1'])
        
    def test_if_user_is_created(self):
        # Get the user with id=1 (in tests the db is empty so it will be the first one)
        user = models.User.objects.get(id=1)
        # Check if it has the same username
        self.assertEqual(user.username, 'testUser')
        
    def test_successful_login(self):
        # Get the response to a POST request on the login page
        response = self.client.post(self.login_url, self.userData)
        # Because it is a render to page landing.html it has code 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/landing.html')
        
    def test_unsuccessful_login(self):
        # Get the response to a POST request on the login page
        response = self.client.post(self.login_url, self.badUserData)
        # Because it is a redirect it has code 302
        self.assertEqual(response.status_code, 302)
        

class TestSearchResults(TestCase):
    
    def setUp(self):
        # Get the client object and the url
        self.client = Client()
        self.results_url = reverse('searchResults')
        # Create test data
        # Create a category
        self.category = models.Category.objects.create(category='General')
        # Create courses
        num = 5
        for i in range(num):
            models.Course.objects.create(categoryId=self.category, name="Test Course "+str(i),
                                         averageMasterTime=i+5, price=i, description="Test Description"+str(i))
        
    def test_successful_results(self):
        # Get the response to a GET request on the results page
        response = self.client.get(self.results_url, {'name': 'test'})
        # Because it is a render to page searchResults.html it has code 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/searchResults.html')
        # Check that it had 5 result in courses
        self.assertEqual(len(response.context['courses']), 5)
        
    def test_unsuccessful_results(self):
        # Get the response to a POST request on the results page
        response = self.client.post(self.results_url, {'name': 'test'})
        # Because it is a redirect it has code 302
        self.assertEqual(response.status_code, 302)
        

class TestProfile(TestCase):
    
    def setUp(self):
        # Get the client object and the url
        self.client = Client()
        # Create test data
        # Create a user
        self.user = models.User.objects.create_user(username='testUser', password='testUser')
        # Create it's profile, public and private
        self.profile = models.Profile.objects.create(userId=self.user)
        self.public = models.Public.objects.create(profileId=self.profile, name='Test', surname='User', avatar=1)
        self.private = models.Private.objects.create(profileId=self.profile, email='testUser@test.com')
        
    def test_user_profile_page(self):
        # Get the profile page for the id of the user
        profile_url = reverse('viewProfile', kwargs={'id': self.user.id})
        response = self.client.get(profile_url)
        # Because it is a render to page viewProfile.html it has code 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/viewProfile.html')
        # Check if it has the info of the user created
        self.assertEqual(response.context['public'].name, self.public.name)
        self.assertEqual(response.context['public'].surname, self.public.surname)
        self.assertEqual(response.context['public'].avatar, self.public.avatar)

    def test_error_user_profiel_page(self):
        # Get the profile page for a random id
        profile_url = reverse('viewProfile', kwargs={'id': 5})
        response = self.client.get(profile_url)
        # Because it is a redirect it has code 302
        self.assertEqual(response.status_code, 302)
        

class TestEnrollCourse(TestCase):
    
    def setUp(self):
        # Get the client object and the url
        self.client = Client()
        self.payments_url = reverse('payments')
        # Create user test data
        self.creatorData = {'username': 'courseCreator',
                            'password': 'courseCreator'}
        self.userData = {'username': 'courseEnroller',
                        'email': 'courseEnroller@test.com',
                        'password': 'courseEnroller'}
        # Create the users
        self.creator = models.User.objects.create_user(username=self.creatorData['username'], password=self.creatorData['password'])
        self.user = models.User.objects.create_user(username=self.userData['username'], password=self.userData['password'])
        # Create the users profile and private
        self.userProfile = models.Profile.objects.create(userId=self.user)
        self.userPrivate = models.Private.objects.create(profileId=self.userProfile, email=self.userData['email'])
        # Create a category
        self.category = models.Category.objects.create(category='General')
        
    def test_enroll_free_course(self):
        # Create a free course
        course = models.Course.objects.create(categoryId=self.category, name="Test Course",
                                                averageMasterTime=5, price=0, description="Test Description")
        # Make it so that the user is enrolled in the course
        models.CoursesEnrolled.objects.create(privateId=self.userPrivate, courseId=course)
        # Login the user 
        self.client.login(username=self.userData['username'], password=self.userData['password'])
        # Go to the payments page and check if there was an enrolled course without a payment method
        response = self.client.get(self.payments_url)
        self.assertEqual(response.context['enrolledCourses'][0].paymentMethod, None)
        
    def test_enroll_paid_course(self):
        # Create a paid course
        course = models.Course.objects.create(categoryId=self.category, name="Test Course",
                                                averageMasterTime=5, price=5, description="Test Description")
        # Create a payment detail
        paymentDetail = models.PaymentDetails.objects.create(privateId=self.userPrivate, cardNumber='1234123412341234',
                                                             expirationMonth=1, expirationYear=24, cvv=123)
        # Make it so that the user is enrolled in the course
        models.CoursesEnrolled.objects.create(privateId=self.userPrivate, courseId=course, paymentMethod=paymentDetail)
        # Login the user 
        self.client.login(username=self.userData['username'], password=self.userData['password'])
        # Go to the payments page and check if there was an enrolled course with a payment method
        response = self.client.get(self.payments_url)
        self.assertEqual(response.context['enrolledCourses'][0].paymentMethod, paymentDetail)


class TestManagePaymentDetails(TestCase):
    
    def setUp(self):
        # Get the client object and the url
        self.client = Client()
        self.manage_payments_url = reverse('managePaymentDetails')
        # Create user test data
        self.userData = {'username': 'testUser',
                        'email': 'testUser@test.com',
                        'password': 'testUser'}
        self.cardData = {'cardNumber': '1234123412341234', 
                         'expirationMonth': 12,
                         'expirationYear': 24,
                         'cvv': 123 }
        # Create the user
        self.user = models.User.objects.create_user(username=self.userData['username'], password=self.userData['password'])
        # Create the users profile and private
        self.userProfile = models.Profile.objects.create(userId=self.user)
        self.userPrivate = models.Private.objects.create(profileId=self.userProfile, email=self.userData['email'])
     
    def test_add_card(self):
        # Create a payment detail
        paymentDetail = models.PaymentDetails.objects.create(privateId=self.userPrivate, cardNumber=self.cardData['cardNumber'], expirationMonth=self.cardData['expirationMonth'],
                                                             expirationYear=self.cardData['expirationYear'], cvv=self.cardData['cvv'],)
        # Login the user 
        self.client.login(username=self.userData['username'], password=self.userData['password'])
        # Do a GET request in the managePaymentsDetails
        response = self.client.get(self.manage_payments_url)
        # Because it is a render to page managePaymentDetails.html it has code 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/managePaymentDetails.html')
        # Check if the payment detail is displayed
        self.assertEquals(response.context['paymentDetails'][0], paymentDetail)
        
