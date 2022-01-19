"""Models for palm oil app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
 
    user_product = db.relationship("User_product", back_populates="users")

    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'

class User_product(db.Model):
    """A product saved by a user."""

    __tablename__ = "user_products"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    favorable = db.Column(db.Boolean, nullable=False)

    user = db.relationship("User", back_populates="user_products")
    product = db.relationship("Product", back_populates="user_products")

    def __repr__(self):
        return f'<User Product id={self.id} user={self.user.first_name} product ={self.product.name}>'

class Product(db.Model):
    """A product."""

    __tablename__ = "products"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    contains_palm = db.Column(db.Boolean, nullable=False)
    rspo_certified = db.Column(db.Boolean, nullable=False)
    fdc_id = db.Column(db.Integer, nullable = False)
    ingredients = db.Column(db.Array, nullable = False)
    brand = db.Column(db.String(50), nullable=False)
   
    user_product = db.relationship("User_product", back_populates="products")

    def __repr__(self):
        return f'<Product id={self.id} product name={self.name}>'
    




def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
