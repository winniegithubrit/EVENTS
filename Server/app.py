from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import *

app = Flask(__name__)
app.config.from_object('config.Config')

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

if __name__ == "__main__":
    app.run()