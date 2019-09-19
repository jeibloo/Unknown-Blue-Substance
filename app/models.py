# This is really just database stuff I hate the name models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# Create user
class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    newest_tweet_id = db.Column(db.BigInteger)

    def __repr__(self):
        return f'<User {self.name}>'


class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Unicode(500))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'),
                        nullable=False)
    embedding = db.Column(db.PickleType, nullable=False)
    # Here we define the relationship betwixt user and tweet
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet {self.text}>'
