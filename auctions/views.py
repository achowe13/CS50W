from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime, timedelta
from .models import User, Auction_listings, Bids, Comments


#NOT LOGGED IN IS NOT WORKING WITH AUTHORIZATION!!!!!
#MUST FIX BEFORE HANDING IN


class newListingForm(forms.Form):
    item_name = forms.CharField(label='Item Name:', label_suffix='')
    description = forms.CharField(label='Description:', widget=forms.Textarea(attrs={'rows':5}))
    price = forms.DecimalField(label='Starting bid: $', max_digits=9, decimal_places=2, label_suffix='', min_value=0)
    image = forms.ImageField(label='Image:', required=False)
    category = forms.ChoiceField(label='Category', choices=(
        ('none','None'),
        ('electronics','Electronics'),
        ('apparal','Apparal'),
        ('sporting goods','Sporting Goods'),
        ('jewelry','Jewelry'),
        ('home & garden','Home & Garden'),
        ('toys','Toys'),
        ('other','Other')
        ))


class bidForm(forms.Form):
    bid = forms.DecimalField(label='Bid: $', max_digits=9, decimal_places=2, label_suffix='')


class commentForm(forms.Form):
    comment = forms.CharField(label='New Comment:', widget=forms.Textarea(attrs={'id':'new_comment_form', 'name':'comment'}))


def index(request):
    listings = Auction_listings.objects.filter(open=True).order_by('-timestamp')
    return render(request, 'auctions/index.html', {
        'listings':listings
    })
    

def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'auctions/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'auctions/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'auctions/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/register.html')
    

def Error(request, error):
    return render(request, 'auctions/error.html', {
        'error':error
    })


@login_required(login_url='/login')
def new_listing(request):
    if request.method == 'POST':
        newListing = newListingForm(request.POST, request.FILES)
        if newListing.is_valid():
            user = request.user
            item_name = newListing.cleaned_data['item_name']
            description = newListing.cleaned_data['description']
            price = newListing.cleaned_data['price']
            image = newListing.cleaned_data['image']
            category =  newListing.cleaned_data['category']
            auction_listing = Auction_listings(item_name=item_name, description=description, price=price, image=image, user=user, category=category)
            auction_listing.save()
            current_listing = Auction_listings.objects.filter(item_name=item_name).first()
            return HttpResponseRedirect(reverse('listing', kwargs={'id':current_listing.id}))
        else:
            return render(request, 'auctions/new_listing.html', {
                'form': newListingForm()
            })
    else:
        return render(request, 'auctions/new_listing.html', {
            'form': newListingForm()
        })

@login_required(login_url='/login')
def Listing(request, id):
    if request.method == 'GET':
        listing = Auction_listings.objects.filter(id=id).first()
        comments = Comments.objects.filter(item=id)
        watched_items = request.user.watchlist.all()
        watch_value = 'Watch'
        listing_owner = False
        winner = None        
        # change watch button to unwatch if listing is already being watched
        if listing in watched_items:
            watch_value = 'Unwatch'
        # checks if listing is created by the user so the user who created the listing can close the listing
        if listing.user == request.user:
            listing_owner = True
        # provides winner if bid is closed and says you win if user is the winning bidder
        if listing.open == False:
            winning_bid = Bids.objects.all().order_by('-bid_price').first()
            if request.user == winning_bid.user:
                winner = 'YOU WIN!'
            else:
                winner = winning_bid.user
        return render(request, 'auctions/listing.html', {
            'id':id,
            'listing':listing,
            'form':bidForm,
            'new_comment_form':commentForm,
            'comments':comments,
            'watch_value':watch_value,
            'is_open':listing.open,
            'listing_owner':listing_owner,
            'winner':winner
        })
    else:
        # bidform sent as post and request sent to new_bid function
        if bidForm(request.POST):
            return New_Bid(request, id)


# New_Bid function attempts to take a bid made my the user and make it the new highest bid
@login_required(login_url='/login')
def New_Bid(request, id):
    listing = Auction_listings.objects.filter(id=id).first()
    bidform_data = bidForm(request.POST)
    if bidform_data.is_valid():
        potential_bid = bidform_data.cleaned_data['bid']
        # return error if new bid is not above old/original bid
        if potential_bid <= listing.price:
            return Error(request, 'Any new bids must be higher than the current price of the item.')
        else:
            # save listing with new price
            listing.price = potential_bid 
            listing.save()
            # save new bid to Bids table
            bid = Bids(user=request.user, item_name=Auction_listings.objects.filter(id=id).first(), bid_price=potential_bid)
            bid.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'id':id}))
    else: 
        # if is_valid decides that your entry was not a valid entry
        return Error(request, 'Invalid form data was submitted.')


# render watchlist populated by all items watched by the user
@login_required(login_url='/login')
def Watchlist(request):
    watched_items = request.user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        'watched_items':watched_items
    })


# adds a new item to the user's watchlist
@login_required(login_url='/login')
def Add_to_Watchlist(request):
    listing_id = request.POST.get('id')
    user = request.user
    listing = Auction_listings.objects.filter(id=listing_id).first()
    watched_items = user.watchlist.all()
    if listing in watched_items:    
        user.watchlist.remove(listing_id)
        user.save()
        return Watchlist(request)
    user.watchlist.add(listing_id)
    user.save()
    return Watchlist(request)

def Categories_page(request):
    listings = Auction_listings.objects.all()
    used_categories = []
    for listing in listings:
        category = listing.category
        if category not in used_categories:
            used_categories.append(category)
    return render(request, 'auctions/categories.html', {
    'categories':used_categories
    })
        
        
def Category_filter_index(request):
    chosen_category = request.POST.get('category')
    listings_in_category = Auction_listings.objects.filter(category=chosen_category)
    if listings_in_category:
        return render(request, 'auctions/category_filter.html', {
        'listings':listings_in_category
    })
    else:
        return Error(request, 'No listings in this category')


@login_required(login_url='/login')
def New_Comment(request):
    user = request.user
    comment = request.POST.get('comment')
    item_id = request.POST.get('id')
    new_comment = Comments(name=user, comment=comment, item=Auction_listings.objects.filter(id=item_id).first())
    new_comment.save()
    return HttpResponseRedirect(reverse('listing', kwargs={'id':item_id}))


@login_required(login_url='/login')
def Close_Bid(request):
    user = request.user
    listing_id = request.POST.get('id')
    listing = Auction_listings.objects.filter(id=listing_id).first()
    if listing.user == user:
        listing.open = False
        listing.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'id':listing_id}))
    else:
        return Error(request, 'You are not authorized to close this auction!')

