from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.createListing, name="createListing"),
    path("Listing_Page/<int:item_id>", views.listingPage, name="listingPage"),
    path("watchList/<int:item_id>", views.watchList,name="watchList"),
    path("seeWatchList", views.seeWatchList,name="seeWatchList"),
    path("categories", views.categories,name="categories")
    ]
    
