from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:id>", views.Listing, name='listing'),
    path("error", views.Error, name="error"),
    path("watchlist", views.Watchlist, name="watchlist"),
    path("categories", views.Categories_page, name="categories"),
    path("category_filter", views.Category_filter_index, name="category_filter"),
    path("Add_to_Watchlist", views.Add_to_Watchlist, name="Add_to_Watchlist"),
    path("New_Comment", views.New_Comment, name="New_Comment"),
    path("Close_Bid", views.Close_Bid, name="Close_Bid")
]
