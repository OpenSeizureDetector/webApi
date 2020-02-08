from rest_framework import viewsets
from rest_framework import permissions
from userdata.models import Profile, Licence
from userdata.serializers import ProfileSerializer, LicenceSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("ProfileViewSet.perform_create()")
        serializer.save(userId=self.request.user)

class LicenceViewSet(viewsets.ModelViewSet):
    queryset = Licence.objects.all()
    serializer_class = LicenceSerializer
    #permission_classes = [permissions.IsAuthenticated]
