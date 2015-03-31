from django.contrib import admin
from twitter.models import User, Tweet, Analytics, AnalyticsReport


class UserAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'current_followers')


class AnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'user',
        'followers',
        'following',
        'listed',
        'tweet_count',
        'retweet_count',
        'reply_count',
        'user_mention_count',
        'link_count',
        'hashtag_count',
    )


class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'user',
        'tweets_reweeted_count',
        'tweets_favorited_count',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Tweet)
admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(AnalyticsReport, AnalyticsReportAdmin)
