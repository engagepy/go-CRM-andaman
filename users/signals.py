from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User
from django.contrib.auth.models import Group
from . import admin

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        # Add user to intern group
        instance.groups.add(Group.objects.get(name='Intern'))
        
    # Existing users: just save the profile
    instance.userprofile.save()


