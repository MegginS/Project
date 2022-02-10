"""Server for palm oil app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
import data_model
import api_calls, news_api, api_alternatives
import bcrypt

app = Flask(__name__)


# from jinja2 import StrictUndefined
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined

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
    
    all_alternatives = api_alternatives.api_alternatives()

    return render_template('alternatives.html', all_alternatives = all_alternatives)

@app.route('/profile')
def show_login():

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
            return render_template('profile.html', email = email, password = password)
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

    if password == password_check:
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
        data_model.create_user(email = email, password = hashed, first_name = first_name, last_name = last_name)
        return render_template('login.html')
    else:
        # flash message
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