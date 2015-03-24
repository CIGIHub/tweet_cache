from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models


@python_2_unicode_compatible
class User(models.Model):
    user_id = models.CharField(max_length=32, blank=True)
    screen_name = models.CharField(max_length=128)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    current_followers = models.PositiveIntegerField(default=0)

    capture_tweets = models.BooleanField(default=True)
    capture_analytics = models.BooleanField(default=False)

    # TODO: Add joined date

    @property
    def followers(self):
        return self.current_followers

    def most_recent_tweet(self):
        if self.tweet_set.first() is not None:
            return self.tweet_set.first().processed_text
        return 'N/A'

    def __str__(self):
        return self.screen_name


@python_2_unicode_compatible
class Tweet(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    tweet_id = models.BigIntegerField()
    time = models.DateTimeField()
    account = models.CharField(max_length=30)
    profile_image_url = models.CharField(max_length=256)
    text = models.CharField(max_length=140)
    processed_text = models.CharField(max_length=1028, blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return "%s - %s" % (self.account, self.tweet_id)


@python_2_unicode_compatible
class FollowersStats(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    followers = models.PositiveIntegerField()
    as_of = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-as_of']

    def __str__(self):
        return "Followers for {} as of {}".format(self.user.screen_name, self.as_of)


class Analytics(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()

    # Stats we collect every period, not incremental
    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    listed = models.PositiveIntegerField(default=0)

    # Stats which are collect only from the 24 peroid defined by date which we can
    # aggergate ourselves
    tweet_count = models.PositiveIntegerField(default=0)
    # classifying the users tweets
    retweet_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    user_mention_count = models.PositiveIntegerField(default=0)
    link_count = models.PositiveIntegerField(default=0)
    hashtag_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = 'analytics'


class AnalyticsReport(models.Model):
    '''
    Additoinal data collected  monthly based on the data we have collected
    '''
    user = models.ForeignKey(User)
    date = models.DateField() # first day of the month

    # Stats on engagement for the last 3,200 tweets
    tweets_reweeted_count = models.PositiveIntegerField(default=0)
    tweets_favorited_count = models.PositiveIntegerField(default=0)


