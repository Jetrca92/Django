from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, Listing


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
        
        #save user
        current_user = request.user
        ins = Listing(name=name, category=category_data, description=description, imgurl=imgurl, price=price, owner=current_user)
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
    return render(request, "auctions/entry.html", {
        "entry": entry
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

def watchlist_add(request, product_id):
    pass
    #if request.method == POST:
        #item_to_save = get_object_or_404(Listing, pk=product_id)
        # Check if the item already exists in that user watchlist
        #if WatchList.objects.filter(user=request.user, item=product_id).exists():
         #   messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
          #  return HttpResponseRedirect(reverse("auctions:index"))
        # Get the user watchlist or create it if it doesn't exists
        #user_list, created = WatchList.objects.get_or_create(user=request.user)
        # Add the item through the ManyToManyField (Watchlist => item)
        #user_list.item.add(item_to_save)
        #messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
        #return render(request, "auctions/watchlist.html")