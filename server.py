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

API_KEY = os.environ['SPOONACULAR_KEY']

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
    """Show the User's homepage."""

    return render_template('user_home.html')

@app.route('/search')
def find_recipes():
    """Search for recipes on Spoonacular"""

    query = request.args.get('query', '')

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch'
    payload = {'apiKey': API_KEY, 'query': query}

    headers = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"}
       
    results = requests.request("GET", url, headers=headers, params=payload)
    print(results.text)

    return render_template('search_results.html')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)