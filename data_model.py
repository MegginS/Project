"""Models for palm oil app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(200), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    user_products = db.relationship("UserProduct", back_populates="users")

def create_user(email, password, first_name, last_name):
    """Create and return a new user."""

    new_user = User(
                    email = email,
                    password = password,
                    first_name = first_name,
                    last_name = last_name)

    db.session.add(new_user)
    db.session.commit()

    return new_user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

class UserProduct(db.Model):
    """A product saved by a user."""

    __tablename__ = "user_products"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    users = db.relationship("User", back_populates="user_products")
    products = db.relationship("Product", back_populates="user_products")

def create_saved_product(product_id, user_id):
    """Create and return a users product."""

    saved_product = UserProduct(
                    product_id = product_id,
                    user_id = user_id)

    db.session.add(saved_product)
    db.session.commit()

    return saved_product


class Product(db.Model):
    """A product."""

    __tablename__ = "products"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    descriptor = db.Column(db.String(400), nullable = True)
    contains_palm = db.Column(db.String(300), nullable = True)
    fdc_id = db.Column(db.Integer, nullable = True)
    ingredients = db.Column(db.ARRAY(db.String), nullable = True)
    brand = db.Column(db.String(50), nullable=True)

    user_products = db.relationship("UserProduct", back_populates="products")
    products_with_palm = db.relationship("ProductWithPalm", back_populates="products")


def create_product(name, descriptor, contains_palm, fdc_id, ingredients, brand):
    """Create and return a product."""

    product = Product(name = name,
                     descriptor = descriptor,
                     contains_palm = contains_palm,
                     fdc_id = fdc_id,
                     ingredients = ingredients,
                     brand = brand)

    db.session.add(product)
    db.session.commit()

    return product


class ProductWithPalm(db.Model):
    """A product containing palm"""

    __tablename__ = "products_with_palm"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    palm_alias_id = db.Column(db.Integer, db.ForeignKey("palm_aliases.id"))

    products = db.relationship("Product", back_populates="products_with_palm")
    palm_aliases = db.relationship("PalmAlias", back_populates="products_with_palm")

def create_product_with_palm(product_id, palm_alias_id):
    """Create and return a palm product."""
    palm_product = ProductWithPalm(
                    product_id = product_id,
                    palm_alias_id = palm_alias_id)
                    
    return palm_product


class PalmAlias(db.Model):
    """A palm alias"""

    __tablename__ = "palm_aliases"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    alias_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    products_with_palm = db.relationship("ProductWithPalm", back_populates="palm_aliases")

def create_alias(alias_name, description):
    "Create and return a palm alias"
    palm_alias = PalmAlias(
                            alias_name = alias_name,
                            description = description)
    return palm_alias

class PossiblePalm(db.Model):
    """A palm alias"""

    __tablename__ = "possible_palm_aliases"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    alias_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

def create_possible_alias(alias_name, description):
    "Create and return a possible palm alias"
    palm_alias = PossiblePalm(
                            alias_name = alias_name,
                            description = description)
    return palm_alias

def connect_to_db(flask_app, db_uri="postgresql:///palm", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)


if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
