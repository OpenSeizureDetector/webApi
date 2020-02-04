from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    #userId = serializers.PrimaryKeyRelatedField(
    #    read_only=True,
    #    default=serializers.CurrentUserDefault())
    class Meta:
        model = Event
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
