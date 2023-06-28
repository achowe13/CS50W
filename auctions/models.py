from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction_listings', related_name='watchlist')
    pass


class Auction_listings(models.Model):
    item_name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='static/auctions/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    timestamp = models.TimeField(auto_now_add=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item_name}: ${self.price} \n{self.description} \n{self.image} \n{self.user}"

class Bids(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    item_name = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name='bids')
    bid_price = models.DecimalField(max_digits=9, decimal_places=2)
    timestamp = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} bid ${self.bid_price} on {self.item_name} at: {self.timestamp}" 

class Comments(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)
    item = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.name} said {self.comment} at {self.timestamp}'
