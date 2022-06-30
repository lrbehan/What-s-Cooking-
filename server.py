from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Comment, Rating, Recipe, SavedRecipe
import crud
from pprint import pformat
import os
import requests

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route('/users', methods=["POST"])
def register_user():
    """create a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user:
        flash(f'Cannot create an account with that email')
    else:
        user = crud.create_user(email, password)

        db.session.add(user)
        db.session.commit()
        flash('Account created please log in')
    return redirect('/')


@app.route('/login', methods=["POST"])
def login_user():
    """User login"""

    email = request.form.get("email")
    password = request.form.get("password")

    if crud.get_user_by_email(email):
        
        user = crud.get_user_by_email(email)
        if user.password != password:
            flash('Incorrect password')
            return redirect("/")
        else:
            session["user_email"] = user.email
            flash('Logged in')
            return redirect("/user_home") 
    else:
        flash('New email, please create account')
        return redirect("/")


@app.route('/logout')
def logout():
    """Logs out user."""
    del session["user_id"]

    return redirect("/")


@app.route('/user_home')
def user_home():
    """Show the User's homepage after login"""
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    
    recipes = crud.get_all_saved_recipes_for_user(user)
    
    return render_template('user_home.html', user=user, recipes=recipes)


API_KEY = os.environ['SPOONACULAR_KEY']

#Base url for spoonactular without endpoints
URL = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes'

# Spoonacular headers are added for every query
HEADERS = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"}


@app.route('/')
def homepage():
    """Show homepage."""
    
    search_endpoint = '/random' #endpoint for random
    payload = {"number":"1"}
       
    data = requests.request("GET", URL + search_endpoint, headers=HEADERS, params=payload).json()
    recipe = data['recipes'][0] #format of endpoint is different
    
    return render_template('homepage.html', recipe=recipe)
    

@app.route('/search')
def find_recipes():
    """Search for recipes on Spoonacular"""
    
    query = request.args.get('query', '')
    search_endpoint = '/complexSearch' #endpoint for search

    payload = {"ranking":"1", "query":request.args['query']} #get query from search page
       
    results = requests.request("GET", URL + search_endpoint, headers=HEADERS, params=payload).json()
    recipe_list = results['results'] 

    return render_template('search_results.html', recipe_list=recipe_list)


@app.route('/recipe')
def get_recipe_details():
    """Show recipe details"""
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    recipe_id = request.args['id']

    recipe = requests.request("GET", URL + (f"/{recipe_id}/information"), headers=HEADERS).json()
    
    ext_ingredients = recipe['extendedIngredients']
    ingredients=[]
    for ingredient in ext_ingredients:
        ingredients.append(ingredient)

    data = recipe['analyzedInstructions']
    if len(data) == 0:
        instructions = "instructions located at the Original Recipe Source"
    else:
        steps = data[0]['steps']
        instructions = []
        for step in steps:
            instructions.append(step['step'])

    saved_recipe_ids = [ recipe.recipe_id for recipe in user.saved_recipes ]
    return render_template('recipe_details.html', user=user, recipe=recipe, ingredients=ingredients, instructions=instructions, saved_recipe_ids=saved_recipe_ids)
    
    #example of an information request https://api.spoonacular.com/recipes/716429/information?apiKey=a3085bb64b4848fca7cf983ebc290d04  


@app.route('/saved_recipe/<recipe_id>')
def get_saved_recipe_details(recipe_id):
    """Show recipe details"""

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    recipe = crud.get_recipe_by_id(recipe_id)
    
    saved_recipe_ids = [ recipe.recipe_id for recipe in user.saved_recipes ]
    rated_recipe_ids = [ recipe.recipe_id for recipe in user.ratings ]
    
    return render_template("saved_recipe.html", recipe=recipe, rated_recipe_ids=rated_recipe_ids, saved_recipe_ids=saved_recipe_ids)


@app.route('/save', methods=['POST'])
def save_recipe():
    """Add recipe to database"""
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    rating_score = request.json.get("rating")
    
    json = request.json
    source_url = json['source_url'] 
    
    recipe_exists = Recipe.query.filter(Recipe.source_url==source_url).first()
    
    if recipe_exists:
        recipe = crud.get_recipe_by_source_url(source_url)
        saved_recipe = SavedRecipe.create(recipe.recipe_id, user.user_id)
    
        db.session.add(saved_recipe)
        db.session.commit()
    
    else:
        json = request.json
        title = json['title']
        ingredients = json['ingredients']
        instructions = json['instructions']
        image_path = json['image_path']
        source_url = json['source_url']
        
        recipe = crud.create_recipe(title=title, ingredients=ingredients, instructions=instructions, image_path=image_path, source_url=source_url)
    
        db.session.add(recipe)
        db.session.commit()

        saved_recipe = SavedRecipe.create(recipe.recipe_id, user.user_id)
    
        db.session.add(saved_recipe)
        db.session.commit()
    
    if rating_score is not None:
        rating = crud.create_rating(user, recipe.recipe_id, int(rating_score))
            
        db.session.add(rating)
        db.session.commit()
    
        return {
            "success": True,
                "status": f"You rated this recipe {rating_score} out of 5"}
    return {"status": "saved"}  
  

# @app.route('/edit_recipe')
# def display_edit_recipe_template():
    
#     original_recipe =
    
#     return render_template("edit_recipe.html", original_recipe=original_recipe)


# @app.route('/edit_recipe', methods="POST")
# def edit_recipe():
    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)