# from datetime import datetime
# from email.policy import default
#
# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class User(AbstractUser):
#
#
#     def __str__(self):
#         return self.username
# #
# # class Categorry(models.Model ):
# #     category_list = models.ManyToManyField('AuctionListing', blank=True,)
#
# class Category(models.Model):
#     category_name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.category_name
#
# class AuctionListing(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
#     current_price = models.DecimalField(max_digits=10, decimal_places=2)
#     imageurl = models.URLField(blank=True, null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     date_added = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
#     is_active = models.BooleanField(default=True)
#     winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')
#
#     def __str__(self):
#         return f"{self.title} (${self.current_price})"
#
#
# class UserComments(models.Model):
#     commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#     comment = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)
#     listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,
#                                 related_name='comments')
#
#     def __str__(self):
#         return f"Comment by {self.commenter} on {self.listing}"
#
#
# class Bid(models.Model):
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
#     listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"${self.amount} bid on {self.listing} by {self.bidder}"
#
#     class Meta:
#         ordering = ['-amount']



from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    def __str__(self):
        return self.username

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    imageurl = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)  # Added this field
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')

    def save(self, *args, **kwargs):
        # Set default end_date if not provided (7 days from creation)
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def time_remaining(self):
        """Calculate and return time remaining for the auction"""
        if self.end_date and self.end_date > timezone.now():
            remaining = self.end_date - timezone.now()
            days = remaining.days
            hours = remaining.seconds // 3600
            return f"{days}d {hours}h"
        return "Expired"

    @property
    def is_expired(self):
        """Check if auction has expired"""
        if self.end_date:
            return self.end_date <= timezone.now()
        return False

    def __str__(self):
        return f"{self.title} (${self.current_price})"

    class Meta:
        ordering = ['-date_added']

class UserComments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.commenter} on {self.listing}"

    class Meta:
        ordering = ['-date_added']

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update the listing's current_price when a new bid is placed
        if self.amount > self.listing.current_price:
            self.listing.current_price = self.amount
            self.listing.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"${self.amount} bid on {self.listing} by {self.bidder}"

    class Meta:
        ordering = ['-amount']

# Optional: Models for testimonials and sponsors if you want to make them dynamic
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    text = models.TextField()
    image = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField()
    website_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


