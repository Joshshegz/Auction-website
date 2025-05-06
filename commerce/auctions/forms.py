from django import forms
from .models import AuctionListing

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ['current_price', 'author']
