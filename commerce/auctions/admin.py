from .models import UserComments, AuctionListing, Category
from .models import Bid, User
from django.contrib import admin

# Register your models here.
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(UserComments)
admin.site.register(AuctionListing)
admin.site.register(Category)