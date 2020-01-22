
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.db.models.query import QuerySet
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from wearers.views import WearerViewSet
from wearers.models import Wearer

class WearerTestCase(TestCase):
    def setUp(self):
        # Create a test instance
        self.wearerObj = Wearer.objects.create({ 'name': 'testWearer',
                                                 'dob': '1969/05/12',
                                                 'userId': 1,
        })

        # Create auth user for views using api request factory
        self.username = 'tester_uname'
        self.password = 'tester_pw'
        self.user = User.objects.create_superuser(self.username, 'test@example.com', self.password)

    def tearDown(self):
        pass

    @classmethod
    def setup_class(cls):
        """setup_class() before any methods in this class"""
        pass

    @classmethod
    def teardown_class(cls):
        """teardown_class() after any methods in this class"""
        pass

    def shortDescription(self):
        return None


    def testViewNoAuth(self):
        """
        No auth example
        """
        api_request = APIRequestFactory().get("")
        detail_view = WearerViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request)
        self.assertEqual(response.status_code, 401)

    def testViewAuth(self):
        """
        Auth using force_authenticate
        """
        factory = APIRequestFactory()
        user = User.objects.get(username=self.username)
        detail_view = WearerViewSet.as_view({'get': 'retrieve'})

        # Make an authenticated request to the view...
        api_request = factory.get('')
        force_authenticate(api_request, user=user)
        response = detail_view(api_request)
        self.assertEqual(response.status_code, 200)       
