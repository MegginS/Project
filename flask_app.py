"""Server for palm oil app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect, make_response)
import data_model
import api_calls, news_api, api_alternatives
import bcrypt

app = Flask(__name__)

from jinja2 import StrictUndefined
app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage, search."""

    return render_template('homepage.html')


@app.route('/results')
def results():
    """View/save results of a search"""

    searched_item = request.args.get("searchedItem")
    search_results = api_calls.api_results(searched_item)

    return render_template('results.html', search_results = search_results)

@app.route('/alternatives')
def show_alternatives():
    
    email = session.get('email')
    
    if email is None:
        flash("Login to save palm alternatives")

    food_category = request.args.get("alternative")
    all_alternatives = api_alternatives.api_alternatives(food_category)
    user_id = data_model.User.query.filter(data_model.User.email == email).first().id

    return render_template('alternatives.html', all_alternatives = all_alternatives, email = email, user_id = user_id)

@app.route("/saving-products", methods = ["POST"])
def save_alternative():

    ids = request.json.get("ids")
# query for a user with that email - get id
# pass product and get product id
# create user with product

    print(ids)
    return {}
# should return "added"


@app.route('/profile')
def show_login():

    email = session.get('email')
    if email is not None:
        current_user = data_model.User.query.filter(data_model.User.email == email).first().id
        # user_favorites = data_model.Product.query.filter(data_model.Product.user_products.user_id == current_user).all()
        user_favorites = data_model.UserProduct.query.filter(data_model.UserProduct.user_id == current_user).all()
        
        favorites = []
        for favorite in user_favorites:
            product_info = data_model.Product.query.filter(data_model.Product.id == favorite.product_id).first()
            favorites.append(product_info)
            
        return render_template('profile.html', email = email, favorites = favorites)
   
    return render_template('login.html')

@app.route('/profile', methods = ['POST'])
def handle_login():
    """Log user into application."""

    email = request.form["email"]
    password = bytes(request.form["password"], "utf-8")
    user = data_model.User.query.filter(data_model.User.email == email).all()

    if len(user) > 0:
        hashedpassword = bytes(user[0].password, "utf-8")
        if bcrypt.checkpw(password, hashedpassword):
            session['email'] = email
            return render_template('profile.html', email = email)
    return render_template('login.html')


@app.route('/new_user')
def show_new_user():

    return render_template('new_user.html')

@app.route('/forgot_password')
def forgot_password():

    return render_template('forgot_password.html')    

@app.route('/new_user', methods = ['POST'])
def add_new_user():
    """Adding a New User"""

    email = request.form["email"]
    password = request.form["password"].encode("utf-8")
    password_check = request.form["password2"].encode("utf-8")
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    user = data_model.get_user_by_email(email)

    if user:
        flash("An account is already associated with this email")
        return render_template('new_user.html')
    else:
        if password == password_check:
            hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
            data_model.create_user(email = email, password = hashed, first_name = first_name, last_name = last_name)
            return render_template('login.html')
        else:
            flash("Username and Password do not match")
            return render_template('new_user.html')

@app.route('/news')
def news():
    """View links to news articles."""

    all_articles = news_api.news_api_results()
    
    return render_template('news.html', all_articles = all_articles)


@app.route('/map')
def deforestation_map():
    """View map of rainforest deforestation from Palm Oil"""
    
    return render_template('map.html')



if __name__ == "__main__":
    data_model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)