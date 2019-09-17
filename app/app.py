from flask import Flask, render_template, url_for
from .models import *


def create_app():
    # Create web server
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    # Add database to init.py? Idk why though
    # this db is imported from 'models'
    db.init_app(app)

    # route needs to be made to figure out location
    @app.route("/")  # root route lmao
    def root():
        users = User.query.all()
        tweets = Tweet.query.all()
        return render_template('index.html', title="Le'Homme",
                               users=users, tweets=tweets)

    # Another route
    # Routes do not have to be functions, usually use template
    @app.route("/about")
    def pred():
        return render_template('about.html')

    return app


if __name__ == "__main__":
    app.run(debug=True)
