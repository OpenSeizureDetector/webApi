from django.db import models
from django.contrib.auth.models import User, Group

class Datapoint(models.Model):
    dataTime = models.DateTimeField()
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    accMean = models.FloatField()
    accSd = models.FloatField()
    hr = models.FloatField()
    categoryId = models.IntegerField()
    eventId = models.IntegerField()
    dataJSON = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
