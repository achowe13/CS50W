from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path("login", views.Login, name="login"),
    path("logout", views.Logout, name="logout"),
    path("register", views.Register, name="register"),
    path("results", views.Results, name='results'),
    path("recipe_page/<int:page_id>", views.Recipe_page, name='recipe_page'),
    path("new_recipe", views.NewRecipe, name="new_recipe"),
    path("all_recipes_page", views.All_Recipes_Page, name="all_recipes_page"),
    path("my_recipes", views.Save_Recipe, name="save_recipe"),
    path("comment", views.Comments, name="comment"),
    path("rate", views.Rate, name="rate")
]