import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Ingredient, Recipe, recipeIngredient, Comment, Save, Rating


def Index(request):
    ingredients = Ingredient.objects.all().order_by('name')
    return render(request, 'MGIH/index.html', {
        'ingredients':ingredients
    })


def Login(request):
    if request.method == 'POST':            
        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'MGIH/login.html', {
                'error': 'Incorrect username and/or password.'
            })
    else:
        return render(request, 'MGIH/login.html')


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')

        if password != conf_password:
            return render(request, 'MGIH/register.html', {
                'error': 'Passwords Do Not Match.'
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'MGIH/register.html', {
                'error': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'MGIH/register.html')
    
def Results(request):
    if request.method == 'POST':
        i = 0
        ingredients = []
        
        #unsure of number of ingredients added so uses while loop with break if no ingredient is found
        while True:
            ingredient = request.POST.get(f'ingredient[{i}]', None)
            ingredient = ingredient
            i = i + 1
            if ingredient == None:
                break
            else:
                ingredients.append(ingredient)

        recipes = Recipe.objects.filter(ingredients__name__in=ingredients).annotate(match_count=Count('ingredients')).order_by('-match_count')

        if recipes:
            for recipe in recipes:
                recipe_ingredients = recipe.ingredients.all()

                this_recipe_ingredients = []
                missing_ingredients = []
                
                for recipe_ingredient in recipe_ingredients:
                    this_recipe_ingredient = recipe_ingredient.name
                    this_recipe_ingredients.append(this_recipe_ingredient)
                    if this_recipe_ingredient not in ingredients:
                        missing_ingredients.append(this_recipe_ingredient)
                
                recipe.ingredient_names = this_recipe_ingredients
                recipe.missing_ingredients = missing_ingredients


        else:
            recipes = None
        
        paginator = Paginator(recipes, 10)
        
        page_num = 1
        
        if request.method == 'GET':
            page_num = request.GET.get('page')
        
        page = paginator.get_page(page_num)
        
        return render(request, 'MGIH/results.html', {
            'ingredients':ingredients,
            'page':page
        })
    else:
        return HttpResponseRedirect(reverse('index'))
    
def Recipe_page(request, page_id):
    recipe = Recipe.objects.get(id=page_id)
    user = request.user
    save_status = False
    
    if request.user.is_authenticated:
        saved_recipe = Save.objects.filter(user=user, recipe=recipe).first()
    else:
        saved_recipe = None
    
    if saved_recipe:
        save_status = True

    recipe_ingredients = recipe.ingredients.all()
    recipe_measurements = recipeIngredient.objects.filter(recipe=recipe)
    
    ingredients = []

    for recipe_ingredient in recipe_ingredients:
        ingredient = recipe_ingredient.name
        ingredients.append(ingredient)

    measurements = []
    for recipe_measurement in recipe_measurements:
        measurement = recipe_measurement.measurement
        measurements.append(measurement)   
    
    measurements_and_ingredients = zip(measurements, ingredients)

    comments = recipe.comments.all()

    page_ratings_object = Rating.objects.filter(recipe=recipe)

    adv_page_rating = 0
    number_of_ratings = len(page_ratings_object)

    if page_ratings_object:    
        page_ratings = [int(each_rating.rating) for each_rating in page_ratings_object]
        adv_page_rating = sum(page_ratings) / len(page_ratings)   
        adv_page_rating = round(adv_page_rating, 1)
    
    print(number_of_ratings, adv_page_rating)

    if request.user.is_authenticated:
        my_rate_object = Rating.objects.filter(user=user, recipe=recipe).first()
    else:
        my_rate_object = None

    my_rating = None

    if my_rate_object:
        my_rating = my_rate_object.rating

    count = [5,4,3,2,1]

    return render(request, 'MGIH/recipe_page.html', {
        'recipe':recipe,
        'm_and_i':measurements_and_ingredients,
        'saved':save_status,
        'comments':comments,
        'rating':my_rating,
        'count':count,
        'adv_rating':adv_page_rating,
        'number_of_ratings':number_of_ratings
    })


@login_required(login_url='/login')
def NewRecipe(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        total_time = request.POST.get('total_time')
        servings  = request.POST.get('servings')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        ingredients = []
        measurements = []
        i = 0
        j = 0

        while True:
            this_ingredient = request.POST.get(f'ingredient[{i}]', None)
            i = i + 1
            if this_ingredient == None:
                break
            else:
                ingredients.append(this_ingredient)
        
        while True:
            this_measurement = request.POST.get(f'measurement[{j}]', None)
            j = j + 1
            if this_measurement == None:
                break
            else:
                measurements.append(this_measurement)

        #return error if i and j do not match
        #if i and j do not match there is a different number of ingredients than there are measurments
        if i != j:
            return HttpResponse('must have both measurements and ingredients')
        
        ingredients_to_be_entered = []
        
        for ingredient in ingredients:
            found_ingredient = Ingredient.objects.filter(name=ingredient).first()
            if found_ingredient:
                ingredients_to_be_entered.append(found_ingredient)
            else:
                new_ingredient = Ingredient(name=ingredient, type='undefined')
                new_ingredient.save()
                new_found_ingredient = Ingredient.objects.filter(name=ingredient).first()
                ingredients_to_be_entered.append(new_found_ingredient)

        new_recipe = Recipe(name=name, description=description, prep_time=prep_time, cook_time=cook_time, total_time=total_time, servings=servings, image=image)
        
        new_recipe.save()

        for foo in range(len(ingredients_to_be_entered)):
            new_recipeIngredient = recipeIngredient(
                ingredient=ingredients_to_be_entered[foo],
                recipe=new_recipe,
                measurement=measurements[foo]
            )
            new_recipeIngredient.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        ingredients = Ingredient.objects.all().order_by('name')
        return render(request, 'MGIH/new_recipe.html',{
            'ingredients':ingredients
        })
    

def All_Recipes_Page(request):
    
    recipes = Recipe.objects.all()

    for recipe in recipes:
        recipe_ingredients = recipe.ingredients.all()
    
        ingredients = []

        for recipe_ingredient in recipe_ingredients:
            ingredient = recipe_ingredient.name
            ingredients.append(ingredient)

        recipe.ingredient_names = ingredients

    paginator = Paginator(recipes, 10)

    page_num = 1

    if request.method == 'GET':
        page_num = request.GET.get('page')
    
    page = paginator.get_page(page_num)

    return render(request, 'MGIH/all_recipes_page.html', {
        'page':page,
    })


@login_required(login_url='/login')
def Save_Recipe(request):
    
    user = request.user
    
    if request.method == 'POST':
        id = request.POST.get('id')
        recipe = Recipe.objects.get(id=id)
        try:
            already_saved = Save.objects.get(user=user, recipe=recipe)
        except ObjectDoesNotExist:
            already_saved = None

        if already_saved:
            already_saved.delete()
        else:
            recipe_to_save = Save(user=user, recipe=recipe)
            recipe_to_save.save()
        return HttpResponseRedirect(reverse('recipe_page', kwargs={'page_id':id}))
    
    else:
        saves = user.saved_recipes.all()
        saved_recipes = []

        for this_save in saves:
            saved_recipe = this_save.recipe
            saved_recipes.append(saved_recipe)

        if saved_recipes:
            
            for this_recipe in saved_recipes:
                ingredients = this_recipe.ingredients.all()
                ingredient_names = []
                
                for ingredient in ingredients:
                    ingredient_names.append(ingredient.name)
                this_recipe.ingredient_names = ingredient_names

        paginator = Paginator(saved_recipes, 10)

        page_num = 1

        if request.method == 'GET':
            page_num = request.GET.get('page')

        page = paginator.get_page(page_num)
        
        return render(request, 'MGIH/my_recipes.html', {
            'page':page,
        })
    

@login_required(login_url='/login')
def Comments(request):
    
    if request.method == 'POST':
        
        user = request.user
        page_id = request.POST.get('page_id')

        recipe = Recipe.objects.get(id=page_id)
        comment = request.POST.get('new_comment')

        new_comment = Comment(user=user, recipe=recipe, comment=comment)
        new_comment.save()

        return HttpResponseRedirect(reverse('recipe_page', kwargs={'page_id':page_id}))

    else:
        return HttpResponse('An error has occured!')
    

@login_required(login_url='/login')
def Rate(request):
    user = request.user
    data = json.loads(request.body)
    rating = int(data.get('rating', ''))

    if rating < 1 or rating > 5:
            return JsonResponse({'failure': 'invalid rating'}, status=403)
    page_id = data.get('page_id', '')
    
    recipe = Recipe.objects.get(id=page_id)
    users_previous_rating = Rating.objects.filter(user=user, recipe=recipe).first()

    if users_previous_rating:
        users_previous_rating.rating = rating
        users_previous_rating.save()
    else:
        user_rating = Rating(user=user, recipe=recipe, rating=rating)
        user_rating.save()

    return JsonResponse({'success': True}, status=200)