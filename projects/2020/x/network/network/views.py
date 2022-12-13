from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, UserFollowing
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):

    tweets = Post.objects.order_by('-updated')
    paginator = Paginator(tweets, 10)
    page = request.GET.get('page')
    paged_tweets = paginator.get_page(page)
    context = {
        "tweets": paged_tweets
    }
    return render(request, "network/index.html", context )


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, profile_id):
    user = User.objects.get(id=profile_id)
    tweets = Post.objects.order_by('-updated').filter(author = user)
    paginator = Paginator(tweets, 10)
    page = request.GET.get('page')
    paged_tweets = paginator.get_page(page)
    follow = UserFollowing.objects.filter(user_id= request.user.id, following_user_id=profile_id)
    followers = UserFollowing.objects.filter(following_user_id=profile_id).count()
    followees = UserFollowing.objects.filter(user_id=profile_id).count()
    follow_bool = False
    if follow:
        follow_bool = True
    context = {
        'user': user,
        'tweets': paged_tweets,
        'follow': follow_bool,
        'followers': followers,
        'followees': followees,
    }
    return render(request,'network/profile.html', context)


@login_required
def newPost(request):
    if request.method == "POST":
        user = request.user
        body = request.POST['post-content']
    
    post = Post(author=user, body=body)
    post.save()

    return redirect(reverse('index'))


@login_required
def follow(request, follower_id, followee_id):
    follower = User.objects.get(id=follower_id)
    followee = User.objects.get(id=followee_id)
    new_follow = UserFollowing(user_id=follower, following_user_id=followee)
    new_follow.save()
    return redirect('profile', profile_id=followee_id)

@login_required
def unfollow(request, follower_id, followee_id):
    follower = User.objects.get(id=follower_id)
    followee = User.objects.get(id=followee_id)
    UserFollowing.objects.filter(user_id= follower, following_user_id=followee).delete()
    return redirect('profile', profile_id=followee_id)

@csrf_exempt
@login_required
def like_unlike_post(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get("post_id")
        user = request.user
    
        post = Post.objects.get(id=post_id)

        if user in post.likes.all():
            post.likes.remove(user)
            icon_value = 'bi-heart'
        else:
            post.likes.add(user)
            icon_value = 'bi-heart-fill'
        
        data = {
            'icon_value': icon_value,
            'likes_count': post.number_of_likes(),
        }
        return JsonResponse(data)
        
@csrf_exempt
@login_required
def update(request):
    
    if request.method == "POST":
        data = json.loads(request.body)
        tweet = Post.objects.get(id=data['post_id'])
        body = data['post_content']
    
    tweet.body = body
    tweet.save()

    return HttpResponse(status=204)
    #return redirect(reverse('index'))

@login_required
def following(request):
    follows = UserFollowing.objects.filter(user_id = request.user)
    follows_id = follows.values_list('following_user_id', flat=True)
    tweets = Post.objects.all().filter(author__in=follows_id).order_by('-updated')
    paginator = Paginator(tweets, 10)
    page = request.GET.get('page')
    paged_tweets = paginator.get_page(page)
    context = {
        "tweets": paged_tweets
    }
    return render(request, "network/following.html", context )

