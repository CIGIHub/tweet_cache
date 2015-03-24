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

    data = {} #map from users to the rows of data.

    for user in users:
        report_data = models.AnalyticsReport.objects.get(user=user, date__year=year, date__month=month)
        fixed_data = models.Analytics.objects.filter(user=user, date__year=year, date__month=month).first()

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
                followers = fixed_data.followers,
                following = fixed_data.following,
                listed = fixed_data.listed,
                tweets_reweeted_count=report_data.tweets_reweeted_count,
                tweets_favorited_count=report_data.tweets_favorited_count,
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

