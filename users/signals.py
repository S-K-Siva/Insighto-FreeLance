from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import User, Profile



def createProfile(sender,instance,created,**kwargs):
    profile = None
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
        )

post_save.connect(createProfile,sender=User)