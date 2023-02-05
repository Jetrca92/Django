from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="author")
    content = models.CharField(max_length=280)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.content} ({self.author})"

class Profile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="owner")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")

    def __str__(self):
        return self.owner.username