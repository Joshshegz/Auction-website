from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auctions.models import AuctionListing
from .models import Watchlist
from django.shortcuts import render


@login_required
def watchlist_view(request):
    # Get all watchlist items for current user with related listings
    watchlist_items = request.user.user_watchlist.select_related('listing').all()
    return render(request, 'watchlist/watchlist.html', {
        'watchlist_items': watchlist_items
    })


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Check if item already exists in watchlist
    if Watchlist.objects.filter(user=request.user, listing=listing).exists():
        Watchlist.objects.filter(user=request.user, listing=listing).delete()
        messages.success(request, "Removed from watchlist")
    else:
        Watchlist.objects.create(user=request.user, listing=listing)
        messages.success(request, "Added to watchlist")

    # Redirect back to previous page
    return redirect(request.META.get('HTTP_REFERER', 'auctions:index'))