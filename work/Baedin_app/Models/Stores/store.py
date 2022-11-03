from django.db import models

from Baedin_app.Models.Categories.categories import Categories
from ..Users.users import User
from django.utils import timezone
class Store(models.Model):
    Id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.TextField(default="",null=True,blank=True)
    store_logo = models.TextField(default="",null=True,blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(default=timezone.now)
    isDeleted = models.BooleanField(default=False)