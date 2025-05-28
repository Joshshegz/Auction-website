from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import ListingForm
from .models import AuctionListing, Category
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
    return HttpResponseRedirect(reverse("auctions:index"))


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
            return redirect("auctions:home")
        else:
            print("Form errors:", form.errors)
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {'form': form})


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
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listings_view(request, category_name):
    try:
        category = Category.objects.get(category_name=category_name)
        listings = AuctionListing.objects.filter(category=category, is_active=True)
    except Category.DoesNotExist:
        listings = []

    return render(request, "auctions/category_listings.html", {
        "category": category_name,
        "listings": listings
    })


def home_page(request):
    # Get active auction items for display (limit to 6 for homepage)
    auction_items_qs = AuctionListing.objects.filter(is_active=True).order_by('-date_added')[:6]

    # Calculate time remaining for each item and store in a separate structure
    auction_items = []
    for item in auction_items_qs:
        item_data = {
            'item': item,
            'time_remaining': None
        }

        if hasattr(item, 'end_date') and item.end_date:
            if item.end_date > timezone.now():
                remaining = item.end_date - timezone.now()
                days = remaining.days
                hours = remaining.seconds // 3600
                item_data['time_remaining'] = f"{days}d {hours}h"
            else:
                item_data['time_remaining'] = "Expired"

        auction_items.append(item_data)

    # Sample testimonials data (you can create a model for this later)
    testimonials = [
        {
            'name': 'Sarah Johnson',
            'position': 'Art Collector',
            'text': 'Amazing platform for finding unique auction items! The bidding process is smooth and transparent.'
        },
        {
            'name': 'Mike Chen',
            'position': 'Antique Dealer',
            'text': 'I\'ve sold several valuable pieces here. Great community and excellent customer service.'
        },
        {
            'name': 'Emma Davis',
            'position': 'Jewelry Enthusiast',
            'text': 'Found some incredible vintage jewelry pieces. The authentication process gives me confidence.'
        },
        {
            'name': 'Robert Wilson',
            'position': 'Vintage Car Collector',
            'text': 'The best auction platform I\'ve used. Professional service and reliable transactions.'
        },
        {
            'name': 'Lisa Thompson',
            'position': 'Fine Arts Buyer',
            'text': 'Discovered amazing artworks at great prices. The platform is user-friendly and secure.'
        },
        {
            'name': 'David Martinez',
            'position': 'Collectibles Expert',
            'text': 'Excellent selection of rare collectibles. The auction process is fair and well-organized.'
        }
    ]

    # Sample upcoming auctions data
    upcoming_auctions = [
        {
            'title': 'Vintage Watch Collection',
            'price': '750.00',
            'timezone': 'EST',
            'days': '03',
            'hours': '12',
            'minutes': '45',
            'seconds': '30',
            'image': 'assets/images/upcoming1.jpg'  # Add this
        },
        {
            'title': 'Contemporary Art Pieces',
            'price': '1200.00',
            'timezone': 'PST',
            'days': '05',
            'hours': '08',
            'minutes': '20',
            'seconds': '15',
            'image': 'assets/images/upcoming2.jpg'  # Add this
        },
        {
            'title': 'Rare Book Collection',
            'price': '450.00',
            'timezone': 'EST',
            'days': '01',
            'hours': '18',
            'minutes': '35',
            'seconds': '50',
            'image': 'assets/images/upcoming3.jpg'  # Add this
        },

    ]

    # Sample sponsors data
    sponsors = [
        {'name': 'ArtWorld', 'image': 'assets/images/sponsors/sponsor1.png'},
        {'name': 'VintageHub', 'image': 'assets/images/sponsors/sponsor2.png'},
        {'name': 'CollectCorp', 'image': 'assets/images/sponsors/sponsor3.png'},
        {'name': 'AuctionPro', 'image': 'assets/images/sponsors/sponsor4.png'},
        {'name': 'BidMaster', 'image': 'assets/images/sponsors/sponsor5.png'},
        {'name': 'TradeLux', 'image': 'assets/images/sponsors/sponsor6.png'}
    ]

    context = {
        'auction_items': auction_items,
        'testimonials': testimonials,
        'upcoming_auctions': upcoming_auctions,
        'sponsors': sponsors
    }

    return render(request, "auctions/home.html", context)


@login_required
def account_view(request):
    context = {
        'pending_orders': 0,
        'processing_orders': 60,
        'delivered_orders': 40,
        'completed_orders': 70,
    }
    return render(request, 'auctions/dashboard.html', context)


@login_required
def closed_listings(request):
    closed_listing = AuctionListing.objects.filter(is_active=True).order_by('-date_added')
    return render(request, 'auctions/closed_listing.html', {'listing': closed_listing})