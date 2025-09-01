# cycles/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Ensure a UserProfile exists for each User; use get_or_create to be idempotent.

    The previous unconditional create could raise IntegrityError when another
    part of the code (or tests) already created a profile for the user. Using
    get_or_create prevents UNIQUE constraint failures.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
