from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ListingForm
from .models import AuctionListing
from watchlist.models import Watchlist
from .models import UserComments

def index(request):
    active_listings = AuctionListing.objects.filter(is_active=True).order_by('-date_added')
    return render(request, "auctions/index.html", {
        "listings": active_listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.current_price = listing.starting_bid
            listing.is_active = True
            listing.save()
            messages.success(request, "Listing created successfully!")
            return redirect("auctions:index")  # Changed to include namespace
        else:
            print("Form errors:", form.errors)
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {'form': form})


# In auctions/views.py listing_detail view:
def listing_detail(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    comments = UserComments.objects.filter(listing=listing).order_by('-date_added')
    user_watchlist_ids = []
    if request.user.is_authenticated:
        user_watchlist_ids = request.user.user_watchlist.values_list('listing_id', flat=True)

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "user_watchlist_ids": user_watchlist_ids,
        "comments": comments
    })


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            UserComments.objects.create(
                commenter=request.user,
                listing=listing,
                comment=comment_text
            )
            messages.success(request, "Comment added successfully!")

    return redirect('auctions:listing_detail', listing_id=listing.id)

def categories_view(request):
    categories = AuctionListing.objects.values_list("category", flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listings_view(request, category_name):
    listings = AuctionListing.objects.filter(category=category_name, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category_name,
        "listings": listings
    })
