from rest_framework import serializers
from .models import Datapoint


class DatapointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datapoint
        fields = "__all__"
