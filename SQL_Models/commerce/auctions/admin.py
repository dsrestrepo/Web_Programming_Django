from django.contrib import admin

from .models import User,AuctionsListing, Bids, WatchList, Comments
# Register your models here.

admin.site.register(User)
admin.site.register(AuctionsListing)
admin.site.register(Bids)
admin.site.register(WatchList)
admin.site.register(Comments)
