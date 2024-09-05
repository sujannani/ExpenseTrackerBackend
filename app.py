from flask import Flask # type: ignore
from flask_pymongo import PyMongo # type: ignore
from flask_marshmallow import Marshmallow # type: ignore
from config import Config
import os
app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
ma = Marshmallow(app)

from controllers.user_controller import *
from controllers.transaction_controller import *
from controllers.category_controller import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
