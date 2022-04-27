from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.

class Wallet(models.Model):
    owned_by = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    status = models.CharField(default="disabled", max_length = 8)
    disabled_at = models.DateTimeField(auto_now = False, blank = True, null = True)
    enabled_at = models.DateTimeField(auto_now = False, blank = True, null = True)
    balance = models.IntegerField(default=0)

class Deposit(models.Model):
    deposited_by = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    status = models.CharField(max_length = 8, null = True)
    deposited_at = models.DateTimeField(auto_now = True, blank = True)
    amount = models.IntegerField(null = False, blank = False)
    reference_id = models.CharField(max_length = 180, unique=True)
    wallet_id = models.ForeignKey(Wallet, on_delete = models.CASCADE)

class Withdraw(models.Model):
    withdrawn_by = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    status = models.CharField(max_length = 8, null = True)
    withdrawn_at = models.DateTimeField(auto_now = True, blank = True)
    amount = models.IntegerField(null = False, blank = False)
    reference_id = models.CharField(max_length = 180, unique=True)
    wallet_id = models.ForeignKey(Wallet, on_delete = models.CASCADE)