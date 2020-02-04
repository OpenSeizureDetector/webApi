from django.db import models
from django.contrib.auth.models import User, Group



class Event(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.IntegerField()
    dataTime = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)

    UNVALIDATED_ALARM_TYPE = 0
    UNVALIDATED_WARNING_TYPE = 1
    FALSE_ALARM_TYPE = 2
    FALSE_WARNING_TYPE = 3
    TC_SEIZURE_TYPE = 4
    OTHER_SEIZURE_TYPE = 5
    OTHER_MEDICAL_TYPE = 6
    
    eventTypes = [
        "Unvalidated Alarm",
        "Unvalidated Warning",
        "False Alarm",
        "False Warning",
        "Tonic-Clonic Seizure",
        "Other Seizure",
        "Other Medical Issue",
        ]
