from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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


def new_listing(request):
    if request.method == "POST":
        
        #save form data to db
        name = request.POST['title']
        category = request.POST['category']
        description = request.POST['description']
        imgurl = request.POST['imgurl']
        
        #if no url for img, assign default value
        if imgurl == '':
            imgurl = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930"
        price = request.POST['starting_bid']

        #get content of a particular category
        category_data = Category.objects.get(category_name=category)

        #save bid and user
        current_user = request.user
        bid = Bid(bid=float(price), user=current_user)
        bid.save()
        ins = Listing(name=name, category=category_data, description=description, imgurl=imgurl, price=bid, owner=current_user)
        ins.save()
        return render(request, "auctions/new_listing_saved.html")

    else:
        #display new listing form
        return render(request, "auctions/new_listing.html", {
            "categories": Category.objects.all()
        })

def entry(request, title):
    #render content for title provided
    entry = Listing.objects.get(name=title)
    is_in_watchlist = request.user in entry.watchlist.all()
    comments = Comment.objects.filter(listing=entry)
    return render(request, "auctions/entry.html", {
        "entry": entry,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments

    })

def category_list(request):
    #render list of categories
    categories = Category.objects.all()
    return render(request, "auctions/category_list.html", {
        "categories": categories
    })

def display_cat(request, title):
    #render content for category provided    
    category = Category.objects.get(category_name=title)
    listings = Listing.objects.filter(is_active=True, category=category)
    return render(request, "auctions/cat.html", {
        "category": category,
        "listings": listings
    })

def user_adds(request, user):
    #render page for adds by specific user
    owner = User.objects.get(username=user)
    user = Listing.objects.filter(is_active=True, owner=owner)
    return render(request, "auctions/user_adds.html", {
        "listings": user,
        "owner": owner
    })

def watchlist_add(request, id):
    #adds item to users watchlist
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("entry", args=(listing.name, )))

def watchlist_remove(request, id):
    #removes item from users watchlist
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("entry", args=(listing.name, )))

def watchlist(request):
    #render watchlist page
    user= request.user
    items = Listing.objects.filter(watchlist=user)
    return render(request, "auctions/watchlist.html", {
        "items": items
    })

def comment(request):
    #saves comment to comment model
    if request.method == "POST":
        id = request.POST['id']
        listing = Listing.objects.get(pk=id)
        user = request.user
        comment = request.POST['comment']
        ins = Comment(author=user, listing=listing, message=comment)
        ins.save()
        return HttpResponseRedirect(reverse("entry", args=(listing.name, )))

def new_bid(request, id):
    if request.method == "POST":
        #get data
        new_bid = int(request.POST['bid'])
        user = request.user
        entry = Listing.objects.get(pk=id)
        entry.watchlist.add(user)
        is_in_watchlist = request.user in entry.watchlist.all()
        comments = Comment.objects.filter(listing=entry)
        #if new bid valid, update data
        if new_bid > entry.price.bid:
            update_bid = Bid(user=user, bid=new_bid)
            update_bid.save()
            entry.price = update_bid
            entry.save()
            return render(request, "auctions/entry.html", {
                "entry": entry,
                "is_in_watchlist": is_in_watchlist,
                "comments": comments
            })
        else:
            #if new bid invalid, render error
            return render(request, "auctions/error.html", {
                "entry": entry
            })

def close_bid(request, id):
    if request.method == "POST":
        #get data
        entry = Listing.objects.get(pk=id)
        close = request.POST['close_bid']
        if close:
            #change owner and active status
            entry.is_active = False
            entry.owner = entry.price.user
            entry.save()
            return render(request, "auctions/closed.html", {
                "entry": entry
            })
        else:
            pass
        
