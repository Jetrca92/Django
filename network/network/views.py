from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Profile


def index(request):
    
    # Get all posts, sort them by date (newest first)
    posts = Post.objects.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            "content": post.content,
            "author": post.author,
            "date": post.date,
            "likes": post.likes
        })
    sorted_posts_data = sorted(posts_data, key=lambda x: x["date"], reverse=True)

    # If form sent, save new post
    if request.method == "POST":
        content = request.POST["new_post"]
        author = request.user
        post = Post(author=author, content=content)
        post.save()
        posts = Post.objects.all()
        posts_data = []
        for post in posts:
            posts_data.append({
                "content": post.content,
                "author": post.author,
                "date": post.date,
                "likes": post.likes
            })
        sorted_posts_data = sorted(posts_data, key=lambda x: x["date"], reverse=True)
        return render(request, "network/index.html", {
            "posts": sorted_posts_data
        })
    else:
        return render(request, "network/index.html", {
            "posts": sorted_posts_data
        })


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

        # Create Profile model for new user
        profile = Profile(owner = user)
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile_page(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(owner=user)

    # Filter posts and sort them by date
    posts = Post.objects.filter(author=user)
    posts_data = []
    for post in posts:
        posts_data.append({
            "content": post.content,
            "author": post.author,
            "date": post.date,
            "likes": post.likes
        })
    sorted_posts_data = sorted(posts_data, key=lambda x: x["date"], reverse=True)

    # Count followers and following
    f = profile.followers.count()
    fw = profile.following.count()
    
    is_following = request.user in profile.followers.all()
    return render(request, "network/profile_page.html", {
        "user": user,
        "profile": profile,
        "f": f,
        "fw": fw,
        "posts": sorted_posts_data,
        "is_following": is_following
    })

def unfollow(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(owner=user)
    profile.followers.remove(request.user)
    return HttpResponseRedirect(reverse("profile_page", args=(username, )))

def follow(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(owner=user)
    profile.followers.add(request.user)
    return HttpResponseRedirect(reverse("profile_page", args=(username, )))
