import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'movie_library.db'

def create_app():
    app = Flask(__name__)
    # Bootstrapping application
    Bootstrap(app)
    # App configuration
    app.config.from_mapping(
        SECRET_KEY='INSERT_SECRET_KEY',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)

    from . import auth
    from . import views
    app.register_blueprint(auth.bp, url_prefix='/')
    app.register_blueprint(views.bp, url_prefix='/')

    from . import models

    with app.app_context():

        db.create_all()

        # new_movie = models.Movie(
        #     title="Phone Booth",
        #     year=2002,
        #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's "
        #                 "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a "
        #                 "jaw-dropping climax.",
        #     rating=7.3,
        #     review="My favourite character was the caller.",
        #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
        # )
        # db.session.add(new_movie)
        #
        # db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app
