"""Server for palm oil app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from data_model import connect_to_db
import api_calls

app = Flask(__name__)


# from jinja2 import StrictUndefined
# app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage, search, and login."""

    return render_template('homepage.html')

@app.route('/results')
def results():
    """View/save results of a search"""

    searched_item = request.args.get("searchedItem")
    search_results = api_calls.api_results(searched_item)


    return render_template('results.html', search_results =search_results)
    
@app.route('/profile')
def profile():
    """View profile"""
    
    return render_template('profile.html')

@app.route('/news')
def news():
    """View links to news articles."""
    
    return render_template('news.html')


@app.route('/map')
def deforestation_map():
    """View map of rainforest deforestation from Palm Oil"""
    
    return render_template('map.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)