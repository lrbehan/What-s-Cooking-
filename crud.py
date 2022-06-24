from model import db, User, Recipe, Rating, Comment, Category, connect_to_db

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_recipe(title, ingredients, instructions, image_path):
    """Create and return a recipe"""

    recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, image_path=image_path)

    return recipe
    
def get_recipe_by_id(recipe_id):
    """Return a recipe from database by recipe_id"""
    return Recipe.query.get(recipe_id)

  
if __name__ == '__main__':
    from server import app
    connect_to_db(app)