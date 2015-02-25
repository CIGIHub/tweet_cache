# tweet_cache
Django App to cache twitter data.


To use:

Add 'twitter' to your INSTALLED_APPS setting
 
 INSTALLED_APPS = (
    ...
    'twitter',
)

Run python manage.py migrate

To import tweets:
Add your twitter keys to the settings file
    TWITTER_CONSUMER_KEY = '<your_consumer_key>'
    TWITTER_CONSUMER_SECRET = '<your_consumer_secret>'

Add twitter users to through the admin screen.
Run python manage.py load_tweets

Depends on tweepy.
