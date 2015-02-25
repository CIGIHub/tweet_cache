from __future__ import unicode_literals

from django.conf import settings
from django.utils.timezone import make_aware
from pytz import utc

import time
import tweepy

from .models import User, Tweet, FollowersStats


def management_load_tweets():
    api = get_api()
    for user in User.objects.filter(active=True):
        if user.user_id == '':
            user = update_user(user, api)

        if user.user_id != '':
            get_tweets_and_followers(user, api)
        time.sleep(5)


_api = None
def get_api():
    global _api
    if _api is None:
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
        # Uncomment the following if we need more access, for example, mentions_timeline.
        # auth.set_access_token(settings.TWITTER_OATH_ACCESS_TOKEN, settings.TWITTER_OATH_ACCESS_TOKEN_SECRET)
        _api = tweepy.API(auth)
    return _api


def update_user(user, api):
    try:
        twitter_user = api.get_user(user.screen_name)
    except tweepy.error.TweepError:
        print(u"Unable to find user page for screen name {}".format(user.screen_name))
        return user
    user.user_id = twitter_user.id
    user.save()
    return user


def get_tweets_and_followers(user, api):
    try:
        twitter_user = api.get_user(user.user_id)
    except tweepy.error.TweepError:
        print(u"Unable to find user page for user id {}".format(user.user_id))
        return
    get_tweets(twitter_user, user, api)
    get_followers(twitter_user, user, api)


def get_tweets(twitter_user, user, api):
    public_tweets = tweepy.Cursor(api.user_timeline, user_id=user.user_id)
    process_tweets(public_tweets, user)


def get_followers(twitter_user, user, api):
    FollowersStats.objects.create(
        user=user,
        followers=twitter_user.followers_count,
    )


def process_tweets(tweets_cursor, user):
    not_created = 0
    for tweet in tweets_cursor.items(200):
        tweet_text = tweet.text
        hashtags = tweet.entities["hashtags"]
        links = tweet.entities["urls"]
        user_mentions = tweet.entities["user_mentions"]
        symbols = tweet.entities["symbols"]
        created_at = make_aware(tweet.created_at, utc)

        for hashtag in hashtags:
            original_tag = "#%s" % hashtag['text']
            markup = "<a class='twitter-link hashtag' href='https://twitter.com%s'>%s</a>" % (original_tag,
                                                                                              original_tag)
            tweet_text = tweet_text.replace(original_tag, markup)

        for link in links:
            original_link = link['url']
            markup = "<a class='twitter-link' href='%s'>%s</a>" % (link['expanded_url'], original_link)
            tweet_text = tweet_text.replace(original_link, markup)

        for user_mention in user_mentions:
            original_mention = "@%s" % user_mention['screen_name']
            markup = "<a class='twitter-link user-mention' href='https://twitter.com/%s'>%s</a>" % (original_mention,
                                                                                                    original_mention)
            tweet_text = tweet_text.replace(original_mention, markup)

        cached_tweet, created = Tweet.objects.get_or_create(
                tweet_id=tweet.id,
                defaults={
                    'user': user,
                    'account': user.screen_name,
                    'time': created_at,
                    'profile_image_url': tweet.user.profile_image_url_https,
                    'text': tweet.text,
                    'processed_text': tweet_text,
                })

        if not created:
            cached_tweet.user = user
            cached_tweet.account = user.screen_name
            cached_tweet.time = created_at
            cached_tweet.profile_image_url = tweet.user.profile_image_url_https
            cached_tweet.text = tweet.text
            cached_tweet.processed_text = tweet_text

            cached_tweet.save()
            not_created += 1

        if not_created > 10:
            break;

