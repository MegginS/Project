import data_model
from flask import (Flask, render_template)

def load_favorites(email):
    current_user = data_model.User.query.filter(data_model.User.email == email).first().id
    user_favorites = data_model.UserProduct.query.filter(data_model.UserProduct.user_id == current_user).all()

    favorites = []
    for favorite in user_favorites:
        product_info = data_model.Product.query.filter(data_model.Product.id == favorite.product_id).first()
        favorites.append(product_info)
        
    return favorites
