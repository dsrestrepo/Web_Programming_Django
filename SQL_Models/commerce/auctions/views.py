from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django.contrib.auth.decorators import login_required
from .models import User, AuctionsListing, Bids, WatchList, Comments
from django.forms import ModelForm
from django import forms

from decimal import Decimal

#forms
class AuctionsForm(ModelForm):
    class Meta:
        model = AuctionsListing
        fields = ['productName', 'productDescription', 'startingBid', 'url', 'category' ]
        widgets = {  'productName':forms.TextInput(attrs={'class': 'productName', 'placeholder': 'Product Name...'}),
                'productDescription':forms.Textarea(attrs={'class': 'productDescription', 'placeholder': 'Product Description...'}),
            }
        labels = {
            "productName": "Name",
            "productDescription": "Description",
            'startingBid': "Starting Bid",
            'url': "url of image"
        }

class BidsForm(ModelForm):
    class Meta:
        model=Bids
        fields=['price']
        labes={'price':"Bid for the item"}

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {'comment':forms.Textarea(attrs={'class': 'comment', 'placeholder': 'Type your comment here...'})}
        labels = {"comment": "",}

class CategoryForm(ModelForm):
    class Meta:
        model = AuctionsListing
        fields = ['category']
        labels = {"category": ""}


def index(request):
    return render(request, "auctions/index.html", {
        "auctionListing":AuctionsListing.objects.all(),
        'bidsL':Bids.objects.all()
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


#create new item
@login_required
def createListing(request):
    if request.method=="POST":
        form=AuctionsForm(request.POST)
        if form.is_valid:
            #take the values
            productName = request.POST["productName"]
            productName = request.POST["productName"]
            productDescription = request.POST["productDescription"]
            startingBid = request.POST["startingBid"]
            url = request.POST["url"]
            category = request.POST["category"]
            state = True
            #take the user
            user_seller = request.user
            #create an AuctionsListing object and save
            auctionListing = AuctionsListing(productName = productName, productDescription = productDescription, startingBid = startingBid, url = url, category = category, user_seller = user_seller, state = state)
            auctionListing.save()
            return HttpResponseRedirect(reverse('listingPage',args=(auctionListing.id,)))
            #return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/createListing.html", {
            'form':form
            })
    return render(request,"auctions/createListing.html",{
        'form':AuctionsForm
    })

#page of the item, bids, and comments
def listingPage(request,item_id):
    auctionListing=AuctionsListing.objects.get(id=item_id)
    message=None
    #if POST
    if request.method=="POST":
        #capture wich form is (end of Auction, new bid or comment)
        form_type=request.POST.get("type_form") 
        
        #END OF THE AUCTION
        if 'state_form' in form_type:
            #new_state=bool(request.POST['state'])
            auctionListing.state=False
            auctionListing.save()
            HttpResponseRedirect(reverse('listingPage',args=(item_id,)))
        #ADD COMMENT
        if 'comment_form' in form_type:
            new_comment=request.POST['comment']
            comment=Comments(user=request.user,product=auctionListing,comment=new_comment)
            comment.save()
            HttpResponseRedirect(reverse('listingPage',args=(item_id,)))
        ##TRY TO OFFER NEW BID:
        elif 'bid_form' in form_type:
            form=BidsForm(request.POST)
            #check server side:
            if form.is_valid:
                new_price=Decimal(request.POST['price'])
                new_user=request.user
                #there are bids for the item?
                try:
                    bids = Bids.objects.get(product=item_id)
                except Bids.DoesNotExist:
                    bids = None
                #if yes verify user and value
                if bids:
                    price=bids.price
                    user=bids.user
                    user_seller=auctionListing.user_seller
                    if new_price > price and new_user != user_seller:
                        bids.price=new_price
                        bids.user=new_user
                        bids.save()
                        message="success bid!!! "
                    elif new_price <= price:
                        message="Your bid should be more than the actual"
                    elif new_user==user_seller:
                        message="you can't bid for your own product"
                else:
                    
                    stating_price=auctionListing.startingBid
                    if new_price > stating_price:
                        bids=Bids(user=new_user,product=auctionListing,price=new_price)
                        bids.save()
                        message="success bid"
                    else:
                        message:"Your bid should be more than the actual"
                request.session["inWatchlist"] = False
                #exist the whatchlist?
                try:
                    watchlist=request.user.watchlist.all()
                except request.DoesNotExist:
                    watchlist = None
                if watchlist:
                    #exist the item in the whatchlist?
                    if  auctionListing.watchlist.exists():
                        request.session["inWatchlist"] = True
                    else:
                        request.session["inWatchlist"] = False
                else:
                    request.session["inWatchlist"] = False
                #there are bids of the item? (Will be not if price is less or user is the owner)
                try:
                    bids = Bids.objects.get(product=item_id)
                except Bids.DoesNotExist:
                    bids = None    
                #there are comments of the item?
                comments = auctionListing.comments.all()

                return render(request, "auctions/listingPage.html",{
                    "auctionListing":auctionListing,
                    'bids':bids,
                    'inWatchlist':request.session["inWatchlist"],
                    'bidsForm':form,
                    'message':message,
                    'commentForm':CommentForm,
                    'comments':comments
                    })        
            else:
                request.session["inWatchlist"] = False
                #exist the whatchlist?
                try:
                    watchlist=request.user.watchlist.all()
                except request.DoesNotExist:
                    watchlist = None
                if watchlist:
                    #exist the item in the whatchlist?
                    if  auctionListing.watchlist.exists():
                        request.session["inWatchlist"] = True
                    else:
                        request.session["inWatchlist"] = False
                else:
                    request.session["inWatchlist"] = False
                #there are bids of the item?
                try:
                    bids = Bids.objects.get(product=item_id)
                except Bids.DoesNotExist:
                    bids = None   
                #there are comments of the item?
                comments = auctionListing.comments.all()

                return render(request, "auctions/listingPage.html",{
                    "auctionListing":auctionListing,
                    'bids':bids,
                    'inWatchlist':request.session["inWatchlist"],
                    'bidsForm':form,
                    'message':message,
                    'commentForm':CommentForm,
                    'comments':comments
                    })
    # Check if there already exists a "inWatchlist" key in our session
    if "inWatchlist" not in request.session:
        # If not, create a new list
        request.session["inWatchlist"] = False
    #if NO POST
    if request.user.is_authenticated:
        #exist the whatchlist?
        try:
            watchlist=request.user.watchlist.all()
        except request.DoesNotExist:
            watchlist = None
        print(watchlist)
        if watchlist:
            #exist the item in the whatchlist?
            if  auctionListing.watchlist.exists():
                request.session["inWatchlist"] = True
            else:
                request.session["inWatchlist"] = False
        else:
            request.session["inWatchlist"] = False
    #there are bids of the item?
    try:
        bids = Bids.objects.get(product=item_id)
    except Bids.DoesNotExist:
        bids = None
    #there are comments of the item?
    comments = auctionListing.comments.all()

    return render(request, "auctions/listingPage.html",{
        "auctionListing":auctionListing,
        'bids':bids,
        'inWatchlist':request.session["inWatchlist"],
        'bidsForm':BidsForm,
        'message':message,
        'commentForm':CommentForm,
        'comments':comments
    })


#add to Watchlist
@login_required
def watchList(request,item_id):
    auctionListing = AuctionsListing.objects.get(id=item_id)
    user=request.user
    #is there a watchlist of the user?
    try:
        watchlist=WatchList.objects.get(user=user.id)
    except WatchList.DoesNotExist:
        watchlist = None
    #if user have watchlist:
    if watchlist:
        if  auctionListing.watchlist.exists():
            #if exist the item in the watchlist, remove the item
            watchlist.product.remove(auctionListing)            
            return HttpResponseRedirect(reverse('listingPage',args=(item_id,)))
        else:
            #exis a watchlist for the user without the item
            #add the product
            watchlist.product.add(auctionListing)        
    #user doesn't have a watch list, create and add the product
    else:
        watchlist=WatchList.objects.create(user=user)
        watchlist.product.add(auctionListing)
    print('the watch list is: ', watchlist.product.all())
    return HttpResponseRedirect(reverse('seeWatchList'))


#see the watchlist
@login_required
def seeWatchList(request):
    user = request.user
    try:
        watchlist=WatchList.objects.get(user=user.id)
    except WatchList.DoesNotExist:
        watchlist = None
    #if exist watchlist:
    if watchlist:
        userwatchlist=watchlist.product.all()        
    #if not watchlist
    else:
        userwatchlist=None
    return render(request, 'auctions/seeWatchList.html', {
        'watchlist': userwatchlist,
        'bidsL':Bids.objects.all()
    })

#Categories list
def categories(request):    
    category='other' #by default
    if request.method == 'GET':
        form = CategoryForm(request.GET)
        # Check if form data is valid (server-side)
        if form.is_valid():
            category = form.cleaned_data["category"]
            return render(request, "auctions/categories.html", {
            "auctionListing":AuctionsListing.objects.all(),
            'bidsL':Bids.objects.all(),
            'form':form,
            'category':category
            })

    return render(request, "auctions/categories.html", {
        "auctionListing":AuctionsListing.objects.all(),
        'bidsL':Bids.objects.all(),
        'form':CategoryForm,
        'category':category
    })
