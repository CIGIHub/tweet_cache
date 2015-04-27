from django.core.management.base import BaseCommand, CommandError
from twitter.utils import management_load_tweets, management_load_analytics, management_load_analytics_report
from optparse import make_option


class Command(BaseCommand):
    help = 'Loads tweets from the Twitter api and caches them.'

    option_list = BaseCommand.option_list + (
        make_option('--include-tweets', '-t', dest='include_tweets',
                    help="The type of data to import"),
        make_option('--include-analytics', '-a', dest='include_analytics',
                    help="The type of data to import"),
        make_option('--include-analytics-report', '-r', dest='include_analytics_report',
                    help='Limit for importing items'),
    )

    def handle(self, **options):
        include_tweets = options.get('include_tweets', True)
        include_analytics = options.get('include_analytics', True)
        include_analytics_report = options.get('include_analytics_report', False)

        if include_tweets:
            management_load_tweets()
        if include_analytics:
            management_load_analytics()
        if include_analytics_report:
            management_load_analytics_report()
