from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Farmer, CustomUser, Client

@receiver(post_delete, sender=Farmer)
def delete_related_user(sender, instance, **kwargs):
    """
    Signal handler to delete the associated CustomUser when a Farmer is deleted.
    """
    if instance.user_id:
        CustomUser.objects.filter(pk=instance.user_id).delete()

@receiver(post_delete, sender=Client)
def delete_associated_user(sender, instance, **kwargs):
    if instance.user_id:
        CustomUser.objects.filter(pk=instance.user_id).delete()