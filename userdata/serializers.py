from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Profile, Licence


class ProfileSerializer(serializers.ModelSerializer):
    #userId = serializers.PrimaryKeyRelatedField(
    #    read_only=True,
    #    default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile
        fields = "__all__"
    #    validators = [
    #        UniqueTogetherValidator(
    #            queryset=Event.objects.all(),
    #            fields=['dataTime', 'userId'],
    #            message='Skipping Duplicate event'
    #        )
    #    ]
    #    read_only_fields = (
    #        'userId',
    #    ) 

class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = "__all__"

