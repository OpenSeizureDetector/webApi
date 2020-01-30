from django.test import TestCase

from rest_framework.test import APIRequestFactory
from django.db.models.query import QuerySet
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

import rawdata.views
from rawdata.models import Datapoint




from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .rawdata import Datapoint
from .serializers import DatapointSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_datapoint(title="", artist=""):
        if title != "" and artist != "":
            Datapoint.objects.create(title=title, artist=artist)

    def setUp(self):
        # add test data
        self.create_datapoint("like glue", "sean paul")
        self.create_datapoint("simple song", "konshens")
        self.create_datapoint("love is wicked", "brick and lace")
        self.create_datapoint("jam rock", "damien marley")


class GetAllDatapointsTest(BaseViewTest):

    def test_get_all_datapoints(self):
        # hit the API endpoint
        response = self.client.get(
            reverse("rawdata", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Datapoint.objects.all()
        serialized = DatapointSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)














class DatapointTestCase(TestCase):
    def setUp(self):
        # Create a test instance
        datapointObj = Datapoint.objects.create(
        )

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
        response = detail_view(api_request, pk=1)
        self.assertEqual(response.status_code, 401,msg="Unauthorised view succeeded")

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
        response = detail_view(api_request, pk=1)
        self.assertEqual(response.status_code, 200, msg="Authorised view failed")       

