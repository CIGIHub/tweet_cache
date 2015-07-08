from __future__ import unicode_literals
import time
import datetime
from collections import namedtuple


from django.conf import settings
from django.utils.timezone import now, make_aware

from pytz import utc
import tweepy

from .models import User, Tweet, FollowersStats, Analytics, AnalyticsReport


def management_load_tweets():
    right_now = now()
    api = get_api()
    for user in User.objects.filter(active=True):
        if user.user_id == '':
            user = update_user(user, api)

        if user.capture_tweets == True and user.user_id != '':
            get_tweets_and_followers(user, api)
        time.sleep(5)

        # Done by social.py now.
        #if user.capture_analytics == True and user.user_id != '':
        #    get_analytics(right_now, user, api)
            # TODO: only once a month, and for the last month
        #    get_analytics_report(right_now, user, api)
        #time.sleep(10)


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
    user.current_followers = twitter_user.followers_count
    user.save()
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
            break


tweet_analytic_keys = [
    'tweet_count',
    'retweet_count',
    'reply_count',
    'user_mention_count',
    'link_count',
    'hashtag_count',
]


def get_analytics(time, user, api):
    try:
        twitter_user = api.get_user(user.user_id)
    except tweepy.error.TweepError:
        print(u"Unable to find user page for user id {}".format(user.user_id))
        return

    # Yesterday
    date = (time - datetime.timedelta(1)).date()

    analytics = dict(
        user = user,
        date = date,
        followers = twitter_user.followers_count,
        following = twitter_user.friends_count,
        listed = twitter_user.listed_count
    )

    # Intialize with 0 so a sum over no tweets works
    tweet_data = [(0, 0, 0, 0, 0, 0)]

    #iterate through the timeline until we find a tweet from before yesterday, UTC
    tweets_cursor = tweepy.Cursor(api.user_timeline, user_id=user.user_id)
    for tweet in tweets_cursor.items():
        # if falls into range
        tweet_date = make_aware(tweet.created_at, utc).date()

        if tweet_date > date:
            continue
        if tweet_date < date:
            break

        tweet_data.append((
            1,
            1 if hasattr(tweet, 'retweeted_status') else 0,
            1 if tweet.in_reply_to_status_id is not None else 0,
            len(tweet.entities["user_mentions"]),
            len(tweet.entities["urls"]),
            len(tweet.entities["hashtags"]),
        ))

    combined_tweet_data = [sum(x) for x in zip(*tweet_data)]
    analytics.update(dict(zip(tweet_analytic_keys, combined_tweet_data)))

    Analytics.objects.update_or_create(
            user=user,
            date=date,
            defaults=analytics,
    )


def get_analytics_report(current_time, user, api):
    '''
    Once a month we dig even deeper to get all of the retweets and favorites for a user
    '''
    month_date = datetime.date(current_time.year, current_time.month, 1)

    retweet_count = 0
    favorite_count = 0

    tweets_cursor = tweepy.Cursor(api.user_timeline, user_id=user.user_id, include_rts=False)
    for i, tweet in enumerate(tweets_cursor.items()):

        tweet_date = make_aware(tweet.created_at, utc).date()

        if tweet_date.month > month_date.month:
            continue
        if tweet_date.month < month_date.month:
            break


        if tweet.retweet_count > 0:
            retweet_count += tweet.retweet_count
        if tweet.favorite_count is not None and tweet.favorite_count > 0:
            favorite_count += tweet.favorite_count

        if i % 100 == 0:
            time.sleep(5)

    AnalyticsReport.objects.update_or_create(
        user=user,
        date=month_date,
        defaults=dict(
            tweets_reweeted_count = retweet_count,
            tweets_favorited_count = favorite_count,
        )
    )









