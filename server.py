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
        flash('Cannot create an account with that email')
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
    del session["user_email"]

    return redirect("/")


@app.route('/user_home')
def user_home():
    """Show the User's homepage after login"""
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    
    recipes = crud.get_all_saved_recipes_for_user(user)
    ratings = crud.get_ratings_by_user(user.user_id)
    
    return render_template('user_home.html', user=user, recipes=recipes, ratings=ratings)


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
    
    payload = {"ranking":"1", 'instructionsRequired': True, "query":request.args['query']}
    
    results = requests.request("GET", URL + search_endpoint, headers=HEADERS, params=payload).json()
    recipe_list = results['results'] 

    return render_template('search_results.html', recipe_list=recipe_list)


@app.route('/recipe')
def get_recipe_details():
    """Show recipe details"""
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    if not user:
        flash ("You must login")
        return redirect("/")

    recipe_id = request.args['id']
    
    #endpoint for recipe details
    recipe = requests.request("GET", URL + (f"/{recipe_id}/information"), headers=HEADERS).json() 
    
    title = recipe['title']
    source_url = recipe['sourceUrl']
    image = recipe['image']

    ext_ingredients = recipe['extendedIngredients']
    ingredients=[]
    for ingredient in ext_ingredients:
        ingredients.append(ingredient['original'])

    data = recipe['analyzedInstructions']
    if len(data) == 0:
        instructions = "Instructions located at original recipe source"
    else:
        steps = data[0]['steps']
        instructions = []
        for step in steps:
            instructions.append(step['step'])
 
    saved_recipe_ids = [ recipe.recipe_id for recipe in user.saved_recipes ]
    rated_recipe_ids = [ recipe.recipe_id for recipe in user.ratings ]

    return render_template('recipe.html', is_API=True, user=user, recipe=recipe, title=title, source_url=source_url, image=image, ingredients=ingredients, instructions=instructions, saved_recipe_ids=saved_recipe_ids, rated_recipe_ids=rated_recipe_ids)
    

@app.route('/saved_recipe/<recipe_id>')
def get_saved_recipe_details(recipe_id):
    """Show recipe details"""

    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)
    
    recipe = crud.get_recipe_by_id(recipe_id)

    rating = crud.get_user_recipe_rating(user, recipe)
    
    saved_recipe_ids = [ recipe.recipe_id for recipe in user.saved_recipes ]
    rated_recipe_ids = [ recipe.recipe_id for recipe in user.ratings ]

    title = recipe.title
    source_url = recipe.source_url
    image = recipe.image_path

    ingredients = recipe.ingredients.split("\n")
    instructions = recipe.instructions.split("\n")
    
    return render_template("recipe.html", is_API=False, recipe=recipe, rated_recipe_ids=rated_recipe_ids, saved_recipe_ids=saved_recipe_ids, rating=rating, title=title, source_url=source_url, image=image, ingredients=ingredients, instructions=instructions)


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

        recipe = crud.get_last_recipe_by_source_url(source_url)
    
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

    
    if rating_score is not None:
        rating = crud.create_rating(user, recipe.recipe_id, int(rating_score))
            
        db.session.add(rating)
        db.session.commit()
        return {
            "success": True,
            "status": f"You rated this recipe {rating_score} out of 5"}
    else:
        saved_recipe = SavedRecipe.create(recipe.recipe_id, user.user_id)
    
        db.session.add(saved_recipe)
        db.session.commit()
        return {"status": "saved"}  


@app.route('/edit_recipe', methods=["POST"])
def save_updated_recipe():
    
    logged_in_email = session.get("user_email")
    user = User.get_by_email(logged_in_email)

    title = request.form.get("title")
    ingredients = request.form.get("edit_ingredients")
    instructions = request.form.get("edit_instructions")
    
    image_path = request.form.get("image")
    source_url = request.form.get("source_url")
    
    # remove original recipe from favorite list
    recipe = crud.get_last_recipe_by_source_url(source_url)
    recipe_id = recipe.recipe_id
    crud.unsave_recipe(recipe_id)
    rated_recipe_ids = [ recipe.recipe_id for recipe in user.ratings ]
    if recipe_id in rated_recipe_ids:
        crud.unsave_rating(recipe_id)

    # save the edited recipe
    recipe = crud.create_recipe(title=title, ingredients=ingredients, instructions=instructions, image_path=image_path, source_url=source_url)
    db.session.add(recipe)
    db.session.commit()

    # add to favorite list
    saved_recipe = SavedRecipe.create(recipe.recipe_id, user.user_id)
    db.session.add(saved_recipe)
    db.session.commit()

    recipe_id = saved_recipe.recipe_id

    return redirect (f"/saved_recipe/{recipe_id}")

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)