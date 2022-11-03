from django.db import models
from ..Users.users import User
from django.utils import timezone
class Wallet(models.Model):
    Id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.TextField(default="",null=True,blank=True)
    creation_time = models.DateTimeField(default=timezone.now)
    isDeleted = models.BooleanField(default=False)