import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .online import BASILICA


def predict_user(user1_name, user2_name, tweet_text):
    # Filter is from SQLAlchemy
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()

    # 
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])

    # Create labels (1's and 0's)
    user1_labels = np.ones(len(user1.tweets))
    user2_labels = np.zeros(len(user2.tweets))

    # Stack the embeddings and put into variable, creates (at least 2D)
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([user1_labels, user2_labels])

    # Set model and 'fit'(train) on embeddings and labels
    log_reg = LogisticRegression(solver='lbfgs', max_iter=1000)
    log_reg.fit(embeddings, labels)

    # Use BASILICA to embed the individual tweet we want to analyze
    # Guess you can choose Twitter as your model? (wow)
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    # The :, 1 separate rows from columns apparently...
    return log_reg.predict_proba(np.array([tweet_embedding]))[:, 1]
