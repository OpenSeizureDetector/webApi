from django.db import models
from django.contrib.auth.models import User, Group

class Datapoint(models.Model):
    dataTime = models.DateTimeField()
    userId = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    statusStr = models.CharField(blank=True, null=True, max_length=30)
    accMean = models.FloatField(blank=True, null=True)
    accSd = models.FloatField(blank=True, null=True)
    hr = models.FloatField(blank=True, null=True)
    categoryId = models.IntegerField(blank=True, null=True)
    eventId = models.IntegerField(blank=True, null=True)
    dataJSON = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
