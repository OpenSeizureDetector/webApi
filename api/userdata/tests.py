from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import json


class UserRegistrationAPIViewTestCase(APITestCase):
    url = "/api/accounts/register/"

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "confirm_password": "INVALID_PASSWORD"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code, response.content)

    def test_user_registration(self):
        """
        Test to verify that a post call with valid data
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "testpwxyz",
            "password_confirm": "testpwxyz"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "testpwxyz",
            "password_confirm": "testpwxyz"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code, response.content)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password": "testpwxyz",
            "password_confirm": "testpwxyz"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code, response.content)

class UserLoginAPIViewTestCase(APITestCase):
    url = "/api/accounts/login/"

    def setUp(self):
        print("Running UserLoginAPIViewTestCase....");
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"login": self.username}, secure=True, follow=True)
        #print("test_authentication_without_password: response=%s, %s" %
        #      (str(response.status_code), str(response.content)))
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"login": self.username, "password": "wrong_password"}, secure=True, follow=True)
        #print("test_authentication_with_wrong_password: response=%s, %s" %
        #      (str(response.status_code), str(response.content)))
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"login": self.username, "password": self.password}, secure=True, follow=True)
        #print("test_authentication_with_valid_data: response=%s, %s" %
        #      (str(response.status_code), str(response.content)))
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))





class ProfileAPIViewTestCase(APITestCase):
    def url(self, key):
        #return reverse("users:token", kwargs={"key": key})
        return("/api/profile/")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password, is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.user_2 = User.objects.create_user("mary", "mary@earth.com", "super_secret")
        self.token_2 = Token.objects.create(user=self.user_2)

    def tearDown(self):
        self.user.delete()
        self.token.delete()
        self.user_2.delete()
        self.token_2.delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get(self):
        print("running ProfileApiViewTest - test_get()")

        # Test that unauthorized access returns 401
        urlStr = self.url("")
        print("test_get - url="+urlStr)
        self.client.credentials(HTTP_AUTHOARIZATION=None)
        response = self.client.get(urlStr)
        self.assertEqual(401, response.status_code,
                         "Unauthorised request succeeded  "+str(response.content))

        # Test that failed authorization returns 401
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid token')
        response = self.client.get(urlStr)
        self.assertEqual(401, response.status_code,
                         "Unauthorised request succeeded  "+str(response.content))


        # Test that correctly authenticated superuser request returns 200
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(urlStr)
        self.assertEqual(200, response.status_code, response.content)
        contentStr = response.content.decode('utf-8')
        # And that we return the correct user data
        results = json.loads(contentStr)['results']
        self.assertEqual(2,len(results),
                         "Expected to receive data for both users for superuser request")
        self.assertEqual(1,results[0]['user'])
        self.assertEqual(2,results[1]['user'])

        # And it works if we request our user data in the URL - but only get a single record, not an array
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url=urlStr+"1/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code, response.content)
        contentStr = response.content.decode('utf-8')
        # And that we return the correct user data
        results = json.loads(contentStr)
        self.assertEqual(1,results['user'])

        # And if we authenticate as user 2, we get user 2's data.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_2.key)
        url=urlStr+"2/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code, response.content)
        contentStr = response.content.decode('utf-8')
        print(contentStr)
        # And that we return the correct user data
        results = json.loads(contentStr)
        self.assertEqual(2,results['user'])

        # But user 2 can not see user1's data.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_2.key)
        url=urlStr+"1/"
        response = self.client.get(url)
        #FIXME - I think this should really return 403 rather than 404
        self.assertEqual(404, response.status_code, response.content)

        # and user 1 can  see user2's data because he is a superuser.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url=urlStr+"2/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code, response.content)
        contentStr = response.content.decode('utf-8')
        print(contentStr)
        # And that we return the correct user data
        results = json.loads(contentStr)
        self.assertEqual(2,results['user'])


