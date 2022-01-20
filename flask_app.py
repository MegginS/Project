from flask import (Flask, render_template, request, flash, session,
                   redirect)
from data_model import connect_to_db

app = Flask(__name__)

