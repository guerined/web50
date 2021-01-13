from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/new", views.new_listing, name="newListing"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_listing, name="category_listing"),
    path("categories/new", views.category_new, name="new_category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("new_comment/<int:listing_id>", views.new_comment, name="new_comment"),
    path("watchlist_add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("auction_close/<int:listing_id>", views.auction_close, name="auction_close")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

