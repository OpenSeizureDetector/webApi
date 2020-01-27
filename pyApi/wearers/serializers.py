from django.contrib.auth.models import User, Group
from wearers.models import Wearer, Licence
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class WearerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wearer
        fields = '__all__'

class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = '__all__'
