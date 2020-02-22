from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Profile, Licence, RoleAllocations, roles

from django.contrib.auth.models import User
import json


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
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    #userId = serializers.CharField(source='user.id')
    class Meta:
        model = Profile
        depth = 1
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'dob', 'licenceAccepted', 'medicalConditions',
                  'is_superuser', 'is_staff',
                  'user',
                  #'userId'
                  )

    def update(self, instance, validated_data):
        # NOTE:  instance is an object of type Profile
        #print("ProfileSerializer.update - validated_data="+json.dumps(validated_data))
        user_data = validated_data.pop('user')
        #print("ProfileSerializer.update - user_data="+repr(user_data))
        #print("ProfileSerializer.update - validated_data="+json.dumps(validated_data))

        # First we save the data in the profile object
        instance.dob = validated_data.get('dob', instance.dob)
        instance.medicalConditions = validated_data.get('medicalConditions',
                                                        instance.medicalConditions)
        instance.licenceAccepted = validated_data.get('licenceAccepted', instance.licenceAccepted)
        instance.save()

        # Then we save the data that is stored in the user model
        userModel = User.objects.get(id=instance.user.id)
        userModel.username = user_data.get('username', userModel.username)
        userModel.first_name = user_data.get('first_name', userModel.first_name)
        userModel.last_name = user_data.get('last_name', userModel.last_name)
        userModel.save()

        # And we return the profile instance.
        return instance

        
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
        
        
        
