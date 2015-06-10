from django.shortcuts import render
from django.db.models import Sum

from . import models


def analytics_compare_example(request, template="analytics_compare_example.html"):
    '''
    A simplistic view which demostraits how the analytic models can be used.
    '''
    month = 3
    year = 2015

    users = models.User.objects.filter(capture_analytics=True)

    data = {}  # map from users to the rows of data.

    for user in users:
        report_data = models.AnalyticsReport.objects.filter(user=user, date__year=year, date__month=month).first()
        tweets_reweeted_count = 0
        tweets_favorited_count = 0
        if report_data:
            tweets_reweeted_count = report_data.tweets_reweeted_count
            tweets_favorited_count = report_data.tweets_favorited_count

        fixed_data = models.Analytics.objects.filter(user=user, date__year=year, date__month=month).first()
        followers = 0
        following = 0
        listed = 0
        if fixed_data:
            followers = fixed_data.followers
            following = fixed_data.following
            listed = fixed_data.listed


        analytics_data = (models.Analytics.objects
            .filter(user=user, date__year=year, date__month=month)
            .aggregate(
                **dict([(x,Sum(x)) for x in (
                    'tweet_count',
                    'retweet_count',
                    'reply_count',
                    'user_mention_count',
                    'link_count',
                    'hashtag_count',
                )])
            )
        )

        analytics_data.update(
            dict(
                followers=followers,
                following=following,
                listed=listed,
                tweets_reweeted_count=tweets_reweeted_count,
                tweets_favorited_count=tweets_favorited_count,
            )
        )
        data[user] = analytics_data

    return render(
        request,
        template,
        dict(
            data=data,
        )
    )


def twitter_dashboard_example(request, template="twitter_dashboard_example.html"):
    '''
    A simplistic view which show how to work with the twitter data.
    '''

    users = models.User.objects.filter(capture_tweets=True).order_by("-current_followers")

    return render(
        request,
        template,
        dict(
            users=users,
        )
    )

