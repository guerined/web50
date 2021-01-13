from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .models import User, Listing, Category, WatchList, Bid, Comment
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['listing_name','description','starting_bid','photo_url','is_active','category']

class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category_listing(request, category_id):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category_id, is_active=True)
    })
    
@login_required
def category_new(request):
    if request.method == "POST":
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("categories"))
    else:
        form = NewCategoryForm()
        context = {
            'form':form
        }
        return render(request,"auctions/newcategory.html", context)

@login_required
def new_listing(request):
    if request.method == "POST":
        user = request.user
        form = NewListingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = user
            data.created_on = datetime.now()
            data.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = NewListingForm()
        context = {
            'form':form
        }
        return render(request,"auctions/newlisting.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    status_message = ""
    bid = Bid()

    if Bid.objects.filter(listing=listing).exists():
        bid = listing.bidlisting.last()
    else:
        bid.bid = listing.starting_bid

    bid2 = listing.bidlisting.last()

    comments = listing.listingcomment.all()
    formbid = NewBidForm()
    error_message=""
    if WatchList.objects.filter(watched_by=request.user, listing = listing).exists():
        watched = True
    else:
        watched = False
    

    if not(listing.is_active):
        if not(Bid.objects.filter(listing=listing).exists()):
            status_message = '<div class="alert alert-danger" role="alert"> Auction is closed! Nobody has won the auction </div>'
        else:
            bid3 = listing.bidlisting.last()
            if request.user == bid3.bid_by:
                status_message = '<div class="alert alert-success" role="alert"> Auction closed and you won the auction </div>'
            else:
                status_message = '<div class="alert alert-warning" role="alert"> Auction closed and won by ' + bid3.bid_by.username + '</div>'

    if request.method == "POST":
        bid_try = request.POST.get("bid","")
        bid_try_d = float(bid_try)
        if (bid_try_d > bid.bid and Bid.objects.filter(listing=listing).exists()) or (not(Bid.objects.filter(listing=listing).exists()) and bid_try_d >= bid.bid):
            user = request.user
            form = NewBidForm(request.POST)
            data = form.save(commit=False)
            data.bid_by = user
            data.listing = listing
            data.save()
            error_message= '<div class="alert alert-success" role="alert">Bid accepted</div>'
            bid = listing.bidlisting.last()
            return render(request, "auctions/listing.html", {
                "listing": listing, "bid": bid, "comments":comments, "formbid":formbid, "error_message":error_message, "watched":watched, "status_message":status_message
            })
        else:
            error_message = '<div class="alert alert-danger" role="alert"> Your bid must be higher than the lastest bid </div>'
            bid = listing.bidlisting.last()
            return render(request, "auctions/listing.html", {
                "listing": listing, "bid": bid2, "comments":comments, "formbid":formbid, "error_message":error_message, "watched":watched, "status_message":status_message
            })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing, "bid": bid2, "comments":comments, "formbid":formbid, "error_message":error_message, "watched":watched, "status_message":status_message
        })

@login_required
def watchlist(request):
    user = request.user
    watch = user.watcher.all()

    return render(request, "auctions/watchlist.html", {
        "watch": watch
    } )

@login_required
def new_comment(request, listing_id):
    form = NewCommentForm()
    listing = Listing.objects.get(id=listing_id)

    if request.method == "POST":
        user = request.user
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = user
            data.created_on = datetime.now()
            data.listing = listing
            data.save()
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        
    else:
        return render(request, "auctions/new_comment.html", {
            "form":form, "listing":listing
        })

@login_required
def watchlist_add(request, listing_id):
    watch = WatchList()
    listing = Listing.objects.get(id=listing_id)

    watch.watched_by = request.user
    watch.listing = listing
    watch.save()
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))

@login_required
def auction_close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))