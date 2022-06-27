from model import db, User, Recipe, Rating, Comment, Category, connect_to_db

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_recipe(title, ingredients, instructions, image_path, source_url, user):
    """Create and return a recipe"""

    recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, image_path=image_path, source_url=source_url, user=user)

    return recipe
    

def get_recipe_by_id(recipe_id):
    """Return a recipe from database by recipe_id"""
    
    return Recipe.query.get(recipe_id)


def get_all_recipes_for_user(user_id):
    """Return all recipes from db by user"""
    
    return Recipe.query.filter(Recipe.user_id==user_id).all()


def create_rating(user, recipe, score):
    """Create a rating"""

    rating = Rating(user=user, recipe=recipe, score=score)

    return rating


def get_ratings_by_user(user):
    """Get ratings by user"""

    return Rating.query.filter_by(user_id=user).all()



def get_rating_by_recipe_and_user(recipe_id, user_id):
    """Get rating by user and recipe"""
    
    return Rating.query.filter_by(user_id=user, recipe_id=recipe_id).first()

  
if __name__ == '__main__':
    from server import app
    connect_to_db(app)