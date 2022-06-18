from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Comment, Rating, Recipe, Saved_Recipe
import crud

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True



@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


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

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash('email or password does not match')
    else:
        session["user_email"] = user.email
        flash('Logged in')
        return redirect("/user_home")


@app.route('/user_home')
def user_home():
    """Show the User's homepage after login"""

    return render_template('user_home.html')

API_KEY = os.environ['SPOONACULAR_KEY']

#Base url for spoonactular without endpoints
URL = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes'

# Spoonacular headers are added for every query
HEADERS = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"}

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

    recipe_id = request.args['id']

    recipe = requests.request("GET", URL + (f"/{recipe_id}/information"), headers=HEADERS).json()
    ingredients = recipe['extendedIngredients']

    return render_template('recipe_details.html', recipe=recipe, ingredients=ingredients)
    
    #example of an information request https://api.spoonacular.com/recipes/716429/information?apiKey=a3085bb64b4848fca7cf983ebc290d04






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)