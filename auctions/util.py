from datetime import datetime, timedelta
from .models import Auction_listings, Bids

# adds a countdown feature until bids close
# bid_start_time is in a different format from timedelta and must be changed unless this function will
# always return an error saying you cant use '+' operator on 'bid_start_time + timedelta(days=7)'
def Remaining_Bid_Time(id):
    listing = Auction_listings.objects.filter(id=id).first()
    bid_start_time = datetime.fromtimestamp(listing.timestamp) 

    remaining_time = bid_start_time + timedelta(days=7) - datetime.now()
    return remaining_time