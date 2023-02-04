from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="author")
    content = models.CharField(max_length=280)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
