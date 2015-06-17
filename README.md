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

Socializr Integration
---------------------

tweet_cache also provided a `social.py` file which expects to register
with django-socializr (https://github.com/CIGIHub/django-socializr) a
tool for getting analytics from multiple apis.

tweet_cache can be used without socializr, but be careful to not import
social.py.

To use with django-socializr it should be as simple as running
`manage.py socializr_update`. tweet_cache registers itself with
socializr.
