from django.db import models
from django.contrib.auth.models import User, Group



class Event(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.IntegerField()
    dataTime = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)

    eventTypes = [
        "Unvalidated Alarm",
        "Unvalidated Warning",
        "False Alarm",
        "False Warning",
        "Tonic-Clonic Seizure",
        "Other Seizure",
        "Other Medical Issue",
        ]
