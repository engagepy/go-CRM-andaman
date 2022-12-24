from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Trip


@receiver(pre_save, sender=Trip)
def trip_final_cal(sender, **kwargs):
    pass

@receiver(post_save, sender=Trip)
def trip_post_cal(sender, **kwargs):
    pass