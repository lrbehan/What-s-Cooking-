"""Models for recipe saving app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # ratings = a list of Rating objects
    # comments = a list of Comment objects
    # recipes = a list of Recipe objects

    def__repr__(self):
        return f'<User user={self.user} email={self.email}>'




class Comment(db.Model):
    """User comments on recipes."""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    comment_body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), nullable=False)

    user = db.relationship("User", backref="comments")
    recipe = db.relationship("Recipe", backref="comments")


    def __repr__(self):
        return f'<Comment comment_id={self.comment_id} comment={self.comment}'



class Rating(db.Model):
    """User ratings of a recipes."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), nullable=False)

    user = db.relationship("User", backref="ratings")
    recipe = db.relationship("Recipe", backref="ratings")


    def __repr__(self):
        return f'<Rating rating_id={self.rating.id} score={self.score}>'


class Recipe(db.Model):
    """A recipe."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.Text)
    ingr_amount = db.Column(db.String)
    instructions = db.Column(db.Text)

    categories = db.relationship("Category", secondary="recipe_category", backref="recipes")

    # ratings = a list of Rating objects
    # comments = a list of Comment objects
    


    def __repr__(self):
        return f'<Recipe recipe_id={self.recipe_id}
                        name={self.name}
                        ingredients={self.ingredients}
                        ingr_amount={self.ingr_amount}
                        instructions={self.instructions}>'


class Category(db.Model):
    """A recipe category"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    category = db.Column(db.String) 
    
    #recipes


class RecipeCategory(db.Model):
    """Category of a specific recipe"""

    __tablename__ = "recipe_category"

    recipe_category_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)

    

def connect_to_db(flask_app, db_uri="postgresql:///recipes", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = false

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
