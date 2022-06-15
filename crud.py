from model import db, User, Recipe, Rating, Comment, Category, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email)


def get_user_by_id(user_id):
    """return user by id"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)