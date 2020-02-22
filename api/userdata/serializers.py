from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Profile, Licence, RoleAllocations, roles

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        #fields = "__all__"
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
                  'is_superuser', 'is_staff', 'profile')

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Profile
        depth = 1
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'dob', 'licenceAccepted', 'medicalConditions', 'user',
                  )


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = "__all__"


class RoleAllocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAllocations
        fields = "__all__"


    def isAdmin(userId):
        queryset=RoleAllocations.objects.filter(userId=userId).values('roleId')
        print(queryset)
        # If there is no entry in RoleAllocations for this user
        # it must be a normal user.
        if len(queryset)==0:
            return false
        # If it is an admin, return true
        if queryset[0]==2:
            return true
        else:
            return false
        
        
        
