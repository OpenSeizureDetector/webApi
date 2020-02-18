from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

from django.contrib.auth.models import User

from rawdata.models import Datapoint
from rawdata.serializers import DatapointSerializer


class DatapointList(generics.ListCreateAPIView):
    queryset = Datapoint.objects.all()
    serializer_class = DatapointSerializer
    permission_classes = [
        #permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAuthenticated,
        #IsOwnerOrFail,
        ]


class DatapointDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Datapoint.objects.all()
    serializer_class = DatapointSerializer
    permission_classes = (
        #permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAuthenticated,
        #IsOwnerOrReadOnly
        #IsOwnerOrFail,
    )


