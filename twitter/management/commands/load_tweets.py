from django.core.management.base import BaseCommand, CommandError
from twitter.utils import management_load_tweets_and_analytics


class Command(BaseCommand):
    help = 'Loads tweets from the Twitter api and caches them.'

    def handle(self, **options):


        management_load_tweets_and_analytics()
