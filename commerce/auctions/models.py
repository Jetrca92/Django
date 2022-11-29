from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=64)
    imgurl = models.CharField(max_length=128, default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/2048px-No_image_available.svg.png")
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.name}({self.category}), {self.description}, {self.price}$ "

class Bids(models.Model):
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Starting bid: {Bids.starting_bid}"


class Comments(models.Model):
    comment = models.CharField(max_length=128)
