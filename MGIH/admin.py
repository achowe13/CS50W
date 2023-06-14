from django.contrib import admin
from .models import User, Ingredient, Recipe, recipeIngredient, Comment, Save, Rating

admin.site.register(User)
admin.site.register(Ingredient)   
admin.site.register(Recipe)
admin.site.register(recipeIngredient)
admin.site.register(Comment)
admin.site.register(Save)
admin.site.register(Rating)
