from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os
import logging

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #     "SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLY_DATABASE_URI")
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    from app.models.data import Data
    from app.models.job import Job
    
    app.logger.setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    # app.logger.info("Initializing db with flask app")
    #logging.info("Initializing db with the flask app")
    db.init_app(app)
    app.logger.info("Dropping all tables")
    with app.app_context():
        db.drop_all()
        app.logger.info("Creating all tables")
        db.create_all()
        app.logger.info(repr(db.metadata))

    # app.logger.info("Migrating db")
    #logging.info("Migrating db")
    migrate.init_app(app, db)
    
    app.logger.info("DB prep is done.")
    logging.info("DB preparation done.")

    # # Register Blueprints here
    from .routes.data_route import data_bp
    from .routes.job_route import jobs_bp

    app.register_blueprint(data_bp)
    app.register_blueprint(jobs_bp)


    CORS(app)
    return app