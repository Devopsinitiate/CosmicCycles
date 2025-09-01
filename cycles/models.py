from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    business_start_date = models.DateField(null=True, blank=True)
    other_dates = models.JSONField(default=dict, blank=True)  # For custom cycles/events
    timezone = models.CharField(max_length=50, default='UTC')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Ensure a UserProfile exists for every user; use get_or_create to be idempotent.
    UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the related profile if present; guard against missing related object.
    try:
        profile = getattr(instance, 'userprofile', None)
        if profile:
            profile.save()
    except Exception:
        # Avoid raising during user save; profile will be created by get_or_create above if missing.
        pass

class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    establishment_date = models.DateField()

    def __str__(self):
        return self.name

# Static cycle/period data from book
class CycleTemplate(models.Model):
    CYCLE_TYPES = [
        ('human', 'Human Life'),
        ('yearly', 'Yearly'),
        ('business', 'Business'),
        ('health', 'Health'),
        ('daily', 'Daily'),
        ('soul', 'Soul'),
        ('reincarnation', 'Reincarnation'),
    ]
    cycle_type = models.CharField(max_length=20, choices=CYCLE_TYPES)
    period_number = models.IntegerField()
    description = models.TextField()
    effects = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.get_cycle_type_display()} Period {self.period_number}"

# Computed cycles for each user
class UserCycle(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cycle_type = models.CharField(max_length=20)
    start_date = models.DateField()
    current_period = models.IntegerField()
    report_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.cycle_type} cycle"
