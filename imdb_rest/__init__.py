import os
from flask import Flask
from imdb_rest.config import config
from imdb_rest.models import db, Names, Titles, ManyNamesHasManyTitles
from imdb_rest.movies import mod_movies


def create_app(config_name):
    app = Flask(__name__)

    # Load app configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init(
        app.config['DB_NAME'],
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASS'],
        port=app.config['DB_PORT']
    )

    # Create database tables if don't exist
    db.create_tables([Names, Titles, ManyNamesHasManyTitles], safe=True)

    import logging
    logger = logging.getLogger('peewee')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    # Connect to database before request
    @app.before_request
    def before_request():
        db.connect()
    
    # Close database connection after request
    @app.after_request
    def after_request(response):
        db.close()
        return response

    # Register blueprints
    app.register_blueprint(mod_movies)

    return app