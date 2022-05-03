from django.db import models
from django.contrib.auth.models import User, Group



class Event(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    osdAlarmState = models.IntegerField(blank=True, null=True)
    dataTime = models.DateTimeField()
    type = models.TextField(blank=True, null=True)
    subType = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    dataJSON = models.TextField(blank=True, null=True)

    UNVALIDATED_ALARM_TYPE = 0
    UNVALIDATED_WARNING_TYPE = 1
    UNVALIDATED_FALL_TYPE = 2
    UNVALIDATED_MANUAL_ALARM_TYPE = 3
    FALSE_ALARM_TYPE = 4
    FALSE_WARNING_TYPE = 5
    FALSE_FALL_TYPE = 6
    TC_SEIZURE_TYPE = 7
    OTHER_SEIZURE_TYPE = 8
    FALL_TYPE = 9
    OTHER_MEDICAL_TYPE = 10
    
    eventTypes = [
        "Unvalidated Alarm",
        "Unvalidated Warning",
        "Unvalidated Fall",
        "Unvalidated Manual Alarm",
        "False Alarm",
        "False Warning",
        "False Fall",
        "Tonic-Clonic Seizure",
        "Other Seizure",
        "Fall",
        "Other Medical Issue",
        ]
