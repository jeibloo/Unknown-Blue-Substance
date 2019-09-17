from decouple import config
from flask import Flask, render_template, url_for, request
from .models import *
from .forms import twitterName


def create_app():
    # Create web server
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')

    # Add database to init.py? Idk why though
    # this db is imported from 'models'
    db.init_app(app)

    # Config stuff
    app.config['ENV'] = config('ENV')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # route needs to be made to figure out location
    @app.route("/")  # root route lmao
    @app.route("/index")  # main content
    def root():
        users = User.query.all()
        tweets = Tweet.query.all()
        return render_template('index.html', title="Le'Homme",
                               users=users, tweets=tweets)

    @app.route("/input")  # input route
    def input():
        return render_template('input.html', title='Input')

    return app


if __name__ == "__main__":
    app.run(debug=True)
