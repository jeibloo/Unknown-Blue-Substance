import basilica
import tweepy
from decouple import config
from .models import db, Tweet, User

twit_a = tweepy.OAuthHandler(config('TWT_CON_KEY'),
                             config('TWT_CON_SEC'))

twit_a.set_access_token(config('TWT_ACS_TOK'),
                        config('TWT_ACS_TOK_SEC'))

TWITTER = tweepy.API(twit_a)

# Basilica now
BASILICA = basilica.Connection(config('BASILICA_KEY'))


# Ryan's functions!!! thx Ryan <3
def add_or_update_user(username):
    try:
        # These three lines gets Twitter user adds it
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        db.session.add(db_user)
        # Gets tweets from user's timeline (200)
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # Calc and truncate tweet
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            db.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        db.session.commit()


def add_users(users):
    # Adds for each user
    for user in users:
        add_or_update_user(user)


def update_all_users():
    # Updates tweets for users
    for user in User.query.all():
        add_or_update_user(user.name)


# TEST FUNCTIONS AND MISC
# Get username and twenty tweets
"""
def get_tweets(user):
    username = TWIT.get_user(user)
    tweets = TWIT.user_timeline(id=username.id)
    texts = []
    for i in tweets:
        texts.append(str(i.text))
    embedded = embeddings(texts)
    return username.name, texts, embedded


def embeddings(tweet_texts):
    with BASIL as c:
        embedded = list(c.embed_sentences(tweet_texts))
    return embedded


# Update database
def update_db(user):
    return "tricks"
"""