from django.db import models
from django.contrib.auth.models import User, Group

class Wearer(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField()
    ald = models.BooleanField(default=False)
    
    userId = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
