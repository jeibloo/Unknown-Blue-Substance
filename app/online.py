import basilica
import tweepy
from decouple import config
from .models import db, Tweet, User

twit_a = tweepy.OAuthHandler(config('TWT_CON_KEY'),
                             config('TWT_CON_SEC'))

twit_a.set_access_token(config('TWT_ACS_TOK'),
                        config('TWT_ACS_TOK_SEC'))

TWIT = tweepy.API(twit_a)

# Basilica now
BASIL = basilica.Connection(config('BASILICA_KEY'))
