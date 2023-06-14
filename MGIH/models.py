from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"ingredient: {self.name}, type: {self.type}, created at {self.timestamp}"


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='recipeIngredient')
    timestamp = models.DateTimeField(auto_now_add=True)
    prep_time = models.CharField(max_length=32)
    cook_time = models.CharField(max_length=32)
    total_time = models.CharField(max_length=32)
    servings = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return f"Recipe name: {self.name}"


class recipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    measurement = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"recipe: {self.recipe}, measurement: {self.measurement}, ingredient: {self.ingredient}"
   

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {self.user}, commented on the recipe: {self.recipe}, and commented: {self.comment}"


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved_by')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {self.user}, saved the recipe: {self.recipe}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user {self.user}, rated {self.recipe} {self.rating} stars at {self.timestamp}"