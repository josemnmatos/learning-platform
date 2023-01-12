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
        
    def test_if_the_courses_were_created(self):
        # Get the count of all the courses
        count = models.Course.objects.all().count()
        self.assertEqual(count, 5)
            
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
        # Check if it has the info of the user we created
        self.assertEqual(response.context['public'].name, self.public.name)
        self.assertEqual(response.context['public'].surname, self.public.surname)
        self.assertEqual(response.context['public'].avatar, self.public.avatar)

    def test_error_user_profiel_page(self):
        # Get the profile page for a random id
        profile_url = reverse('viewProfile', kwargs={'id': 5})
        response = self.client.get(profile_url)
        # Because it is a redirect it has code 302
        self.assertEqual(response.status_code, 302)