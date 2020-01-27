from django.db import models
from django.contrib.auth.models import User, Group


class Licence(models.Model):
    versionStr = models.CharField(max_length=10)
    summary = models.CharField(max_length=500)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Wearer(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField()
    ald = models.BooleanField(default=False)
    agreedToLicenceId = models.ForeignKey(Licence,
                                          on_delete=models.CASCADE,
                                          default=False)
    
    userId = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



