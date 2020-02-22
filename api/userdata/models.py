from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Licence(models.Model):
    version = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    licenceText = models.TextField(blank=True)

    def __unicode__(self):
        return '{0}: {1}'.format(self.title, self.licenceText)


roles = {
    0: "User",
    1: "Analyst",
    2: "Admin"
    }
    
class RoleAllocations(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    roleId = models.IntegerField()

    
class Profile(models.Model):
    """ User profile - details of user's medical condition
    and agreement to licence to use data.
    """
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    medicalConditions = models.TextField(blank=True, default='none specified')
    licenceAccepted = models.OneToOneField(Licence,on_delete=models.CASCADE,
                                           blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        print("userdata.models.create_user_profile")
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        print("userdata.models.save_user_profile")
        instance.profile.save()


        

