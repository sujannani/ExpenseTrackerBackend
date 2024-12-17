from flask import Flask # type: ignore
from flask_pymongo import PyMongo # type: ignore
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
bcrypt=Bcrypt()

@app.route("/")
def index():
    return "Hello, World!"

from controllers.user_controller import *
from controllers.transaction_controller import *
from controllers.category_controller import *

if __name__ == '__main__':
    app.run(debug=True)
