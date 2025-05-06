from django.db import models

# Create your models here.

from django.db import models
from auctions.models import AuctionListing
from django.contrib.auth import get_user_model

User = get_user_model()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='watchlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')  # Prevent duplicates
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user}'s watchlist item: {self.listing.title}"