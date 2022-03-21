"""Server for palm oil app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect, make_response)
import data_model
import api_calls, news_api, api_alternatives, functions
import bcrypt
import requests

app = Flask(__name__)

from jinja2 import StrictUndefined
with open('flask_key.txt') as f:
    app.secret_key = f.readline().strip()


app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage, search."""

    email = session.get('email')
    return render_template('homepage.html', email = email)


@app.route('/results')
def results():
    """View/save results of a search"""

    email = session.get('email')
    searched_item = request.args.get("searchedItem")

    with open('api_keys.txt') as f:
        api_key = f.readline().strip()
    payload = {'query': searched_item,'dataType': 'Branded','api_key': api_key}

    try:
        response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', params = payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return redirect('/')
    except requests.exceptions.RequestException:
        return redirect('/')

    search_results = api_calls.api_results(searched_item)
    
    if email is None:
        user_id = None
        flash("Login to save products")

    return render_template('results.html', search_results = search_results, email = email)

@app.route('/alternatives')
def show_alternatives():
    
    email = session.get('email')
    
    food_category = request.args.get("alternative")
    
    all_alternatives = api_alternatives.api_alternatives(food_category)

    if email is None:
        user_id = None
        flash("Login to save palm alternatives")
    else:
        user_id = data_model.User.query.filter(data_model.User.email == email).first().id
        
    return render_template('alternatives.html', all_alternatives = all_alternatives, email = email, user_id = user_id)


@app.route("/saving-product", methods = ["POST"])
def save_alt():
    
    email = session.get('email')

    product_id = request.json.get("productId")
    user_id = data_model.User.query.filter(data_model.User.email == email).first().id

    userproduct = data_model.UserProduct.query.filter(data_model.UserProduct.product_id == product_id, data_model.UserProduct.user_id == user_id).first()

    if userproduct is None:
        data_model.create_saved_product(product_id, user_id)
    return "success"

@app.route('/profile')
def show_login():

    email = session.get('email')

    if email:
        favorites = functions.load_favorites(email)
        user = data_model.User.query.filter(data_model.User.email == email).first().first_name
        user = user.title()

        return render_template('profile.html', email = email, favorites = favorites, user = user)
    else:
        return render_template('login.html', email = email)

@app.route('/profile', methods = ['POST'])
def handle_login():
    """Log user into application."""

    email = request.form["email"]
    password = bytes(request.form["password"], "utf-8")
    username = data_model.User.query.filter(data_model.User.email == email).all()
 

    if len(username) > 0:
        hashedpassword = bytes(username[0].password, "utf-8")
        user = data_model.User.query.filter(data_model.User.email == email).first().first_name
        user = user.title()
        if bcrypt.checkpw(password, hashedpassword):
            session['email'] = email
            favorites = functions.load_favorites(email)
            return render_template('profile.html', email = email, favorites = favorites, user = user)
        else:
            flash("Invalid Password")
            return render_template('login.html', email = None)

    else:
        return render_template('login.html', email = None)

@app.route('/logout')
def handle_logout():
    """Logout user."""

    session.pop('email', None)
    return redirect('/')


@app.route('/new_user')
def show_new_user():

    return render_template('new_user.html', email = None)

@app.route('/forgot_password')
def forgot_password():

    email = session.get('email')
    return render_template('forgot_password.html', email = None)

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
        return render_template('new_user.html', email = None)
    else:
        if password == password_check:
            hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
            data_model.create_user(email = email, password = hashed, first_name = first_name, last_name = last_name)
            return render_template('login.html', email = None)
        else:
            flash("Username and Password do not match")
            return render_template('new_user.html', email = None)

@app.route('/news')
def news():
    """View links to news articles."""

    email = session.get('email')
    all_articles = news_api.news_api_results()
    
    return render_template('news.html', all_articles = all_articles, email = email)


@app.route('/FAQ')
def information():
    """Information page on Oil Palm """

    email = session.get('email')
    return render_template('info.html', email = email)


if __name__ == "__main__":
    data_model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)