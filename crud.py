from model import db, User, Recipe, Rating, Comment, Category, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_user_by_id(user_id):
    """return user by id"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_recipe(title, ingredients, instructions):
    """Create and return recipe after edit"""
    recipe = Recipe(title = title, ingredients = ingredients, instructions = instructions)
    return recipe

def get_recipes():
    """Return all recipes."""
    return Recipe.query.all()

def get_recipe_by_id(recipe_id):
    """Return recipe by recipe_id"""
    return Recipe.query.get(recipe_id)

def get_recipes_saved(user_id):
    """Return recipes saved by specific user"""
    return Recipe.query.filter(SavedRecipe.user_id).all()


    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)