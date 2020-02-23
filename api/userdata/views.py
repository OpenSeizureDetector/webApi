from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from userdata.models import Profile, Licence
from userdata.serializers import UserSerializer, ProfileSerializer, LicenceSerializer
import common.queryUtils
from common.permissions import IsOwnerOrAdmin
import json

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get_queryset(self):
        queryset = User.objects.all().order_by('id')
        user = self.request.query_params.get('user', None)
        authUser = self.request.user.id
        print("UserViewSet.get_queryset - user=%s, authUser=%s" %
              (user, authUser))
        queryset = queryset.filter(id=authUser)
        return queryset


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrAdmin]
    def get_queryset(self):
        queryset = Profile.objects.all().order_by('id')
        user = self.request.query_params.get('user', None)
        authUser = self.request.user.id
        print("ProfileViewSet.get_queryset - user=%s, authUser=%s" %
              (user, authUser))
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=authUser)
        return queryset


    def perform_create(self, serializer):
        print("ProfileViewSet.perform_create()")
        serializer.save(user=self.request.user)

class LicenceViewSet(viewsets.ModelViewSet):
    queryset = Licence.objects.all()
    serializer_class = LicenceSerializer
    #permission_classes = [permissions.IsAuthenticated]
