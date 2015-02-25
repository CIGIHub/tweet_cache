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

    @property
    def followers(self):
        stat = self.followersstats_set.first()
        if stat is None:
            return 'n/a'
        else:
            return stat.followers

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




