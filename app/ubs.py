from decouple import config
from flask import Flask, render_template, request
import os
from .models import db, User
from .predict import predict_user
from .online import add_or_update_user, update_all_users


def create_app():
    SECRET_KEY = os.urandom(32)  # Cross site script away
    # Create web server
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV')
    app.config['SECRET_KEY'] = SECRET_KEY
    db.init_app(app)

    # route needs to be made to figure out location
    @app.route("/")  # root route lmao
    def root():
        return render_template('base.html', title="Comparison",
                               users=User.query.all())

    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', title='Update!',
                               users=User.query.all())

    @app.route('/reset')
    def reset():
        # db.drop_all()
        # db.create_all()
        # Hehe
        return render_template('base.html', title='Database Optimized!!!', user=[])

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # Make the name either the param or get it from the html user_name
        # using that app.route called '/user' w/ the POST method
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        # Put user1 and user2 in the html (the chosen values)
        # into user1 and user2 here in this function
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = "Can't compare themselves"
        else:
            # Grabs the name -> tweet_text from that input
            # and puts it in tweet_text
            tweet_text = request.values['tweet_text']
            confidence = int(predict_user(user1, user2, tweet_text)*100)
            if confidence >= 50:
                message = f'"{tweet_text}" is more likely for {user1} than {user2} w/ {confidence}% confidence.'
            else:
                message = f'"{tweet_text}" is more likely for {user2} than {user1} w/ {100-confidence}% confidence.'
        return render_template('prediction.html', title='Prediction',
                               message=message)

    return app


if __name__ == "__main__":
    app.run(debug=True)
