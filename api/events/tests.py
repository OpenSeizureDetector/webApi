from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Event

class EventTests(APITestCase):
    def test_getEventUnauth(self):
        """
        Ensure that an unauthenticated request does not return any data.
        """
        url = reverse('events-list')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 0)
        #self.assertEqual(Account.objects.get().name, 'DabApps')
