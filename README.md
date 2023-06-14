# My Girl Is Hungry

## Description:
My Girl is Hungry is a project that solves the problem of looking in the fridge and never being able to decide on what to make.  Instead of struggling to come up with something to cook, just enter the ingredients you have on hand and you will be provided with recipes that best match what you already have!  It’s the best way to take the frustration out of deciding what to eat.

## Overview:
When you enter the website, you are greeted by a simple index page where you can see the layout navigation at the top and a space to enter ingredients in the bottom.  You can add in as many ingredients as you like by clicking the + button to add more boxes for entry, and then upon submitting you will be given a list of recipes based on the ingredients you have entered.  These recipes will be ordered by number of matching ingredients and you can click any of these recipes to enter into that recipe’s page.  In the recipe page you can see the entire recipe and directions as well as leave comments on the recipe, rate the recipe from one to five stars, see the average rating for the recipe, and save the recipe into your “my recipes list” to be able to access it at any time.  
But what if you don’t see a recipe for something you are already familiar with?  Then head to the “new recipe” page where you can enter any recipes you have on hand into our database where everyone can use it.  On while adding a new recipe, you can add pictures, cooking times, ingredients, and directions, as well as everything else needed for someone else to be able to create this recipe.

## Distinctiveness and Complexity:
This website uses 7 different Django models including a many to many relationship through another one of the models.  While using the page there is a login and registration function allowing users to create an account and sign in. Once signed in users can save recipes based on the individual user while also allowing access to restricted portions of the webpage which require being logged in.  Each user can also rate each recipe from 1 to 5 stars which the page will remember upon reentering the page, in addition to providing the total number of ratings and an average of all of the ratings so far.  Users can also enter new recipes into the database using a multi-part form allowing for pictures, directions, cook times, and any number of ingredients and measurements.  The ingredient dropdowns are populated with over 1100 ingredients and create new ones if there is an ingredient entered that is not in the database.
	This website fulfills the requirements for the capstone project because it:
-	Is distinct from other projects
-	Is **Not** a social networking platform
-	Is **Not** an e-commerce site
-	Utilizes Django with 7 different models
-	Utilizes JavaScript on the front end in MGIH/static/MGIH/MyGirlIsHungry.js
-	Is mobile responsive and looks the same with mobile

## File Contents
#### Front end:
	/Media/images: where image files for recipes are stored
	/MGIH/static/MGIH/MyGirlIsHungry.js: JavaScript file for project (only one but used with multiple pages with if statements)
	/MGIH/static/MGIH/styles.css: CSS style sheet
	/MGIH/templates/MGIH/all_recipes_page.html:  HTML for page showing all of the recipes in the database.
	/MGIH/templates/MGIH/index.html:  Home page of the application that allows entering ingredients for cross referencing.
	/MGIH/templates/MGIH/layout.html:  Layout used in conjunction with other pages to add navigation.
	/MGIH/templates/MGIH/login.html:  Page where user will log in to an already existing account.
	/MGIH/templates/MGIH/my_recipes.html:  Shows recipes saved by user (only available while logged in).
	/MGIH/templates/MGIH/new_recipe.html:  Allows users to enter new recipes into the database.
	/MGIH/templates/MGIH/recipe_page.html:  Page for each individual recipe showing entire recipe and directions as well as allowing users to save, leave comments and rate each recipe.
	/MGIH/templates/MGIH/register.html:  Register a new user
	/MGIH/templates/MGIH/results.html:  Displays results from search on index page

#### Back end:
	/MGIH/admin.py:  Used to implement admin page through django
	/MGIH/models.py:  Where the models were created
	/MGIH/urls.py:  Connect urls to different portions of the web application.
	/MGIH/views.py:  Where the main python code is located and all of the backend functions.
	/myGirlIsHumgry/settings.py:  Used to adjust settings and set location of saved files.
	/myGirlIsHumgry/urls.py:  Connects myGirlIsHumgry apps (e.g. admin and settings) to the rest of the application and runs through MGIH/urls.py
	/db.sqlite3:  SQL database where all tables are stored
	/ingredients.csv:  CSV file used to enter ingredients into SQL table
	/manage.py:  not edited but used to run server, make migrations, ect.
	/README.md:	  This file, the one you are looking at, this one.
	/requirements.txt:  Requirements to run the application.

## Installation and Running:
-	‘pip install -r requirements.txt’
-	‘python manage.py migrate’
-	‘python manage.py runserver’

## Demonstration:
https://youtu.be/qpQggMQzwlQ


