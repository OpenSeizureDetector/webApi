from rest_framework import serializers
from .models import Datapoint


class DatapointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datapoint
        fields = "__all__"


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
