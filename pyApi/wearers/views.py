from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from wearers.serializers import UserSerializer, GroupSerializer, WearerSerializer, LicenceSerializer
from wearers.models import Wearer
from wearers.models import Licence


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class WearerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wearer.objects.all()
    serializer_class = WearerSerializer

    
class LicenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Licence.objects.all()
    serializer_class = LicenceSerializer
