from model import db, User, Recipe, SavedRecipe, Rating, Comment, Category, connect_to_db

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_recipe(title, ingredients, instructions, image_path, source_url):
    """Create and return a recipe"""

    recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, image_path=image_path, source_url=source_url)

    return recipe
    

def get_recipe_by_id(recipe_id):
    """Return a recipe from database by recipe_id"""
    
    return Recipe.query.get(recipe_id)


def get_saved_recipe_by_recipe_id(recipe_id):

    return SavedRecipe.query.filter(SavedRecipe.recipe_id==recipe_id)


def get_recipe_by_source_url(source_url):
    """Return a recipe from the database by source_url"""

    return Recipe.query.filter(Recipe.source_url==source_url).first()


def get_all_saved_recipes_for_user(user):
    """Return all saved_recipes from db by user"""

    return SavedRecipe.query.filter(SavedRecipe.user==user).all()


def create_rating(user, recipe_id, score):
    """Create a rating"""

    rating = Rating(user=user, recipe_id=recipe_id, score=score)

    return rating


def get_ratings_by_user(user):
    """Get ratings by user"""

    return Rating.query.filter_by(user_id=user).all()

  
if __name__ == '__main__':
    from server import app
    connect_to_db(app)