from __future__ import unicode_literals
import time
import datetime
from collections import namedtuple

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import tweepy

from socializr.base import SocializrConfig, register
from socializr.utils import get_setting

from .models import User, Analytics
from .utils import get_analytics, get_analytics_report


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


class TwitterConfig(SocializrConfig):
    def collect(self):
        right_now = now()
        api = get_api()
        for user in User.objects.filter(active=True):
            if user.capture_analytics == True and user.user_id != '':
                get_analytics(right_now, user, api)
                if right_now.day == 1:
                    get_analytics_report(right_now, user, api)
            time.sleep(10)


register(TwitterConfig)
