from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    imgurl = models.CharField(max_length=512)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")

    def __str__(self):
        return self.name


