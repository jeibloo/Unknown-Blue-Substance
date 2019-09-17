from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# Create user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode(280))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    # Here we define the relationship betwixt user and tweet
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet {self.text}>'
