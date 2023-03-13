from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, Post, Profile
from django.core.paginator import Paginator


def index(request):
    
    # Get all posts, sort them by date (newest first), divide in pages
    posts = Post.objects.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            "content": post.content,
            "author": post.author,
            "date": post.date,
            "likes": post.likes,
            "id": post.id
        })
    sorted_posts_data = sorted(posts_data, key=lambda x: x["date"], reverse=True)
    paginator = Paginator(sorted_posts_data, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

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
                "likes": post.likes,
                "id": post.id
            })
        sorted_posts_data = sorted(posts_data, key=lambda x: x["date"], reverse=True)
        paginator = Paginator(sorted_posts_data, 10)
        page_number = request.GET.get('page')
        posts_page = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": posts_page,
            "page_number": page_number
        })
    else:
        return render(request, "network/index.html", {
            "posts": posts_page,
            "page_number": page_number
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
    user_profile = User.objects.get(username=username)
    profile = Profile.objects.get(owner=user_profile)

    # Filter posts and sort them by date
    posts = Post.objects.filter(author=user_profile)
    posts_data = []
    for post in posts:
        posts_data.append({
            "content": post.content,
            "author": post.author,
            "date": post.date,
            "likes": post.likes,
            "id": post.id
        })
    sorted_posts_data = sorted(posts_data, key=lambda x: x["date"], reverse=True)

    # Count followers and following
    f = profile.followers.count()
    fw = profile.following.count()
    
    is_following = request.user in profile.followers.all()
    return render(request, "network/profile_page.html", {
        "user_profile": user_profile,
        "profile": profile,
        "f": f,
        "fw": fw,
        "posts": sorted_posts_data,
        "is_following": is_following
    })

def unfollow(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(owner=user)
    user_profile = Profile.objects.get(owner=request.user)
    profile.followers.remove(request.user)
    user_profile.following.remove(user)

    return HttpResponseRedirect(reverse("profile_page", args=(username, )))

def follow(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(owner=user)
    user_profile = Profile.objects.get(owner=request.user)
    profile.followers.add(request.user)
    user_profile.following.add(user)
    return HttpResponseRedirect(reverse("profile_page", args=(username, )))

def following(request):
    user_profile = Profile.objects.get(owner=request.user)
    following_posts = []
    for us in user_profile.following.all():
        posts = Post.objects.filter(author=us)
        for post in posts:
            following_posts.append({
                "content": post.content,
                "author": post.author,
                "date": post.date,
                "likes": post.likes
            })
    sorted_following_posts = sorted(following_posts, key=lambda x: x["date"], reverse=True)
    paginator = Paginator(sorted_following_posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "following_posts": posts_page
    })

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        post.content = content
        post.save()
        return JsonResponse({'content': content})
    else:
        return JsonResponse({'error': 'Invalid request method'})