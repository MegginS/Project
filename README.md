## Unearth Palm

There are 193 endangered species that have palm oil production listed as one of their main threats. As the demand for palm oil rises, biodiverse forests are cleared to make way for palm oil plantations. Leaving animals such as the critically endangered orangutangs, pygmy elephants, Sumatran rhinoceroses, and Sumatran tigers with less and less habitat. Currently, there are about 47 million acres of palm oil plantations which is over 5x what it was 40 years ago. Palm oil can be found in 50% of all packaged products we find in supermarkets.

The consequences of palm oil production have led to consumer boycotts. Some companies have bypassed the boycotts by not explicitly labeling ingredients as “palm-oil” leaving the ethical consumer unaware that the product contains palm oil. In the United States palm oil can be listed under 200+ different names. This site allows you to search food product to check if it is made with palm.

## Technology Stack
   * **Backend:** Python, SQLAlchemy, Jinja, Flask
   * **Frontend:** HTML, CSS, Bootstrap, JavaScript, Ajax
   * **Database:** PostgreSQL
   * **API's:** FoodData Central API, USDA API (undocumented), News API

## Installation

Unearth Palm is not deployed, here is how to run the app locally:

Clone the repository:

```
git clone https://github.com/MegginS/UnearthPalm.git
```

Prerequisites:
* Python3
* PostgreSQL

Set up and activate a virtual environment, install dependencies:
```
cd Project
pip3 install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```
Setting up the database:

```
python3 seed_database.py
```

Obtaining and using API Keys:
* USDA API: request a key at https://fdc.nal.usda.gov/api-key-signup.html 
* Save USDA key in a file labeled "api_keys.txt"
* News API: request a key at https://newsapi.org/register
* Save News API key in a file labeled "news_key.txt"
* Add both text files to your .gitignore

Running the application:
```
python3 flask_app.py
Navigate to localhost:5000
```
## Contact 
Meggin Simon: megginsimon@gmail.com

Project Link: https://github.com/MegginS/Project
