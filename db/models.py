from django.contrib.auth.models import User
from django.db import models


class Investor(models.Model):
    user = models.OneToOneField(User, related_name='investor', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone = models.CharField(max_length=30, null=False, blank=False)
    is_deleted = models.BooleanField(default=False)


class Wallet(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    investor = models.ForeignKey(Investor, on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)


class Assets(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    symbol = models.CharField(max_length=8)
    is_deleted = models.BooleanField(default=False)
