from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"

class Listing(models.Model):
    listing_name = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    photo_url = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="createdby")
    created_on = models.DateTimeField()
    is_active = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="categories")

    def __str__(self):
        return f"{self.listing_name} : {self.description}"

class Comment(models.Model):
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="commented")
    created_on = models.DateTimeField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingcomment")

    def __str__(self):
        return f"{self.id} : {self.created_by} : {self.comment}"

class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=10)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidlisting")

    def __str__(self):
        return f"{self.id} : {self.bid_by} : {self.listing} : {self.bid_by}"

class WatchList(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")
    watched_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")

    def __str__(self):
        return f"{self.id} : {self.listing} : {self.watched_by}"