from django.urls import path
from . import views

app_name = 'watchlist'

urlpatterns = [
    path('', views.watchlist_view, name='watchlist'),
    path('toggle/<int:listing_id>/', views.toggle_watchlist, name='toggle_watchlist'),
]