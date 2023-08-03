from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("RENDER_DB_URI")

    from app.models.data import Data
    from app.models.job import Job

    db.init_app(app)
    migrate.init_app(app, db)

    # # Register Blueprints here
    # from .routes.data_routes import data_bp
    # from .routes.jobs_routes import jobs_bp

    # app.register_blueprint(data_bp)
    # app.register_blueprint(jobs_bp)



    CORS(app)
    return app