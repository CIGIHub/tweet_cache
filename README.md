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
Add twitter users to through the admin screen.
Run python manage.py load_tweets

Depends on tweepy.
