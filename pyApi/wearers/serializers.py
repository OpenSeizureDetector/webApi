from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from wearers.models import Wearer, Licence
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    #wearers = serializers.PrimaryKeyRelatedField(
    #    many=True,
    #    queryset=Wearer.objects.all())

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class WearerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wearer
        fields = '__all__'

    def create(self, validated_data):
        print("wearerSerializer.create()")
        message = "testing"
        send_mail(
            'Testing',
            message,
            'donotreply@openseizuredetector.org.uk',
            ['grahamjones139@gmail.com']
        )
        return None
        
class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = '__all__'
