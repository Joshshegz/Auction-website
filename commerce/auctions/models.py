from datetime import datetime
from email.policy import default

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):


    def __str__(self):
        return self.username
#
# class Categorry(models.Model ):
#     category_list = models.ManyToManyField('AuctionListing', blank=True,)

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    imageurl = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')

    def __str__(self):
        return f"{self.title} (${self.current_price})"


class UserComments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,
                                related_name='comments')

    def __str__(self):
        return f"Comment by {self.commenter} on {self.listing}"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} bid on {self.listing} by {self.bidder}"

    class Meta:
        ordering = ['-amount']