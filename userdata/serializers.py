from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Profile, Licence, RoleAllocations, roles


class ProfileSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(
        #read_only=True,
    #    default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile
        fields = "__all__"
        #read_only_fields = (
        #    'userId',
        #) 

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
        
        
        
