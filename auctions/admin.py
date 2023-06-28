from django.contrib import admin
from .models import User, Auction_listings, Bids, Comments
# Register your models here.

admin.site.register(User)
admin.site.register(Auction_listings)
admin.site.register(Bids)
admin.site.register(Comments)