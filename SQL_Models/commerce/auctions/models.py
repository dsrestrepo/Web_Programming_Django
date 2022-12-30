from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class AuctionsListing(models.Model):
    category_options = [
        ('tecno', 'Technology'),
        ('books', 'Books'),
        ('cloth', 'Clothes'),
        ('Healt', 'Health'),
        ('Home', 'Home'),
        ('other', 'Others'),
        ('music', 'Music'),
        ('sport', 'Sports'),
        ('pets', 'Pets'),
        ('food', 'Food'),
        ('games', 'Games')
    ]
    productName = models.CharField(max_length=64)
    productDescription = models.TextField()
    startingBid = models.DecimalField(max_digits=8, decimal_places=2)
    url = models.URLField()
    category = models.CharField(max_length=8, choices=category_options, default='other')
    state = models.BooleanField()
    user_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product")
    
    def __str__(self):
        return f"the product {self.productName} offered for user: {self.user_seller} at: {self.startingBid}"


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bids")
    product = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE,null = True, blank = True,related_name="bids")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"The user {self.user} has offered {self.price} for the product {self.product}"


class WatchList(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="watchlist")
    product=models.ManyToManyField(AuctionsListing, blank=True, related_name="watchlist")

    def __str__(self):
        return f"the user {self.user} has a whatch list"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"the user {self.user} has commented {self.product}"

