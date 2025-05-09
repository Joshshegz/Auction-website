from django.urls import path
from . import views
from watchlist.views import watchlist_view

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('watchlist/', watchlist_view, name='watchlist'),
    path("categories/", views.categories_view, name="categories"),
    path("categories/<str:category_name>/", views.category_listings_view, name="category_listings"),
    path('listing/<int:listing_id>/comment/', views.add_comment, name='add_comment'),
]