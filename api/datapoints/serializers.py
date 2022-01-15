from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Datapoint


class DatapointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datapoint
        fields = "__all__"
        #validators = [
        #    UniqueTogetherValidator(
        #        queryset=Datapoint.objects.all(),
        #        fields=['dataTime', 'userId'],
        #        message='Skipping Duplicate datapoint'
        #    )
        #]
        read_only_fields = (
            'userId',
        ) 

class DatapointSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Datapoint
        fields = [
            "dataTime",
            "userId",
            "statusStr",
            "accMean",
            "accSd",
            "hr"
        ]
        read_only_fields = (
            'userId',
        ) 
