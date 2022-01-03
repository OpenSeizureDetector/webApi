from django.db import models
from django.contrib.auth.models import User, Group



class Event(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.IntegerField()
    dataTime = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)

    UNVALIDATED_ALARM_TYPE = 0
    UNVALIDATED_WARNING_TYPE = 1
    UNVALIDATED_FALL_TYPE = 2
    FALSE_ALARM_TYPE = 3
    FALSE_WARNING_TYPE = 4
    FALSE_FALL_TYPE = 5
    TC_SEIZURE_TYPE = 6
    OTHER_SEIZURE_TYPE = 7
    FALL_TYPE = 8
    OTHER_MEDICAL_TYPE = 9
    
    eventTypes = [
        "Unvalidated Alarm",
        "Unvalidated Warning",
        "Unvalidated Fall",
        "False Alarm",
        "False Warning",
        "False Fall",
        "Tonic-Clonic Seizure",
        "Other Seizure",
        "Fall",
        "Other Medical Issue",
        ]
