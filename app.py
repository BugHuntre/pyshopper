from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

from Backend.config import BASE_DIR
from Backend.models import db
from routes.__init import register_all_routes  # <-- Import all Blueprints

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pyshopper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

register_all_routes(app)  # ✅ Register all Blueprints

@app.route("/")
def home():
    return "✅ PyShopper API is running."

if __name__ == "__main__":
    app.run(debug=False)
