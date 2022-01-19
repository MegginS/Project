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
 
    user_products = db.relationship("User_product", back_populates="users")

    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'

class User_product(db.Model):
    """A product saved by a user."""

    __tablename__ = "user_products"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    favorable = db.Column(db.Boolean, nullable=False)

    users = db.relationship("User", back_populates="user_products")
    products = db.relationship("Product", back_populates="user_products")

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
    ingredients = db.Column(db.String, nullable = False)
    brand = db.Column(db.String(50), nullable=False)
   
    user_products = db.relationship("User_product", back_populates="products")
    products_with_palm = db.relationship("Product_with_palm", back_populates="products")

    def __repr__(self):
        return f'<Product id={self.id} product name={self.name}>'
    
class Product_with_palm(db.Model):
    """A product containing palm"""

    __tablename__ = "products_with_palm"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    palm_alias_id = db.Column(db.Integer, db.ForeignKey("palm_aliases.id"))

    products = db.relationship("Product", back_populates="products_with_palm")
    palm_aliases = db.relationship("Palm_alias", back_populates="products_with_palm")

class Palm_alias(db.Model):
    """A palm alias"""

    __tablename__ = "palm_aliases"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    alias_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    products_with_palm = db.relationship("Product_with_palm", back_populates="palm_aliases")
